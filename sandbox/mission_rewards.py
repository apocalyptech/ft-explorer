#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

data = Data('TPS')

def report(label, var):
    if var and var != '':
        if ',' in var:
            items = var.split(',')
        else:
            items = [var]
        for item in items:
            print('  {}: {}'.format(label, Data.get_attr_obj(item)))


for mission_class in data.get_all_by_type('MissionDefinition'):
    mission = data.get_struct_by_full_object(mission_class)
    reward = mission['Reward']
    alt = mission['AlternativeReward']
    print('{} ({}):'.format(mission['MissionName'], mission_class))
    report('Main Item', reward['RewardItems'])
    report('Main Pool', reward['RewardItemPools'])
    report('Alt Item', alt['RewardItems'])
    report('Alt Pool', alt['RewardItemPools'])
    print('')

