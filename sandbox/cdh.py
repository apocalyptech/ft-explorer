#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import re
import sys
from ftexplorer.data import Data

# Pools we're using
#data = Data('TPS')
#pools = [
#        ('Shields', 'shield'),
#        ('All Weapons', 'all'),
#        ('AR-Weighted', 'ar'),
#        ('Launchers Only', 'launcher'),
#        ('Shotguns Only', 'shotgun'),
#        ('Snipers Only', 'sniper'),
#        ('Lasers Only', 'laser_only'),
#        ('Laser-Weighted', 'laser'),
#    ]
data = Data('BL2')
pools = [
        ('AR-Weighted', 'ar'),
        ('Pistol-Weighted', 'pistols'),
        ('Shotgun-Weighted', 'shotguns'),
        ('SMG-Weighted', 'smg'),
        ('All Weapons', 'all'),
        ('Launchers Only', 'launchers'),
        ('Snipers Only', 'snipers'),
        ('Shotguns Only', 'only_shotguns'),
        ('ARs Only', 'only_ar'),
        ('Shields', 'shields'),
    ]

# Read in categories
categories = {}
#filename = '/home/pez/Programs/games/borderlands_tps/ucp/enemy_use.txt'
#filename = '/home/pez/Programs/games/borderlands_tps/ucp/enemy_use_dahl.txt'
#filename = '/home/pez/Programs/games/borderlands_tps/ucp/enemy_use_shields_guardians.txt'
#filename = '/home/pez/Programs/games/borderlands_tps/ucp/enemy_use_shields_claptrap.txt'
#filename = '/home/pez/Programs/games/borderlands_tps/ucp/enemy_use_shields_stalkers.txt'
#filename = '/home/pez/Programs/games/borderlands_2/ucp/enemy_use_dlc5.txt'
filename = '/home/pez/Programs/games/borderlands_2/ucp/enemy_use_dlc5_take2.txt'
with open(filename) as df:
    while True:
        category = df.readline().strip()
        if category == '':
            break
        orig_pools = set()
        to_change = []
        line = df.readline()
        while line.strip() != '':
            if line[:3] == 'GD_':
                # Adding quotes so we don't inadvertantly match on substrings
                orig_pools.add("'{}'".format(line.strip()))
            else:
                to_change.append(line.strip())
            line = df.readline()
        categories[category] = (orig_pools, to_change)

dipl_count = 0
pt_cipl_count = 0
level_ipl_count = 0
dl_ia_count = 0
nipl_count = 0

for weight in ['regular', 'badass']:

    print('###')
    print('### {} Definitions'.format(weight))
    print('###')
    print('')

    # Set up data-gathering structures
    dipl = {}
    pt_cipl = {}
    level_ipl = {}
    dl_ia = {}
    nipl = {}
    for (label, pool) in pools:
        dipl[pool] = []
        pt_cipl[pool] = []
        level_ipl[pool] = []
        dl_ia[pool] = []
        nipl[pool] = []

    # Now loop through and find out what we need to find out
    for (label, pool) in pools:
        full_cat = '{}_{}'.format(pool, weight)
        if full_cat in categories:
            (orig_pools, to_change) = categories[full_cat]
            for object_name in to_change:

                node = data.get_node_by_full_object(object_name)
                parsed = node.get_structure()

                found = False

                if 'DefaultItemPoolList' in parsed:
                    for (dipl_idx, pool_list) in enumerate(parsed['DefaultItemPoolList']):
                        if 'ItemPool' in pool_list:
                            for check_pool in orig_pools:
                                if check_pool in pool_list['ItemPool']:
                                    dipl[pool].append((dipl_idx, object_name))
                                    dipl_count += 1
                                    found = True
                                    break

                if 'NewItemPoolList' in parsed:
                    for (nipl_idx, pool_list) in enumerate(parsed['NewItemPoolList']):
                        if 'ItemPool' in pool_list:
                            for check_pool in orig_pools:
                                if check_pool in pool_list['ItemPool']:
                                    nipl[pool].append((nipl_idx, object_name))
                                    nipl_count += 1
                                    found = True
                                    break

                if 'ItemPoolList' in parsed:
                    for (ipl_idx, pool_list) in enumerate(parsed['ItemPoolList']):
                        if 'ItemPool' in pool_list:
                            for check_pool in orig_pools:
                                if check_pool in pool_list['ItemPool']:
                                    parts = object_name.split('.')
                                    level_ipl[pool].append((parts[0], ipl_idx, object_name, parsed['AIClass']))
                                    level_ipl_count += 1
                                    found = True
                                    break

                if 'PlayThroughs' in parsed:
                    for (pt_idx, pt) in enumerate(parsed['PlayThroughs']):
                        if 'CustomItemPoolList' in pt:
                            for (cipl_idx, cipl) in enumerate(pt['CustomItemPoolList']):
                                if 'ItemPool' in cipl:
                                    for check_pool in orig_pools:
                                        if check_pool in cipl['ItemPool']:
                                            pt_cipl[pool].append((pt_idx, cipl_idx, object_name))
                                            pt_cipl_count += 1
                                            found = True
                                            break

                if 'DefaultLoot' in parsed:
                    for (dl_idx, dl) in enumerate(parsed['DefaultLoot']):
                        if 'ItemAttachments' in dl:
                            for (ia_idx, ia) in enumerate(pt['ItemAttachments']):
                                if 'ItemPool' in ia:
                                    for check_pool in orig_pools:
                                        if check_pool in ia['ItemPool']:
                                            dl_ia[pool].append((dl_idx, ia_idx, object_name))
                                            dl_ia_count += 1
                                            found = True
                                            break

                if not found:
                    print('WARNING: {} was not found'.format(object_name))

    print('    enemy_dipl = (')
    for (label, pool) in pools:
        full_cat = '{}_{}'.format(pool, weight)
        print('            # {}'.format(label))
        print('            [')
        for (dipl_idx, name) in dipl[pool]:
            print('                ({}, \'{}\'),'.format(dipl_idx, name))
        print('            ],')
    print('        )')
    print('')

    print('    enemy_pt_cipl = (')
    for (label, pool) in pools:
        full_cat = '{}_{}'.format(pool, weight)
        print('            # {}'.format(label))
        print('            [')
        for (pt_idx, cipl_idx, name) in pt_cipl[pool]:
            print('                ({}, {}, \'{}\'),'.format(pt_idx, cipl_idx, name))
        print('            ],')
    print('        )')
    print('')

    print('    enemy_level_ipl = (')
    for (label, pool) in pools:
        full_cat = '{}_{}'.format(pool, weight)
        print('            # {}'.format(label))
        print('            [')
        for (level, ipl_idx, name, aiclass) in level_ipl[pool]:
            print('                (\'{}\', {}, \'{}\'), # {}'.format(level, ipl_idx, name, aiclass))
        print('            ],')
    print('        )')
    print('')

    print('    enemy_dl_ia = (')
    for (label, pool) in pools:
        full_cat = '{}_{}'.format(pool, weight)
        print('            # {}'.format(label))
        print('            [')
        for (dl_idx, ia_idx, name) in dl_ia[pool]:
            print('                ({}, \'{}\'),'.format(dl_idx, ia_idx, name))
        print('            ],')
    print('        )')
    print('')

    print('    enemy_nipl = (')
    for (label, pool) in pools:
        full_cat = '{}_{}'.format(pool, weight)
        print('            # {}'.format(label))
        print('            [')
        for (nipl_idx, name) in nipl[pool]:
            print('                ({}, \'{}\'),'.format(nipl_idx, name))
        print('            ],')
    print('        )')
    print('')

print('# dipl_count: {}'.format(dipl_count))
print('# pt_cipl_count: {}'.format(pt_cipl_count))
print('# level_ipl_count: {}'.format(level_ipl_count))
print('# dl_ia_count: {}'.format(dl_ia_count))
print('# nipl_count: {}'.format(nipl_count))
