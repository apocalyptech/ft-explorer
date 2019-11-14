#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Finds all objects which exist inside classes which include a
# *Rate* attribute somewhere in there whose object names contain
# the given string.  Used when trying to track down where in
# the world the speed of Sanctuary's main gate is coming from.
#
# Requires having run find_classes_with_rate.py previously.

from ftexplorer.data import Data

data = Data('BL2')
print('type,speed,recovery,up,down,left,right,minvert,minhoriz')
for obj_name in data.get_all_by_type('WeaponTypeDefinition'):
    obj = data.get_struct_by_full_object(obj_name)
    print('{},{},{},{},{},{},{},{},{}'.format(
        obj_name,
        obj['WeaponKickSpeed'],
        obj['WeaponKickRecoveryTime'],
        obj['WeaponKickUp'],
        obj['WeaponKickDown'],
        obj['WeaponKickLeft'],
        obj['WeaponKickRight'],
        obj['MinimumVerticalPercentage'],
        obj['MinimumHorizontalPercentage'],
        ))
