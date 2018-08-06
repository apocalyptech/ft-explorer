#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

print("""
This doesn't actually work, btw.  As far as I can tell, it *should*
work, but no such luck.  My theory is that all the vehicle-blocking
stuff gets computed before the hotfix gets fired, so even though
the parameter looks updated with an `obj dump`, it doesn't actually
have an effect.  Just a theory, though.  Anyway, a command to diable
ALL blocking meshes, which actually works, is:

set Engine.BlockingMeshComponent bIsDisabled True

""")

data = Data('TPS')
levelname = 'Deadsurface_P'

print('Level hotfixes in {}'.format(levelname))
for (nodename, node) in data.get_level_package_nodes(levelname):
    for child in node.get_children_with_name('blockingmeshactor'):
        for meshchild in child.children.values():
            full_obj = '{}.{}.{}'.format(nodename, child.name, meshchild.name)
            structure = meshchild.get_structure()
            if 'ScalarParameterValues' in structure:
                block_player = False
                block_vehicle = False
                vehicle_idx = -1
                for (idx, param_value) in enumerate(structure['ScalarParameterValues']):
                    if param_value['ParameterName'] == '"Players"':
                        if round(float(param_value['ParameterValue'])) == 1:
                            block_player = True
                    elif param_value['ParameterName'] == '"PlayerVehicles"':
                        vehicle_idx = idx
                        if round(float(param_value['ParameterValue'])) == 1:
                            block_vehicle = True
                if block_vehicle and not block_player and vehicle_idx != -1:
                    full_obj = '{}.{}.{}'.format(nodename, child.name, meshchild.name)
                    print('  set {} ScalarParameterValues[{}].ParameterValue 0'.format(full_obj, vehicle_idx))
print('')
