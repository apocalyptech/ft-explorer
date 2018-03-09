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

# The main app doesn't have a search, of course.  But at the moment,
# FT's TPS data is a bit anemic, and BLCMM's TPS data is entirely
# nonexistant, and it'd be nice to be able to search.  So, this'll
# do that.  Expect it to be slow.

import os
import re
import sys
import lzma
import colorama
import argparse

parser = argparse.ArgumentParser(
    description='Search through FT-Explorer\'s BL2/TPS data',
    )

parser.add_argument('-n', '--nocolor',
    action='store_true',
    help='Supress color output',
    )

parser.add_argument('game',
    choices=['bl2', 'tps'],
    help='Which game to search',
    )

parser.add_argument('searchstr',
    help='String to search for',
    )

args = parser.parse_args()

game = args.game.upper()
search_str = args.searchstr.lower()

if not args.nocolor:
    colorama.init(autoreset=True, strip=False)

with os.scandir(os.path.join('resources', game, 'dumps')) as it:
    for entry in sorted(it, key=lambda e: getattr(e, 'name').lower()):
        if entry.name[-8:] == '.dump.xz':
            with lzma.open(entry.path, 'rt', encoding='latin1') as df:
                cur_obj = None
                cur_type = None
                found_result = False
                for line in df.readlines():
                    match = re.search('\*\*\* Property dump for object \'(\S+) (\S+?)\' \*\*\*', line)
                    if match:
                        cur_type = match.group(1)
                        cur_obj = match.group(2)
                        found_result = False
                    if not found_result and cur_obj and cur_type and search_str in line.lower():
                        found_result = True
                        if args.nocolor:
                            print("{}'{}'".format(cur_type, cur_obj))
                        else:
                            print("{}{}{}'{}'".format(colorama.Fore.BLUE, cur_type, colorama.Fore.YELLOW + colorama.Style.DIM, cur_obj))
