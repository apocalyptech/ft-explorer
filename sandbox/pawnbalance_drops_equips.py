#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# This util loops through all AIPawnBalanceDefinitions and dumps out
# a list of what loot/equip pools are used by which of those definitions.
# Basically intended to be pruned manually, edited, and then passed
# to cdh.py to generate replacement data for Cold Dead Hands.  Was not
# used until updating BL2 CDH for DLC5...

import sys
from ftexplorer.data import Data

pools = {}

data = Data('BL2')
for baldef_name in data.get_all_by_type('AIPawnBalanceDefinition'):
    baldef = data.get_struct_by_full_object(baldef_name)

    if 'PlayThroughs' in baldef and baldef['PlayThroughs'] != 'None' and baldef['PlayThroughs'] != '':
        for pt in baldef['PlayThroughs']:
            if 'CustomItemPoolList' in pt and pt['CustomItemPoolList'] != 'None' and pt['CustomItemPoolList'] != '':
                for pool in pt['CustomItemPoolList']:
                    pool_name = Data.get_attr_obj(pool['ItemPool'])
                    if pool_name not in pools:
                        pools[pool_name] = set()
                    pools[pool_name].add(baldef_name)

    if 'DefaultItemPoolList' in baldef and baldef['DefaultItemPoolList'] != 'None' and baldef['DefaultItemPoolList'] != '':
        for pool in baldef['DefaultItemPoolList']:
            pool_name = Data.get_attr_obj(pool['ItemPool'])
            if pool_name not in pools:
                pools[pool_name] = set()
            pools[pool_name].add(baldef_name)

for pool_name, baldefs in sorted(pools.items()):
    print(pool_name)
    for baldef in sorted(baldefs):
        print('    {}'.format(baldef))
    print('')
