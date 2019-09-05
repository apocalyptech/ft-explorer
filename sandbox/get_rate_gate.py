#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Finds all objects which exist inside classes which include a
# *Rate* attribute somewhere in there whose object names contain
# the given string.  Used when trying to track down where in
# the world the speed of Sanctuary's main gate is coming from.
#
# Requires having run find_classes_with_rate.py previously.

from ftexplorer.data import Data

#search_for = 'Gate'
search_for = 'Sanct'

classes = []
with open('rate_classes.txt') as df:
    for line in df:
        classes.append(line.strip())

data = Data('BL2')
for classname in classes:
    for obj_name in data.get_all_by_type(classname):
        if search_for in obj_name:
            print(obj_name)
