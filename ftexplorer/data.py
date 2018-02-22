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

class Data(object):
    """
    Top-level data object to hold everything we're interested in.
    """

    def __init__(self, game):

        self.top = Node('')

        # Read in our index
        index_filename = os.path.join('resources', game, 'dumps', 'index.json.xz')
        index = []
        if os.path.exists(index_filename):
            with lzma.open(index_filename, 'rt') as df:
                index = json.load(df)

        # Populate our basic node tree
        for (filename, pos_start, length, parts) in index:
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
