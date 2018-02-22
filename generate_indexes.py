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

# This script generates an index file which FT/BLCMM Explorer can then use
# to know what elements should be in its tree, rather than having to load all
# the data at start time.  This means that there's technically a delay between
# the user clicking on an element and the element being drawn, though in
# practice I haven't been able to actually notice it.
#
# Note that this process is quite slow...  We're reading the data line-by-line
# but still need to know the byte position within the file so that we can find
# each element, so we can't take advantage of any of Python's inherent
# optimizations when doing line-based file reads.  Since this is a process
# intended to only be run by myself whenever/if the data files get updated, I
# haven't bothered to look into optimizing it.  On my machine it takes a good
# twelve minutes to generate.
#
# Internally, the index is a list of lists, where each element of the main
# list contains these elements:
#
#   1) Filename
#   2) Start position (uncompressed)
#   3) Length (uncompressed
#   4) A list defining exactly where the item should live in the tree
#      (its name, basically, but exploded)

out_file = 'index.json.xz'
min_collapse_count = 2

# Print a warning - everyone Not Me won't actually care about this.
print()
print("This utility is only useful if you've updated the resource files with")
print("new data.  It will update the game index files to reflect the new")
print("contents, so it's available in the app.")
print()
print('Hit Ctrl-C now to exit, or Enter to continue...')
input()

# Generate indexes for both games.
for game in ['BL2', 'TPS']:

    print('Indexing {} Game Data'.format(game))
    print('----------------------')

    game_dir = os.path.join('resources', game, 'dumps')
    game_index = os.path.join(game_dir, out_file)

    collapse_names = {}
    full_collapse_names = set()

    # Loop through files and build the index
    index = {}
    with os.scandir(game_dir) as it:
        for entry in sorted(it, key=lambda e: getattr(e, 'name').lower()):
            if entry.name[-8:] == '.dump.xz' or entry.name[-7:] == '.txt.xz':
                print('Processing {}'.format(entry.name))
                with lzma.open(entry.path, 'rt', encoding='latin1') as df:
                    obj_name = None
                    begin_pos = df.tell()
                    line = df.readline()
                    while line:
                        match = re.search(r"Property dump for object '\S+ (\S+)' ", line)
                        if match:
                            if obj_name:
                                index[obj_name][2] = begin_pos - index[obj_name][1]
                            obj_name = match.group(1)
                            main_parts = re.split('[:\.]', obj_name)
                            index[obj_name] = [entry.name, begin_pos, 0, main_parts]

                            # Grab info about our top level, to see if it makes sense to
                            # do extra splitting on it.
                            top_name = main_parts[0].lower()
                            full_collapse_names.add(top_name)
                            name_parts = top_name.rsplit('_', 1)
                            if len(name_parts) > 1:
                                if name_parts[0] not in collapse_names:
                                    collapse_names[name_parts[0]] = set()
                                collapse_names[name_parts[0]].add(name_parts[1])

                        begin_pos = df.tell()
                        line = df.readline()
                    if obj_name:
                        index[obj_name][2] = begin_pos - index[obj_name][1]

    # Filter out any top-level keys which are substrings of another key,
    # or which don't have enough children
    to_prune = set()
    for (key, vals) in collapse_names.items():

        # We need at least `min_collapse_count` items underneath us to
        # qualify for collapsing
        if len(vals) < min_collapse_count:
            to_prune.add(key)
        else:
            parts = key.split('_')
            for num in range(len(parts)):
                # Prune any substrings
                testval = '_'.join(parts[:num])
                if testval in collapse_names:
                    to_prune.add(testval)

    # Also prune any collapsing which matches on a real object name,
    # so we don't have a confusing-looking tree
    for key in full_collapse_names:
        if key in collapse_names:
            to_prune.add(key)

    # Now do the pruning
    for key in to_prune:
        del collapse_names[key]

    # Add in a pre-split Parts list to our index, split
    # out additionally by `collapse_names`, if it applies.
    for (name, data) in index.items():
        name_parts = data[3][0].rsplit('_', 1)
        if len(name_parts) > 1:
            if name_parts[0].lower() in collapse_names:
                data[3][:1] = ['{}_*'.format(name_parts[0]), data[3][0]]

    # Write out our index
    print('Writing index to {}'.format(game_index))
    with lzma.open(game_index, 'wt') as df:
        json.dump(list(index.values()), df)

    print()

print('Done!')
