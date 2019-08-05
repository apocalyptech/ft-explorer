#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
import argparse
from ftexplorer.data import Data

data = Data('BL2')

objects = []
objects.extend(data.get_all_by_type('AIBehaviorProviderDefinition'))
objects.extend(data.get_all_by_type('BehaviorProviderDefinition'))

found_event_names = {}

for bpd_name in objects:
    bpd = data.get_node_by_full_object(bpd_name).get_structure()
    if 'BehaviorSequences' in bpd and bpd['BehaviorSequences'] != 'None' and bpd['BehaviorSequences'] != '':
        for seq in bpd['BehaviorSequences']:
            if 'EventData2' in seq and seq['EventData2'] != 'None' and seq['EventData2'] != '':
                for event in seq['EventData2']:
                    if 'UserData' in event and event['UserData'] != 'None' and event['UserData'] != '':
                        event_name = event['UserData']['EventName']
                        if 'NPC' in event_name:
                            if event_name not in found_event_names:
                                found_event_names[event_name] = set()
                            found_event_names[event_name].add(bpd_name)

for (name, bpds) in found_event_names.items():
    print(name)
    for bpd in bpds:
        print(' * {}'.format(bpd))
    print('')
