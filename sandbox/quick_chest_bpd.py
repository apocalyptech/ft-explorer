#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

faster = 5

if len(sys.argv) < 2:
    print('Need at least one BPD name')
    sys.exit(1)

data = Data('BL2')
for bpd_name in sys.argv[1:]:
    bpd = data.get_struct_by_full_object(bpd_name)
    for bs_idx, seq in enumerate(bpd['BehaviorSequences']):
        for cold_idx, cold in enumerate(seq['ConsolidatedOutputLinkData']):
            delay = float(cold['ActivateDelay'])
            if delay != 0:
                print('set {} BehaviorSequences[{}].ConsolidatedOutputLinkData[{}].ActivateDelay {}'.format(
                    bpd_name,
                    bs_idx,
                    cold_idx,
                    round(delay / 5, 3),
                    ))

