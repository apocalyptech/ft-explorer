#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import re
import os
import lzma

# Finding class types which have an attribute with `Rate` in the
# name (but omitting `RotationRate`).  This is actually run versus
# the data collected by https://github.com/BLCM/DataDumper/

rate_re = re.compile('^\s*([^=]*?Rate[^=]*?)=.*')

for filename in sorted(os.listdir('.')):
    if filename.endswith('.dump.xz'):
        with lzma.open(filename, 'rt', encoding='latin1') as df:
            for line in df:
                match = rate_re.match(line)
                if match:
                    if match.group(1) != 'RotationRate':
                        print(filename[:-8])
                        break
