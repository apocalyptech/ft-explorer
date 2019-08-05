#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

data = Data('BL2')
for gbdef in data.get_all_by_type('GameBalanceDefinition'):
    gb = data.get_struct_by_full_object(gbdef)
    if 'BalanceByRegion' in gb:
        for (balidx, bal) in enumerate(gb['BalanceByRegion']):
            print('set {} BalanceByRegion[{}].MaxDefaultGameStage.BaseValueConstant 80'.format(
                gbdef, balidx,
                ))
            if 'MissionOverrides' in bal and bal['MissionOverrides'] is not None and bal['MissionOverrides'] != '' and bal['MissionOverrides'] != 'None':
                for (overidx, over) in enumerate(bal['MissionOverrides']):
                    print('set {} BalanceByRegion[{}].MissionOverrides[{}].MaxGameStage.BaseValueConstant 80'.format(
                        gbdef, balidx, overidx,
                        ))
