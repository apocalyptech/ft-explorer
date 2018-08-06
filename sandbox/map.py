#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import re
import sys
import math
from ftexplorer.data import Data

data = Data('TPS')

# find all objects a certain distance from the given point
x = 10588
y = -1347
z = 3602
matchname = 'WillowPopulationOpportunityPoint'
distance = 4500

node = data.get_node_by_full_object('Moon_P.TheWorld:PersistentLevel')
for child in node.children.values():
    if child.name[:len(matchname)] == matchname:
        struct = child.get_structure()
        child_x = float(struct['Location']['X'])
        child_y = float(struct['Location']['Y'])
        child_z = float(struct['Location']['Z'])
        child_distance = math.sqrt((x-child_x)**2+(y-child_y)**2+(z-child_z)**2)
        if child_distance <= distance:
            print('{name} - {pd} ({x}, {y}, {z})'.format(
                name=child.name,
                pd=struct['PopulationDef'],
                x=child_x,
                y=child_y,
                z=child_z,
                ))
