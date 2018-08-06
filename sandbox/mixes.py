#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data, Weight

# Looks for certain pawnbalances inside a list of popdefs.  Yay.

data = Data('BL2')
popdefs = [
        'GD_Population_Bandit.Population.PopDef_BanditMix_Glacial',
        'GD_Population_Marauder.Population.PopDef_Boom',
        'GD_Population_Marauder.Population.PopDef_BoomBoom',
        'GD_Population_Marauder.Population.PopDef_MarauderBadass',
        'GD_Population_Marauder.Population.PopDef_MarauderIntro',
        'GD_Population_Marauder.Population.PopDef_MarauderMix_Regular',
        'GD_Population_Nomad.Population.Unique.PopDef_Flynt',
        'GD_Population_Psycho.Population.PopDef_Psycho',
        'GD_Population_Psycho.Population.PopDef_PsychoBurning',
        'GD_Population_Psycho.Population.PopDef_PsychoSuicide',
    ]
pawns = set([
    'GD_Population_Marauder.Balance.PawnBalance_MarauderElite',
    'GD_Population_Marauder.Balance.PawnBalance_MarauderRegular',
    'GD_Population_Marauder.Balance.PawnBalance_Scavenger',
    'GD_Population_Midget.Balance.PawnBalance_MidgetShotgun'
    ])

commands = []
for popdef_name in popdefs:

    reported = False
    popdef = data.get_struct_by_full_object(popdef_name)
    for (archetype_idx, archetype) in enumerate(popdef['ActorArchetypeList']):
        prob = Weight(archetype['Probability'])
        if prob.value > 0:
            factory_name = Data.get_struct_attr_obj(archetype, 'SpawnFactory')
            factory = data.get_struct_by_full_object(factory_name)
            pawn_name = Data.get_struct_attr_obj(factory, 'PawnBalanceDefinition')
            if pawn_name in pawns:
                if not reported:
                    print(popdef_name)
                    reported = True
                print(' * [{}] {} @ {}'.format(archetype_idx, pawn_name, prob.value))
                commands.append("""set {} ActorArchetypeList[{}].Probability
                    (
                        BaseValueConstant=200000, 
                        BaseValueAttribute=None, 
                        InitializationDefinition=None, 
                        BaseValueScaleConstant=1 
                    )""".format(popdef_name, archetype_idx))

    if reported:
        print('')

for command in commands:
    print(command)
    print('')
