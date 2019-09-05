#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

# Finding all AttributeStartingValues attributes in use by game pawns.

asvs = set()

def get_asvs(obj, asvs):
    if 'AttributeStartingValues' in obj and obj['AttributeStartingValues'] != '' and obj['AttributeStartingValues'] != 'None':
        for asv in obj['AttributeStartingValues']:
            asv_val = Data.get_struct_attr_obj(asv, 'Attribute')
            if asv_val is not None:
                asvs.add(asv_val)

data = Data('TPS')
for classdef_name in data.get_all_by_type('AIClassDefinition'):
    get_asvs(data.get_struct_by_full_object(classdef_name), asvs)
for pawnbal_name in data.get_all_by_type('AIPawnBalanceDefinition'):
    pawnbal = data.get_struct_by_full_object(pawnbal_name)
    if 'PlayThroughs' in pawnbal and pawnbal['PlayThroughs'] != '' and pawnbal['PlayThroughs'] != 'None':
        for pt in pawnbal['PlayThroughs']:
            get_asvs(pt, asvs)

print('ASVs found:')
print('')
for asv in sorted(asvs):
    print(asv)
print('')
