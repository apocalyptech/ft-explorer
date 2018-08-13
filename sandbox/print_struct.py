#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

game = sys.argv[1]
obj = sys.argv[2]

data = Data(game.upper())
val = data.get_struct_by_full_object(obj)
print(val)

