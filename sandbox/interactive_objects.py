#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data, Weight

data = Data('BL2')
keys = {}
ios = data.get_all_by_type('WillowInteractiveObject')
for io_name in sorted(ios):
    io_obj = data.get_struct_by_full_object(io_name)
    iodef_name = Data.get_struct_attr_obj(io_obj, 'InteractiveObjectDefinition')
    if iodef_name and iodef_name == 'GD_Balance_Treasure.InteractiveObjects.InteractiveObj_StorageLocker':
        for key in io_obj.keys():
            if type(io_obj[key]) == str:
                if key not in keys:
                    keys[key] = {}
                if io_obj[key] not in keys[key]:
                    keys[key][io_obj[key]] = 0
                keys[key][io_obj[key]] += 1

for key in sorted(keys.keys()):
    values = keys[key]
    if len(values) > 1:
        print(key)
        for (value, count) in values.items():
            print(' * {}: {}'.format(value, count))
        print('')
