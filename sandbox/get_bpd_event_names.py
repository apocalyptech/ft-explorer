#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

data = Data('BL2')

objects = []
objects.extend(data.get_all_by_type('AIBehaviorProviderDefinition'))
objects.extend(data.get_all_by_type('BehaviorProviderDefinition'))
num_objects = len(objects)

event_names = set()
for idx, obj_name in enumerate(sorted(objects)):
    sys.stderr.write("BPD {}/{}\r".format(idx, num_objects))
    obj_struct = data.get_struct_by_full_object(obj_name)
    for seq in obj_struct['BehaviorSequences']:
        for event in seq['EventData2']:
            event_names.add(event['UserData']['EventName'])
print('', file=sys.stderr)
for name in sorted(event_names):
    print(name)
