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
output_dumps = 'binaries/objects'
per_file_limit = 10000

# Load in our found objects, if we have it
found_objects = {}
if os.path.exists(found_index):
    with lzma.open(found_index, 'rt') as df:
        found_objects = json.load(df)
    print('Loaded {} found objects from {}'.format(sum([len(v) for v in found_objects.values()]), found_index))

# Load our launch.log to find what objects are available, and figure out
# if we need to load them or not.
num_dumps = 0
file_num = 1
cur_output_file = '{}{}'.format(output_dumps, file_num)
with open(launch_log, 'r', encoding='latin1') as df:
    odf = open(cur_output_file, 'w')
    for line in df.readlines():
        match = re.match('^\[[0-9\.]+\] Log: \d+\) (\S+) (\S+)\.Name = \S+\s*$', line)
        if match:
            obj_type = match.group(1)
            obj_name = match.group(2)
            if obj_type not in found_objects or obj_name not in found_objects[obj_type]:
                if num_dumps >= per_file_limit:
                    odf.close()
                    print('Generated {} dump statements to {}'.format(num_dumps, cur_output_file))
                    file_num += 1
                    cur_output_file = '{}{}'.format(output_dumps, file_num)
                    odf = open(cur_output_file, 'w')
                    num_dumps = 0
                print('obj dump {}'.format(obj_name), file=odf)
                num_dumps += 1

                # We're not actually writing this out, but it should prevent some duplicate
                # statements from being generated, at least.
                if obj_type not in found_objects:
                    found_objects[obj_type] = {}
                found_objects[obj_type][obj_name] = True

# Report on how many dumps we generated for the final file
print('Generated {} dump statements to {}'.format(num_dumps, cur_output_file))
