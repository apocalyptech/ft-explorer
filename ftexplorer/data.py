#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2018, CJ Kucera
# All rights reserved.
#   
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
import sys
import lzma
import json

class Node(object):
    """
    A node in our tree
    """

    def __init__(self, name):
        self.name = name
        self.filename = None
        self.pos_start = 0
        self.length = 0
        self.loaded = False
        self.has_data = False
        self.data = []
        self.child_keys = None
        self.children = {}

    def __repr__(self):
        return self.name

    def __getitem__(self, item):
        """
        Lets us behave somewhat like a list
        """
        if self.child_keys is None:
            self.child_keys = sorted(self.children.keys(), key=str.lower)
        return self.children[self.child_keys[item]]

    def start_data(self, obj_name_parts, game, filename, pos_start, length):
        """
        Starts recording data for the specified object.
        Returns a list which can be appended to
        """
        if len(obj_name_parts) == 0:
            self.filename = filename
            self.pos_start = pos_start
            self.length = length
            self.game = game
            self.has_data = True
            self.data = []
            return self.data
        lower = obj_name_parts[0].lower()
        if lower not in self.children:
            self.children[lower] = Node(obj_name_parts[0])
        return self.children[lower].start_data(
                obj_name_parts[1:],
                game,
                filename,
                pos_start,
                length)

    def load(self):
        """
        Loads ourselves from our data file
        """
        if self.loaded or not self.has_data:
            return self.data
        if self.filename:
            try:
                with lzma.open(os.path.join('resources', self.game, 'dumps', self.filename), 'rb') as df:
                    df.seek(self.pos_start)
                    self.data = df.read(self.length).decode('latin1').splitlines()
                    self.loaded = True
                    return self.data
            except Exception as e:
                return ['ERROR!  Could not load data: {}'.format(str(e))]

    def parse_data_value(self, value):
        """
        Parses a structure inside our data - basically a property value,
        but also any "sub" value that's inside parens in there.  This is
        *highly* inefficient the way it's currently written -- those
        parenthetical statements end up getting looped over multiple times
        throughout here.  The code is also fairly laughable, so sorry about
        that.  This isn't actually used by the GUI (thankfully).  It's
        just here to support some data-inspection scripts.  Note that in
        the event we get some data I didn't plan for, this function could
        raise an Exception.

        Note that this does NOT properly deal with quotes - if you have
        something quoted which happens to have a comma in it, for instance,
        things will probably go awry.
        """
        #print('parsing: {}'.format(value))
        if len(value) == 0:
            return value
        elif value[0] == '(' and value[-1] == ')':
            newdict = {}
            cur_level = 0
            cur_key = []
            cur_value = []
            cur_inner = []
            state = 0
            first_key_pass = False
            for char in value[1:-1]:

                # State 0 - reading key
                if state == 0:
                    if char == '=':
                        state = 1
                    elif first_key_pass and char == ',':
                        pass
                    else:
                        cur_key.append(char)
                    first_key_pass = False

                # State 1 - reading value
                elif state == 1:
                    if char == ',':
                        newdict[''.join(cur_key)] = self.parse_data_value(''.join(cur_value))
                        cur_key = []
                        cur_value = []
                        cur_inner = []
                        first_key_pass = True
                        state = 0
                    elif char == '(':
                        cur_level += 1
                        cur_inner.append(char)
                        state = 2
                    else:
                        cur_value.append(char)

                # State 2 - Reading first char of an inner paren stanza
                elif state == 2:
                    if char == '(':
                        newdict[''.join(cur_key)] = []
                        state = 4
                        at_first = True
                    else:
                        state = 3

                # State 3 - reading a regular inner dict
                if state == 3:
                    if char == '(':
                        cur_level += 1
                    elif char == ')':
                        cur_level -= 1
                    cur_inner.append(char)
                    if cur_level == 0:
                        newdict[''.join(cur_key)] = self.parse_data_value(''.join(cur_inner[1:-1]))
                        cur_key = []
                        cur_value = []
                        cur_inner = []
                        first_key_pass = True
                        state = 0

                # State 4 - Reading a list
                elif state == 4:
                    if char == '(':
                        cur_level += 1
                        if not at_first:
                            cur_inner.append(char)
                    elif char == ')':
                        cur_level -= 1
                        cur_inner.append(char)

                        if cur_level == 1:
                            newdict[''.join(cur_key)].append(self.parse_data_value(''.join(cur_inner)))
                            cur_inner = []

                        elif cur_level == 0:
                            cur_key = []
                            cur_value = []
                            cur_inner = []
                            first_key_pass = True
                            state = 0

                    elif cur_level == 1 and char == ',':
                        pass

                    else:
                        cur_inner.append(char)

                    at_first = False

            # Clean up, depending on our state
            if state == 0:
                pass
            elif state == 1:
                newdict[''.join(cur_key)] = self.parse_data_value(''.join(cur_value))
            else:
                raise Exception("shouldn't be able to get here")

            return newdict
        else:
            parts = value.split(',')
            if len(parts) == 1:
                # See the comment on the other side of the `if` here.  We may have
                # a single-element dict.
                if '=' in value:
                    newdict = {}
                    (key, val) = value.split('=', 1)
                    newdict[key] = val
                    return newdict
                else:
                    return value
            else:
                # This is hokey, and a byproduct of the stupid way we're parsing
                # this stuff (and is susceptible to corner cases) - anyway, at
                # this point we MAY have a dict, or we may just have a string
                # which happens to have a comma in it.  We'll just test the first
                # element and see if there's an equals sign in it.  If it does,
                # then we'll parse it as a dict.  If not, just return as a string.
                if '=' in parts[0]:
                    newdict = {}
                    for part in parts:
                        (key, val) = part.split('=', 1)
                        newdict[key] = val
                    return newdict
                else:
                    return value

    def get_structure(self):
        """
        Returns ourselves as a data structure of lists/dicts.  This is
        not actually used by the GUI at the moment - it's just here to
        support some data-inspection scripts I'm writing.
        """
        main = {}
        for line in self.load():
            match = re.match('^\s*([A-Za-z0-9_]+)(\((\d+)\))?=(.*)$', line)
            if match:
                key = match.group(1)
                index = match.group(3)
                value = match.group(4)
                if index is None:
                    main[key] = self.parse_data_value(value)
                else:
                    if key not in main:
                        main[key] = []
                    main[key].append(self.parse_data_value(value))
            #else:
            #    print(line)
        return main

    def get_children_with_name(self, prefix):
        """
        Returns a list of children of ourselves which match the given
        prefix to the child name.
        """
        prefix = prefix.lower()
        for childname, child in self.children.items():
            if childname.lower().startswith(prefix):
                yield child

class Data(object):
    """
    Top-level data object to hold everything we're interested in.
    """

    def __init__(self, game):

        self.top = Node('')
        self.game = game

        # Read in our index
        index_filename = os.path.join('resources', game, 'dumps', 'index.json.xz')
        index = []
        if os.path.exists(index_filename):
            with lzma.open(index_filename, 'rt') as df:
                index = json.load(df)

        # Populate our basic node tree
        for (filename, filename_data) in index.items():
            for (parts, pos_start, length) in filename_data:
                self.top.start_data(parts,
                        game=game,
                        filename=filename,
                        pos_start=pos_start,
                        length=length)

    def __getitem__(self, item):
        """
        Lets us act somewhat like a list
        """
        return self.top[item]

    def get_all_by_type(self, obj_type):
        """
        Returns a list of all objects of the given type.  Note that this is
        not efficient at all, and doesn't cache anything - we will loop
        through the whole file and match regexes each time this is called.
        Also note that the object type is case-sensitive, and must match
        the data filename.
        """
        objects = []
        with lzma.open(os.path.join('resources', self.game, 'dumps',
                '{}.dump.xz'.format(obj_type)), 'rt') as df:
            for line in df.readlines():
                match = re.match('^\*\*\* Property dump for object \'\S+ (\S+)\'.*$', line)
                if match:
                    objects.append(match.group(1))
        return objects

    def get_node_paths_by_full_object(self, name):
        """
        Returns a list of components which can be used to find the given
        object `name` in our tree.
        """
        components = re.split('[\.:]', name)
        cur_node = self.top
        paths = []

        # Handle a case where we may have split things up by wildcard
        if '_' in components[0]:
            (left, right) = components[0].rsplit('_', 1)
            test_name = '{}_*'.format(left.lower())
            if test_name in cur_node.children:
                cur_node = cur_node.children[test_name]
                paths.append(cur_node)

        # Now iterate
        for component in components:
            cur_node = cur_node.children[component.lower()]
            paths.append(cur_node)

        # Return the list
        return paths

    def get_node_by_full_object(self, name):
        """
        Retrieves a node by the full object name.
        """
        return self.get_node_paths_by_full_object(name)[-1]

    def get_level_package_names(self, levelname):
        """
        Returns a list of package names for the given level name.
        """
        main_name = '{}.TheWorld'.format(levelname)
        level_packages = ['{}:PersistentLevel'.format(main_name)]
        main_node = self.get_node_by_full_object(main_name)
        for child in main_node.get_children_with_name('levelstreaming'):
            childstruct = child.get_structure()
            if childstruct['LoadedLevel'] != 'None':
                level_packages.append(childstruct['LoadedLevel'].split("'", 2)[1])
        return level_packages

    def get_level_package_nodes(self, levelname):
        """
        Returns a list of nodes for the given level name.  Will be a list of
        tuples.  The first element is the base node name, the second is the
        node itself.
        """
        return [(name, self.get_node_by_full_object(name)) for name in self.get_level_package_names(levelname)]
