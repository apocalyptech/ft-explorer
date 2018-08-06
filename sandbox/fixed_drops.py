#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Find AIPawnBalanceDefinitions which use fixed probabilities for their
# Runnables drops.

from ftexplorer.data import Data
data = Data('BL2')

def is_fixed(prob):
    """
    Returns True of the probability stanza is fixed in a way
    we don't like
    """
    if prob['BaseValueAttribute'] != 'None' or prob['InitializationDefinition'] != 'None':
        return False
    bvc = round(float(prob['BaseValueConstant']), 6)
    bvsc = round(float(prob['BaseValueScaleConstant']), 6)
    if bvc == 1.0 and bvsc == 1.0:
        return False
    elif bvc == 0.0 or bvsc == 0.0:
        return False
    return True

def investigate_pool(pool, report):
    """
    Looks into a pool to see if we should report it.
    """
    if (pool['ItemPool'] != 'None' and
            'AmmoAndResourcePools' not in pool['ItemPool'] and
            'EnemyUse' not in pool['ItemPool'] and
            'Pool_GunsAndGear_Weighted' not in pool['ItemPool'] and
            'ItemPool_MoxxiPicture' not in pool['ItemPool'] and
            'Pool_GrenadeMods_All' not in pool['ItemPool'] and
            'GD_CustomItemPools' not in pool['ItemPool'] and
            'Pool_SpellGrenade' not in pool['ItemPool'] and
            'Pool_Shields_All_01_Common' not in pool['ItemPool']
            ):
        prob = pool['PoolProbability']
        if is_fixed(prob):
            print(report)

for classname in data.get_all_by_type('AIPawnBalanceDefinition'):
    pawn = data.get_node_by_full_object(classname).get_structure()
    if 'DefaultItemPoolList' in pawn:
        for (dipl, pool) in enumerate(pawn['DefaultItemPoolList']):
            investigate_pool(pool, '{} DefaultItemPoolList[{}]'.format(classname, dipl))
    if 'PlayThroughs' in pawn:
        for (pt_idx, pt) in enumerate(pawn['PlayThroughs']):
            if ('CustomItemPoolList' in pt and
                    pt['CustomItemPoolList'] is not None and
                    pt['CustomItemPoolList'] != ''):
                for (cipl, pool) in enumerate(pt['CustomItemPoolList']):
                    investigate_pool(pool, '{} PlayThroughs[{}].CustomItemPoolList[{}]'.format(classname, pt_idx, cipl))
