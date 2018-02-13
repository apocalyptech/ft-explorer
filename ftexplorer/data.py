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

class Node(object):
    """
    A node in our tree
    """

    def __init__(self, name, obj_type=None):
        self.name = name
        self.obj_type = obj_type
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

    def start_data(self, obj_name_parts, obj_type):
        """
        Starts recording data for the specified object.
        Returns a list which can be appended to
        """
        if len(obj_name_parts) == 0:
            self.obj_type = obj_type
            return self.data
        if obj_name_parts[0] not in self.children:
            self.children[obj_name_parts[0]] = Node(obj_name_parts[0])
        return self.children[obj_name_parts[0]].start_data(obj_name_parts[1:], obj_type)

class Data(object):
    """
    Top-level data object to hold everything we're interested in.
    """

    def __init__(self):

        self.top = Node('')

        #with open('resources/Resource - InventoryPartListCollectionDefinition.txt', 'r') as df:
        with os.scandir('resources') as it:
            for entry in it:
                if entry.name[:11] == 'Resource - ' and entry.name[-4:] == '.txt':
                    print('Processing resource file: {}'.format(entry.name))
                    with open(entry.path, 'r') as df:
                        cur_obj = None
                        obj_type = None
                        obj_data = []
                        for line in df.readlines():

                            if line[:29] == '*** Property dump for object ':
                                (obj_type, cur_obj) = line[30:-6].split(' ', 1)
                                parts = re.split('[\.:]', cur_obj)
                                obj_data = self.top.start_data(parts, obj_type)

                            # Always append the line
                            if not cur_obj:
                                raise Exception('found data without having an object')
                            #obj_data.append(line.rstrip())
                            obj_data.append(line)

        print('Done processing files')

    def __getitem__(self, item):
        """
        Lets us act somewhat like a list
        """
        return self.top[item]
