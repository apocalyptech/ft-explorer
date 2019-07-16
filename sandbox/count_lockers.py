#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:


import sys
from ftexplorer.data import Data

data = Data('BL2')

locker_count = 0
for (name, node) in data.get_level_package_nodes('GaiusSanctuary_P'):
    for point in node.get_children_with_name('willowpopulationopportunitypoint'):
        point_struct = point.get_structure()
        if 'Locker' in point_struct['PopulationDef']:
            locker_count += 1
            print('{}.{}'.format(name, point))
print('--')
print('Locker count: {}'.format(locker_count))
