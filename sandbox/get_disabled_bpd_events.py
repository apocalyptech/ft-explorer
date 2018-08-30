#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

data = Data('TPS')
for bpd_name in sorted(data.get_all_by_type('BehaviorProviderDefinition')):
    bpd = data.get_struct_by_full_object(bpd_name)
    found_disabled = False
    for seq_idx, seq in enumerate(bpd['BehaviorSequences']):
        if found_disabled:
            break
        for event_idx, event in enumerate(seq['EventData2']):
            enabled = event['UserData']['bEnabled']
            name = event['UserData']['EventName']
            if enabled != 'True':
                found_disabled = True
                print('{}: [{}] {} [{}]'.format(bpd_name, seq_idx, name, event_idx))
                break
