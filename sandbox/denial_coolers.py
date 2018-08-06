#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Attempting to find some pattern to the bandit coolers near the
# Denial Subroutine battle which don't actually work.

import sys
from ftexplorer.data import Data, Weight

data = Data('TPS')
cooler_points = []
points = data.get_all_by_type('WillowPopulationOpportunityPoint')
for point_name in sorted(points):
    if point_name.startswith('Ma_RightCluster_Combat.TheWorld:PersistentLevel'):
        point = data.get_struct_by_full_object(point_name)
        popdef_name = Data.get_struct_attr_obj(point, 'PopulationDef')
        if popdef_name and popdef_name == 'GD_Population_Treasure.Lootables.BanditCooler':
            cooler_points.append(point)
            if point['PhysicsVolume'] == "BehaviorVolume'Ma_RightCluster_Combat.TheWorld:PersistentLevel.BehaviorVolume_6'":
                #print("set {} PhysicsVolume DefaultPhysicsVolume'Loader.TheWorld:PersistentLevel.DefaultPhysicsVolume_2'".format(point_name))
                print("set {} PopulationDef PopulationDefinition'GD_Ma_Population_Treasure.Lootables.BanditAmmo_Marigold'".format(point_name))

print('Found {} coolers'.format(len(cooler_points)))
print('')
keys = {}
for point in cooler_points:
    for key in point.keys():
        if type(point[key]) == str:
            if key not in keys:
                keys[key] = {}
            if point[key] not in keys[key]:
                keys[key][point[key]] = 0
            keys[key][point[key]] += 1

for key in sorted(keys.keys()):
    values = keys[key]
    if len(values) > 1:
        print(key)
        for (value, count) in values.items():
            print(' * {}: {}'.format(value, count))
        print('')
