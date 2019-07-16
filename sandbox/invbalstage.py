#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:


import sys
from ftexplorer.data import Data

data = Data('BL2')
baldef_names = data.get_all_by_type('InventoryBalanceDefinition') + \
        data.get_all_by_type('WeaponBalanceDefinition')

for baldef_name in sorted(baldef_names):
    baldef = data.get_struct_by_full_object(baldef_name)
    if ('Manufacturers' in baldef and
            baldef['Manufacturers'] is not None and
            baldef['Manufacturers'] != ''):
        for (man_idx, man) in enumerate(baldef['Manufacturers']):
            if ('Grades' in man and
                    man['Grades'] is not None and
                    man['Grades'] != ''):
                for (grade_idx, grade) in enumerate(man['Grades']):
                    if ('GameStageRequirement' in grade and
                            grade['GameStageRequirement'] is not None and
                            grade['GameStageRequirement'] != ''):
                        req = grade['GameStageRequirement']
                        min_stage = req['MinGameStage']
                        if int(min_stage) > 1:
                            print('set {} Manufacturers[{}].Grades[{}].GameStageRequirement.MinGameStage 1'.format(
                                baldef_name,
                                man_idx,
                                grade_idx,
                                ))
