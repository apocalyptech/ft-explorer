#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data, Weight

data = Data('TPS')
levels = [
        ('Cortex', 'Ma_SubBoss_P'),
    ]

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

    print('{} ({})'.format(level_label, level_name))
    print('')

    # Loop through popdefs to get a list of all pawnbalances which can spawn
    for popdef in sorted(popdefs):
        print(' * {}'.format(popdef))
        for pawnbalance in get_spawns_from_popdef(popdef, data):
            print('   - {}'.format(pawnbalance))
        print('')
