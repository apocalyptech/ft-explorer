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

import re
import os
import sys
import lzma
import json

found_index = 'found.json.xz'
launch_log = 'logs/launch.log'
data_dir = 'dumps'

# Load in our found objects, if we have it
found_objects = {}
if os.path.exists(found_index):
    with lzma.open(found_index, 'rt') as df:
        found_objects = json.load(df)
    print('Loaded {} found objects from {}'.format(sum([len(v) for v in found_objects.values()]), found_index))

# Load our logfile and grab all the data we can
cur_obj = None
cur_type = None
data_files = {}
written_stats = {}
with open(launch_log, 'r', encoding='latin1') as df:
    for line in df.readlines():

        # Look for new objects
        match = re.match('^\[[0-9\.]+\] Log: \*\*\* Property dump for object \'(\S+) (\S+)\' \*\*\*\s*', line)
        if match:
            cur_type = match.group(1)
            cur_obj = match.group(2)

            if cur_type in found_objects and cur_obj in found_objects[cur_type]:
                print('WARNING: {} {} already in our found index'.format(cur_type, cur_obj))
                cur_obj = None
                cur_type = None
            else:

                # Keep track of how many objects we've written
                if cur_type not in written_stats:
                    written_stats[cur_type] = 1
                else:
                    written_stats[cur_type] += 1
                
                # And also add the new object to our found dict
                if cur_type not in found_objects:
                    found_objects[cur_type] = {}
                found_objects[cur_type][cur_obj] = True

        # Check for our dump end
        if 'Primary PhysX scene will be in software' in line:
            if cur_obj and cur_type and cur_type in data_files:
                # Make sure we always have an empty line at the end of the files
                print('', file=data_files[cur_type])
            cur_obj = None
            cur_type = None

        # Write out to our data file if we found anything
        if cur_obj and cur_type:
            if cur_type not in data_files:
                data_files[cur_type] = open(os.path.join(data_dir, '{}.dump'.format(cur_type)), 'a', encoding='latin1')
                written_stats[cur_type] = 0
            print(line[15:].rstrip(), file=data_files[cur_type])

# Close out all our filehandles
for df in data_files.values():
    df.close()

# Report on what we wrote
for (key, val) in sorted(written_stats.items()):
    print('{}: {} new objects'.format(key, val))
print('--')
print('{} new objects total'.format(sum(written_stats.values())))

# Save out our found index
with lzma.open(found_index, 'wt') as df:
    json.dump(found_objects, df)
total_objs = 0
print('Saved {} found objects to {}'.format(sum([len(v) for v in found_objects.values()]), found_index))
print('--')
