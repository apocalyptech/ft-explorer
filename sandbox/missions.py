#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# TODO:
# To handle the tree properly, we'll have to actually *build* a tree and
# render the links once we have the full tree.  Should be fun.  The other
# component is knowing when maps open, because many of the missions have
# dependencies which don't give you the whole picture.  I suspect the best
# way to do this will be to loop through all LevelTravelStationDefinition
# objects (under GD_LevelTravelStations) -- there'll be pairs in there,
# which we can use to figure out when levels are open, though there may
# be some tricksiness for when a mission opens up multiple zones.  For
# TPS, I suspect we'll also have to loop through FastTravelStationDefinition
# objects (under GD_FastTravelStations).

import os
import sys
from ftexplorer.data import Data

def striptype(obj_name):
    (junk1, name, junk2) = obj_name.split("'", 2)
    return name

def dotnode(obj_name):
    name_parts = obj_name.split('.')
    return name_parts[-1].lower().replace('-', '_')

data = Data('BL2')
with open('b2missions.dot', 'w') as df:
    print('digraph b2 {', file=df)
    for mission_obj in data.get_all_by_type('MissionDefinition'):
        node = data.get_node_by_full_object(mission_obj)
        mission = node.get_structure()

        dot_name = dotnode(mission_obj)
        print('    {} [label=<{}>];'.format(dot_name, mission['MissionName']), file=df)

        print('{} ({})'.format(mission['MissionName'], mission_obj))
        if 'Dependencies' in mission:
            main_deps = set()
            for dep in mission['Dependencies']:
                print(' * {}'.format(dep))
                if dep[:17] != 'MissionDefinition':
                    raise Exception('Unknown mission dep type: {}'.format(dep))
                depname = striptype(dep)
                main_deps.add(depname)
                depname_dot = dotnode(depname)
                print('    {} -> {};'.format(depname_dot, dot_name), file=df)
                
                objdep = mission['ObjectiveDependency']
                if objdep['Objective'] != 'None':
                    objdep_name = striptype(objdep['Objective'])
                    (objdep_m, objdep_o) = objdep_name.split(':', 1)
                    if objdep_m in main_deps:
                        print(' * (ObjDep to {} again, ignoring)'.format(objdep_m))
                    else:
                        print(' * ObjDep: {} {}'.format(objdep['Objective'], objdep['Status']))
                        objdep_base_dot_name = dotnode(objdep_m)
                        objdep_dot_name = '{}_{}'.format(objdep_base_dot_name, objdep_o.lower())
                        dep_struct = data.get_node_by_full_object(objdep_m).get_structure()
                        obj_struct = data.get_node_by_full_object(objdep_name).get_structure()
                        print('    {} [label=<{}<br/><i>(through {})</i>>];'.format(
                            objdep_dot_name, dep_struct['MissionName'], obj_struct['ProgressMessage']),
                            file=df)
                        print('    {} -> {};'.format(objdep_base_dot_name, objdep_dot_name), file=df)
                        print('    {} -> {};'.format(objdep_dot_name, dot_name), file=df)
        print('')
    print('}', file=df)
