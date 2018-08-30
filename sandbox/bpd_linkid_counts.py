#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import struct
from ftexplorer.data import Data

for game in ['BL2', 'TPS']:
    linkids = {}
    data = Data(game)
    bpd_names = []
    bpd_names.extend(data.get_all_by_type('BehaviorProviderDefinition'))
    bpd_names.extend(data.get_all_by_type('AIBehaviorProviderDefinition'))
    for bpd_name in sorted(bpd_names):
        bpd = data.get_struct_by_full_object(bpd_name)
        for bs_idx, bs in enumerate(bpd['BehaviorSequences']):
            for cold_idx, cold in enumerate(bs['ConsolidatedOutputLinkData']):
                link = int(cold['LinkIdAndLinkedBehavior'])
                packed = struct.pack('>i', link)
                linkid = packed[0]
                if packed[1] != 0:
                    print('{} BehaviorSequences[{}].ConsolidatedOutputLinkData[{}] - {} second byte is: {}'.format(
                        bpd_name,
                        bs_idx,
                        cold_idx,
                        link,
                        packed[1],
                        ))
                if linkid == 255:
                    linkid = -1
                if linkid not in linkids:
                    linkids[linkid] = 1
                else:
                    linkids[linkid] += 1

    print('{} linkids:'.format(game))
    for linkid in sorted(linkids.keys()):
        print('  {}: {:,d}'.format(linkid, linkids[linkid]))
    print('')
