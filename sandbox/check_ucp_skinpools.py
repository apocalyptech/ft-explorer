#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import re
from ftexplorer.data import Data

patchfile = '/home/pez/git/b2patching/BLCMods/Borderlands 2 mods/Shadowevil/Patch.txt'
start_stop_str = "Skinpool Fixes (Don't uncheck this)"
extra_stop_str = 'VendorFix'

data = Data('BL2')
pool_cache = {}

from_values = {}
to_values = {}

freed_pools = set()

# One hard-coded pool which is freed up in a slightly different way than
# everything else
freed_pools.add('GD_ItemPools_Shop.WeaponPools.Shoppool_FeaturedItem_WeaponMachine_Skins')

with open(patchfile) as df:
    processing = False
    for line in df.readlines():
        if processing:
            if start_stop_str in line or extra_stop_str in line:
                processing = False
            else:
                line = line.strip()
                if line == '':
                    continue
                match = re.search('<value>",(.*?),BalancedItems\[(\d+)\]\.(.*),,(.*?)"', line)
                if match:
                    main_pool = match.group(1)
                    bal_idx = int(match.group(2))
                    var_changed = match.group(3)
                    changed_to = match.group(4)
                    if var_changed == 'ItmPoolDefinition' and changed_to == 'None':
                        if main_pool not in pool_cache:
                            pool_cache[main_pool] = data.get_node_by_full_object(main_pool).get_structure()
                        (junk, destination, junk2) = pool_cache[main_pool]['BalancedItems'][bal_idx]['ItmPoolDefinition'].split("'", 2)
                        freed_pools.add(destination)
                        if destination not in pool_cache:
                            pool_cache[destination] = data.get_node_by_full_object(destination).get_structure()
                        if len(pool_cache[destination]['BalancedItems']) > 1:
                            raise Exception('Pool {} has {} items'.format(destination, len(pool_cache[destination]['BalancedItems'])))
                        (junk, ultimate, junk2) = pool_cache[destination]['BalancedItems'][0]['InvBalanceDefinition'].split("'", 2)
                        from_values['{}_{}'.format(main_pool, bal_idx)] = ultimate
                    elif var_changed == 'InvBalanceDefinition' and 'InventoryBalanceDefinition' in changed_to:
                        (junk, new_inv, junk2) = changed_to.split("'", 2)
                        to_values['{}_{}'.format(main_pool, bal_idx)] = new_inv
                    else:
                        raise Exception('Unknown line found: {}'.format(line))
        else:
            if start_stop_str in line:
                processing = True

# Sanity checks
if len(from_values) != len(to_values):
    raise Exception('lengths differ: {} -> {}'.format(len(from_values), len(to_values)))
for key in from_values.keys():
    if key not in to_values:
        raise Exception('{} not found in destination dict'.format(key))
for key in from_values.keys():
    if from_values[key] != to_values[key]:
        raise Exception('Mismatch: {} -> {}'.format(from_values[key], to_values[key]))

# Now report
print('Freed pools:')
for pool in sorted(freed_pools):
    print(' * {}'.format(pool))
