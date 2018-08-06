#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

level_map = {
        'Ma_Nexus_': 'Ma_Nexus_P',
        'Ma_Motherboard_': 'Ma_Motherboard_P',
    }

data = Data('TPS')
points = data.get_all_by_type('PopulationOpportunityPoint')
for point_name in points:
    point = data.get_struct_by_full_object(point_name)
    popdef = Data.get_struct_attr_obj(point, 'PopulationDef')
    if popdef:
        if popdef == 'GD_Ma_AdPopup.Pop_AdPopup_Wide' or popdef == 'GD_Ma_AdPopup.Pop_AdPopup_Tall':
            printed = False
            for (key, val) in level_map.items():
                if point_name.startswith(key):
                    print('level {} set {} PopulationDef '.format(val, point_name))
                    print('')
                    printed = True
            if not printed:
                raise Exception('Unknown level: {}'.format(point_name))
