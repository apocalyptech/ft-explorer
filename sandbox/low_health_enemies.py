#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data, Weight

# Enemies with low health probably shouldn't use Turtle shields,
# because they can become unkillable.  Let's find out which ones
# might apply

def find_has_shields(poollist):
    if poollist is None or poollist == '':
        return (False, None)
    for pool in poollist:
        if 'Pool_Shields_Standard_EnemyUse' in pool['ItemPool']:
            shieldweight = Weight(pool['PoolProbability'])
            if shieldweight.value > 0:
                return (True, shieldweight.value)
    return (False, None)

data = Data('TPS')
for classname in data.get_all_by_type('AIPawnBalanceDefinition'):

    # Get BalDef
    baldef = data.get_struct_by_full_object(classname)
    try:
        pawn_name = baldef['PlayThroughs'][0]['DisplayName']
    except KeyError as e:
        #print('WARNING: No PlayThroughs for {}'.format(classname))
        pawn_name = '(unknown)'

    # Find out if this enemy has a chance to use shields
    has_shields = False
    shield_loc = None
    shield_prob = None
    has_cipl = False
    if ('PlayThroughs' in baldef and
            baldef['PlayThroughs'] is not None and
            baldef['PlayThroughs'] != ''):
        if (len(baldef['PlayThroughs']) > 0 and
                'CustomItemPoolList' in baldef['PlayThroughs'][0] and
                baldef['PlayThroughs'][0]['CustomItemPoolList'] is not None and
                baldef['PlayThroughs'][0]['CustomItemPoolList'] != ''):
            has_cipl = True
        (has_shields, shield_prob) = find_has_shields(baldef['PlayThroughs'][0]['CustomItemPoolList'])
        if has_shields:
            shield_loc = 'PlayThroughs[0]'
    if not has_shields and 'DefaultItemPoolList' in baldef:
        (has_shields, shield_prob) = find_has_shields(baldef['DefaultItemPoolList'])
        if has_shields:
            if has_cipl:
                shield_loc = 'DIPL (but CIPL clears?)'
            else:
                shield_loc = 'DIPL'
    
    # Don't bother processing if there's no shields
    if not has_shields:
        continue

    # Now dig down to see if we can find health modifiers
    archetype_name = Data.get_struct_attr_obj(baldef, 'AIPawnArchetype')
    if not archetype_name:
        print('WARNING: No archetype name for {} ({})'.format(pawn_name, classname))
        continue
    archetype = data.get_struct_by_full_object(archetype_name)
    aiclass_name = Data.get_struct_attr_obj(archetype, 'AIClass')
    if not aiclass_name:
        print('WARNING: No AIClass name for {}'.format(archetype_name))
        continue
    aiclass = data.get_struct_by_full_object(aiclass_name)
    health_modifier = None
    if ('AttributeStartingValues' in aiclass and
            aiclass['AttributeStartingValues'] != None and
            aiclass['AttributeStartingValues'] != ''):
        for value in aiclass['AttributeStartingValues']:
            if 'GD_Balance_HealthAndDamage.AIParameters.Attribute_HealthMultiplier' in value['Attribute']:
                if health_modifier is None:
                    health_modifier = Weight(value['BaseValue'])
                else:
                    print('WARNING: Overridden health value in {}'.format(aiclass_name))
    if health_modifier is not None:
        if health_modifier.value < 1:
            print('{} ({}): Health Modifier: {} (shield in {}, prob {})'.format(
                pawn_name, classname, health_modifier.value, shield_loc, shield_prob))

