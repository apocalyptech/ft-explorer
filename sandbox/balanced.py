#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

class Balanced(object):

    ids = {
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_0_VeryCommon'": 200,
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_1_Common'": 100,
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_2_Uncommon'": 10,
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_3_Uncommoner'": 5,
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_4_Rare'": 1,
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_5_VeryRare'": .1,
            "AttributeInitializationDefinition'GD_Balance.Weighting.Weight_6_Legendary'": .03,
        }

    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item_struct):
        if item_struct['ItmPoolDefinition'] != 'None':
            title = item_struct['ItmPoolDefinition'].split("'")[1]
        else:
            title = item_struct['InvBalanceDefinition'].split("'")[1]
        
        prob = item_struct['Probability']
        if prob['BaseValueAttribute'] != 'None':
            raise Exception('Cannot handle BVA at the moment')
        if prob['InitializationDefinition'] == 'None':
            bvc = round(float(prob['BaseValueConstant']), 6)
        else:
            if prob['InitializationDefinition'] in self.ids:
                bvc = self.ids[prob['InitializationDefinition']]
            else:
                raise Exception('Not found in known IDs: {}'.format(prob['InitializationDefinition']))
        bvsc = round(float(prob['BaseValueScaleConstant']), 6)
        weight = round(bvc*bvsc, 6)
        self.total += weight
        self.items.append((title, weight))

    def get_report(self):
        if self.total == 0:
            return ""
        ret_list = []
        for (title, weight) in self.items:
            prob = weight/self.total*100
            if prob >= 1:
                prob = round(prob)
            else:
                prob = round(prob, 2)
            ret_list.append("\t{}%: {}".format(prob, title))
        return "\n".join(ret_list)

data = Data('TPS')
with open('/home/pez/Programs/games/borderlands_tps/ucp/enemy_use.txt') as df:
    for line in df.readlines():
        if line[:3] == 'GD_':
            pool = line.strip()
            structure = data.get_node_by_full_object(pool).get_structure()
            bal = Balanced()
            for item in structure['BalancedItems']:
                bal.add_item(item)
            print(pool)
            print(bal.get_report())
            print('')
