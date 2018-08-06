#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data, Weight

# Looks up all the enemies in a list of maps and reports on whether or not
# they're set to use shields (and in which playthroughs they're set to use
# shidles).  Used when I was looking into early-game TPS shield usage, since
# very few enemies actually use shields in there, except for the very first
# level.

#data = Data('TPS')
#levels = [
#        ('Regolith Range', 'Deadsurface_P'),
#        ('Crisis Scar', 'ComFacility_P'),
#        ('Outlands Canyon', 'Outlands_P2'),
#        ('Triton Flats', 'Moon_P'),
#    ]
data = Data('BL2')
levels = [
        ('Southern Shelf', 'SouthernShelf_P'),
        #('Southern Shelf - Bay', 'Cove_P'),
    ]
shield_pool = 'GD_ItempoolsEnemyUse.Shields.Pool_Shields_Standard_EnemyUse'

popdef_cache = {}
def get_spawns_from_popdef(popdef_name, data):

    global popdef_cache
    if popdef_name in popdef_cache:
        return popdef_cache[popdef_name]

    popdef_set = set()
    popdef_struct = data.get_node_by_full_object(popdef_name).get_structure()
    for archetype in popdef_struct['ActorArchetypeList']:
        if archetype['SpawnFactory'] != 'None':
            spawnfactory_name = archetype['SpawnFactory'].split("'", 2)[1]
            sf_struct = data.get_node_by_full_object(spawnfactory_name).get_structure()
            if 'PawnBalanceDefinition' in sf_struct:
                if sf_struct['PawnBalanceDefinition'] != 'None':
                    popdef_set.add(sf_struct['PawnBalanceDefinition'].split("'", 2)[1])
            elif 'PopulationDef' in sf_struct:
                new_popdef_name = sf_struct['PopulationDef'].split("'", 2)[1]
                popdef_set = popdef_set.union(get_spawns_from_popdef(new_popdef_name, data))
            elif 'WillowAIPawnArchetype' in sf_struct:
                popdef_set.add(sf_struct['WillowAIPawnArchetype'].split("'", 2)[1])
            elif 'VehicleArchetype' in sf_struct:
                popdef_set.add(sf_struct['VehicleArchetype'].split("'", 2)[1])
            elif 'ObjectBalanceDefinition' in sf_struct:
                pass
            else:
                raise Exception('Not sure what to do: {}'.format(spawnfactory_name))

    popdef_cache[popdef_name] = popdef_set
    return popdef_set

pawnbalance_cache = {}

for (level_label, level_name) in levels:

    # Loop through level to get a list of all popdefs
    popdefs = set()
    for (nodename, node) in data.get_level_package_nodes(level_name):
        for child in node.get_children_with_name('populationopportunityden'):
            child_struct = child.get_structure()
            popdef = Data.get_struct_attr_obj(child_struct, 'PopulationDef')
            if popdef:
                popdefs.add(popdef)

    # Loop through popdefs to get a list of all pawnbalances which can spawn
    pawnbalances = set()
    for popdef in popdefs:
        for pawnbalance in get_spawns_from_popdef(popdef, data):
            pawnbalances.add(pawnbalance)

    print('{} ({})'.format(level_label, level_name))
    print('')
    same = []
    for pawnbalance in sorted(pawnbalances):
        if pawnbalance in pawnbalance_cache:
            same.append(pawnbalance)
        else:
            print(' * {}'.format(pawnbalance))
            pb_struct = data.get_node_by_full_object(pawnbalance).get_structure()
            pawnbalance_cache[pawnbalance] = pb_struct
            print_blank_line = False
            have_cipl_on_first = False
            if ('PlayThroughs' in pb_struct and
                    pb_struct['PlayThroughs'] != '' and
                    len(pb_struct['PlayThroughs']) > 0):
                for (pt_idx, pt) in enumerate(pb_struct['PlayThroughs']):
                    print_blank_line = True
                    if 'CustomItemPoolList' in pt and pt['CustomItemPoolList'] != '':
                        found_shield = False
                        if pt_idx == 0 and int(pt['PlayThrough']) == 1:
                            have_cipl_on_first = True
                        for (cipl_idx, cipl) in enumerate(pt['CustomItemPoolList']):
                            if shield_pool in cipl['ItemPool']:
                                found_shield = True
                                prob = Weight(cipl['PoolProbability'])
                                print('   Shield Chance at [{}]PlayThrough {}, CIPL {}: {:d}%'.format(
                                    pt_idx,
                                    pt['PlayThrough'],
                                    cipl_idx,
                                    round(prob.value*100),
                                    ))
                                break
                        if not found_shield:
                            print('   No Shield on [{}]PlayThrough {}'.format(
                                pt_idx,
                                pt['PlayThrough'],
                                ))
                    else:
                        print('   No CIPL to override on [{}]PlayThrough {}'.format(
                            pt_idx,
                            pt['PlayThrough'],
                            ))

            if not have_cipl_on_first:
                print_blank_line = True
                if ('DefaultItemPoolList' in pb_struct and
                        pb_struct['DefaultItemPoolList'] != '' and
                        len(pb_struct['DefaultItemPoolList']) > 0):
                    found_shield = False
                    for (dipl_idx, dipl) in enumerate(pb_struct['DefaultItemPoolList']):
                        if shield_pool in dipl['ItemPool']:
                            found_shield = True
                            prob = Weight(dipl['PoolProbability'])
                            print('   Shield Chance at DIPL {}: {:d}%'.format(dipl_idx, round(prob.value*100)))
                            break
                    if not found_shield:
                        print('   No Shield!')
                else:
                    print('   No DIPL to define gear')

            if print_blank_line:
                print('')

    if len(same) > 0:
        print(' * Same as from previous levels:')
        for pawnbalance in same:
            print('   * {}'.format(pawnbalance))
        print('')
