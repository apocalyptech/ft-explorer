#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

data = Data('TPS')
bpd_name = 'GD_DahlFanatic.Character.AIDef_DahlFanatic:AIBehaviorProviderDefinition_0'

def compliment(number):
    """
    Returns a two's-compliment tuple for the given number.
    """
    number = int(number)
    one = (number >> 16)
    two = (number & 0xFF)
    return (one, two)

def follow(link, cold_data, behavior_data, prefix=''):
    (link_index, link_length) = compliment(link)
    print('{}Links at {}, length {}'.format(prefix, link_index, link_length))
    for cold_index in range(link_index, link_index+link_length):
        cold = cold_data[cold_index]
        (link_id, bindex) = compliment(cold['LinkIdAndLinkedBehavior'])
        behavior = behavior_data[bindex]
        print('{}* (delay {}) Behavior {}: {}'.format(
            prefix,
            round(float(cold['ActivateDelay'])),
            bindex,
            behavior['Behavior']))
        follow(behavior['OutputLinks']['ArrayIndexAndLength'],
            cold_data,
            behavior_data,
            prefix='{}  '.format(prefix))

bpd = data.get_node_by_full_object(bpd_name).get_structure()
seq0 = bpd['BehaviorSequences'][0]

event_data = seq0['EventData2']
behavior_data = seq0['BehaviorData2']
variable_data = seq0['VariableData']
cold_data = seq0['ConsolidatedOutputLinkData']
var_data = seq0['ConsolidatedVariableLinkData']
link_data = seq0['ConsolidatedLinkedVariables']

for event in event_data:
    if event['UserData']['bEnabled'] == 'True':
        print('Event {}:'.format(event['UserData']['EventName']))
        follow(event['OutputLinks']['ArrayIndexAndLength'], cold_data, behavior_data, prefix='  ')
        print('')
