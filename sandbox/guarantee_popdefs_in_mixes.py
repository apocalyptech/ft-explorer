#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

data = Data('BL2')

# Given the specified popdefs, make them practically guaranteed in
# any mix that they happen to belong to.
popdef_names = set([
        #'GD_Population_Engineer.Balance.PawnBalance_HyperionHawk',
        #'GD_Population_Midget.Balance.PawnBalance_MidgetRat',
        #'GD_Allium_PsychoSnow_Midget.Balance.PawnBalance_PsychoSnow_Midget',
        #'GD_Population_Marauder.Balance.PawnBalance_MarauderGrunt',
        #'GD_Population_Marauder.Balance.PawnBalance_MarauderIntro',
        #'GD_Population_Midget.Balance.PawnBalance_MidgetShotgun',
        #'GD_Population_Nomad.Balance.PawnBalance_NomadPyro',
        #'GD_Aster_Pop_Knights.Balance.PawnBalance_Knight_Paladin',
        'GD_Population_SpiderAnt.Balance.PawnBalance_SpiderantChubby',
        #'GD_Population_PrimalBeast.Population.Unique.PopDef_PrimalBeast_KingMong',
    ])

wpd_cache = {}
for pfbap_name in data.get_all_by_type('PopulationFactoryBalancedAIPawn'):
    pfbap = data.get_struct_by_full_object(pfbap_name)
    pawn_name = Data.get_struct_attr_obj(pfbap, 'PawnBalanceDefinition')
    if pawn_name in popdef_names:
        (mix_name, junk) = pfbap_name.split(':', 1)
        if mix_name not in wpd_cache:
            wpd_cache[mix_name] = data.get_struct_by_full_object(mix_name)
        for (aal_idx, aal) in enumerate(wpd_cache[mix_name]['ActorArchetypeList']):
            sf_name = Data.get_struct_attr_obj(aal, 'SpawnFactory')
            if sf_name == pfbap_name:
                print('set {} ActorArchetypeList[{}].Probability (BaseValueConstant=200000,BaseValueAttribute=None,InitializationDefinition=None,BaseValueScaleConstant=1)'.format(
                    mix_name, aal_idx
                    ))
