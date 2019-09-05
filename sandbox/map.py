#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import re
import sys
import math
from ftexplorer.data import Data

data = Data('BL2')

# find all objects a certain distance from the given point
level_package = 'Grass_Cliffs_P'
x = -17621
y = 990
z = 1555
distance = 600

def is_close(obj_x, obj_y, obj_z):
    global x
    global y
    global z
    global distance
    child_x = float(obj_x)
    child_y = float(obj_y)
    child_z = float(obj_z)
    child_distance = math.sqrt((x-child_x)**2+(y-child_y)**2+(z-child_z)**2)
    rv = child_distance <= distance
    return (rv, '({:0.1f}, {:0.1f}, {:0.1f}) @ {:0.1f}'.format(child_x, child_y, child_z, child_distance))

types = [
    ('WillowPopulationOpportunityPoint_', 'Location', 'PopulationDef'),
    ('PopulationOpportunityPoint_', 'Location', 'PopulationDef'),
    ('InterpActor_', 'Location', 'ReplicatedMesh'),
    ('WillowInteractiveObject_', 'Location', 'InteractiveObjectDefinition'),
    # Eh, nothing useful to report on this one.
    #('StaticMeshActor_', 'Location', 'foo'),
    ]

for (package_name, data_type) in data.get_level_package_nodes(level_package):
    node = data.get_node_by_full_object(package_name)
    for child in node.children.values():
        for (type_prefix, loc_attr, report_attr) in types:
            if child.name.startswith(type_prefix):
                struct = child.get_structure()
                if loc_attr in struct:
                    (match, suffix) = is_close(struct[loc_attr]['X'], struct[loc_attr]['Y'], struct[loc_attr]['Z'])
                    if match:
                        print('{prefix}.{name} - {report} {suffix}'.format(
                            prefix=package_name,
                            name=child.name,
                            report=struct[report_attr],
                            suffix=suffix,
                            ))
                        break
