#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

# Given a popdef and a level, *only* spawn that popdef.

print("WARNING: This doesn't... work?  It should, as far as I can tell, but it doesn't.")
print("It *does* disable everything BUT the specified popdef, but the other mixes just")
print("generate no enemies at all.  Hrmph.")

data = Data('BL2')
popdef_name = 'GD_Population_Midget.Balance.PawnBalance_MidgetShotgun'
aidef_name = 'GD_AI_DenDef.AIDenDef_Bandits'
level_name = 'SouthernShelf_P'

mixes = set()
for (package_name, package) in data.get_level_package_nodes(level_name):
    for child in package:
        if child.name.startswith('PopulationOpportunityDen'):
            mix_name = Data.get_struct_attr_obj(child.get_structure(), 'PopulationDef')
            if mix_name:
                mixes.add(mix_name)

for mix_name in mixes:
    print("set {} AIDef WillowAIDenDefinition'{}'".format(mix_name, aidef_name))
    mix = data.get_struct_by_full_object(mix_name)
    for (aal_idx, aal) in enumerate(mix['ActorArchetypeList']):
        if aal_idx == 0:
            sf_name = Data.get_struct_attr_obj(aal, 'SpawnFactory')
            print("set {} PawnBalanceDefinition AIPawnBalanceDefinition'{}'".format(sf_name, popdef_name))
            print("set {} ActorArchetypeList[0].Probability (BaseValueConstant=1,BaseValueAttribute=None,InitializationDefinition=None,BaseValueScaleConstant=1)".format(mix_name))
        else:
            print("set {} ActorArchetypeList[{}].Probability (BaseValueConstant=0,BaseValueAttribute=None,InitializationDefinition=None,BaseValueScaleConstant=0)".format(mix_name, aal_idx))
