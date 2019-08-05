#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
import argparse
from ftexplorer.data import Data

data = Data('TPS')

for obj_name in data.get_all_by_type('WeaponNamePartDefinition'):
    obj = data.get_node_by_full_object(obj_name).get_structure()
    if 'PartName' not in obj or obj['PartName'] == '' or obj['PartName'] == 'None':
        print(obj_name)
