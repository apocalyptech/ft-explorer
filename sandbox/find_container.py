#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

if len(sys.argv) != 2:
    print('Specify a PopulationDefinition')
    sys.exit(0)

popdef = sys.argv[1]

# This would actually probably be quicker to do a getall on the object types
# and then glean the level from there...

data = Data('TPS')
for name, package in data.get_levels():
    found = False
    for node_name, node in data.get_level_package_nodes(package):
        points = []
        points.extend(node.get_children_with_name('populationopportunitypoint_'))
        points.extend(node.get_children_with_name('willowpopulationopportunitypoint_'))
        for child in points:
            child_struct = child.get_structure()
            if popdef in child_struct['PopulationDef']:
                print('Found in {} ({})'.format(name, package))
                found = True
                break
        if found:
            break
print('(done)')
