#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import struct
from ftexplorer.data import Data

data = Data('BL2')

#bpd = data.get_struct_by_full_object('GD_ButtStallion_Proto.Character.AIDef_ButtStallion_Proto:AIBehaviorProviderDefinition_1')
bpd = data.get_struct_by_full_object('gd_slotmachine.SlotMachine:BehaviorProviderDefinition_0')
behavior_linkids = {}
for idx, cold in enumerate(bpd['BehaviorSequences'][1]['ConsolidatedOutputLinkData']):
    compliment = int(cold['LinkIdAndLinkedBehavior'])
    # Use big-endian just for clarity's sake
    packed = struct.pack('>i', compliment)
    #print('{:08b} {:08b} {:08b} {:08b}'.format(packed[0], packed[1], packed[2], packed[3]))
    #linkid = compliment >> 16
    #linkid = compliment >> 24
    linkid = packed[0]
    behavior = compliment & 0xFF
    if behavior not in behavior_linkids:
        behavior_linkids[behavior] = {}
    if linkid not in behavior_linkids[behavior]:
        behavior_linkids[behavior][linkid] = 1
    else:
        behavior_linkids[behavior][linkid] += 1
    print('[{:3d}] {:9d} ({:08b} {:08b} {:08b} {:08b}): {}, {}'.format(idx, compliment, packed[0], packed[1], packed[2], packed[3], linkid, behavior))

print('')
for behavior, linkids in behavior_linkids.items():

    show_behavior = False
    if len(linkids) == 1:
        for val in linkids.values():
            if val > 1:
                show_behavior = True
                break
    else:
        show_behavior = True

    if show_behavior:
        print('{}: {}'.format(behavior, linkids))
