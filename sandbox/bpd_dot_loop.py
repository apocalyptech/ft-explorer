#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
import argparse
from ftexplorer.data import Data

data = Data('BL2')
cold_followed = set()

def compliment(number):
    """
    Returns a two's-compliment tuple for the given number.
    """
    number = int(number)
    one = (number >> 16)
    two = (number & 0xFF)
    return (one, two)

def follow(link, cold_data, behavior_data, coming_from, seq_idx, odf):
    """
    Follows the given `link` (being a two's-compliment number of the sort
    found in BPDs) through the given `behavior_data`, using `cold_data`
    as the glue.  `coming_from` is the source which we've been linked
    from.  `seq_idx` is our current BPD index
    """
    global cold_followed
    (link_index, link_length) = compliment(link)
    for (cold_order_idx, cold_index) in enumerate(range(link_index, link_index+link_length)):
        full_cold_index = '{}_{}'.format(seq_idx, cold_index)
        if full_cold_index in cold_followed:
            continue
        else:
            cold_followed.add(full_cold_index)
        try:
            cold = cold_data[cold_index]
        except IndexError:
            broken_id = 'broken_{}_{}'.format(seq_idx, cold_order_idx)
            print('  {} [label=<BROKEN>,style=filled,fillcolor=red];'.format(broken_id), file=odf)
            print('  {} -> {}'.format(coming_from, broken_id), file=odf)
            return
        (link_id, bindex) = compliment(cold['LinkIdAndLinkedBehavior'])
        behavior = behavior_data[bindex]
        going_to = 'behavior_{}_{}'.format(seq_idx, bindex)
        delay = round(float(cold['ActivateDelay']))
        if delay == 0:
            delay_extra = ''
        else:
            delay_extra = '<br/>d{}'.format(delay)
        print('  {} -> {} [taillabel=<{}<br/>[{}]{}>];'.format(coming_from, going_to, cold_order_idx, cold_index, delay_extra), file=odf)
        follow(behavior['OutputLinks']['ArrayIndexAndLength'],
            cold_data,
            behavior_data,
            going_to,
            seq_idx,
            odf,
            )

def get_var_list(number):
    global cvld_data
    global clv_data
    global variable_data
    (var_index, var_len) = compliment(number)
    var_list = []
    for cvld_idx in range(var_index, var_index+var_len):
        cvld = cvld_data[cvld_idx]
        var_name = cvld['PropertyName']
        var_type_full = cvld['VariableLinkType']
        (link_index, link_len) = compliment(cvld['LinkedVariables']['ArrayIndexAndLength'])
        # This is stupid because our ft-explorer parsing is stupid.  Doesn't really
        # handle lists of numbers too well.  We'll just pretend.
        clv_data_real = [int(p) for p in clv_data.split(',')]

        for link_index_iter in range(link_index, link_index+link_len):

            finalvar_idx = clv_data_real[link_index_iter]
            finalvar = variable_data[finalvar_idx]
            if finalvar['Name'] == '':
                finalvar_name = ''
            else:
                finalvar_name = finalvar['Name']
            if finalvar['Type'].startswith('BVAR_'):
                finalvar_type = finalvar['Type'][5:].lower()
            else:
                raise Exception('Unknown variable type: {}'.format(finalvar['Type']))

            finalvar_desc = '[{}]{}({}) via [{}]{}, [{}]'.format(
                    finalvar_idx,
                    finalvar_name.strip('"'),
                    finalvar_type,
                    cvld_idx,
                    var_name.strip('"'),
                    link_index_iter,
                    )

            if var_type_full == 'BVARLINK_Input':
                var_list.append('&lt;- {}'.format(finalvar_desc))
            elif var_type_full == 'BVARLINK_Output':
                var_list.append('-&gt; {}'.format(finalvar_desc))
            elif var_type_full == 'BVARLINK_Context':
                var_list.append('({})'.format(finalvar_desc))
            else:
                raise Exception('Unknown var type: {}'.format(var_type_full))

    return var_list

def get_var_extra(number):
    var_list = get_var_list(number)
    if len(var_list) > 0:
        return '<br/>{}'.format('<br/>'.join(var_list))
    else:
        return ''

objects = []
objects.extend(data.get_all_by_type('AIBehaviorProviderDefinition'))
objects.extend(data.get_all_by_type('BehaviorProviderDefinition'))

for bpd_name in objects:
    with open('bpds/{}.dot'.format(bpd_name), 'w') as odf:

        print('Processing {}'.format(bpd_name))
        bpd = data.get_node_by_full_object(bpd_name).get_structure()
        cold_followed = set()
        print('digraph bpd {', file=odf)
        print('', file=odf)
        print('  labelloc = "t";', file=odf)
        print('  fontsize = 25;', file=odf)
        print('  label = <{}>;'.format(bpd_name), file=odf)
        print('', file=odf)

        print('  {', file=odf)
        print('    node [style=filled,fillcolor=chartreuse2];', file=odf)
        for (seq_idx, seq) in enumerate(bpd['BehaviorSequences']):

            seq_name = seq['BehaviorSequenceName']
            event_data = seq['EventData2']
            behavior_data = seq['BehaviorData2']
            variable_data = seq['VariableData']
            cold_data = seq['ConsolidatedOutputLinkData']
            cvld_data = seq['ConsolidatedVariableLinkData']
            clv_data = seq['ConsolidatedLinkedVariables']

            for (event_idx, event) in enumerate(event_data):
                if event['UserData']['bEnabled'] == 'True':

                    var_extra = get_var_extra(event['OutputVariables']['ArrayIndexAndLength'])

                    print('    event_{}_{} [label=<[{}]{}.{}{}>];'.format(
                        seq_idx,
                        event_idx,
                        seq_idx,
                        seq_name.strip('"'),
                        event['UserData']['EventName'].strip('"'),
                        var_extra,
                        ), file=odf)

            print('', file=odf)

        print('  }', file=odf)
        print('', file=odf)

        for (seq_idx, seq) in enumerate(bpd['BehaviorSequences']):

            seq_name = seq['BehaviorSequenceName']
            event_data = seq['EventData2']
            behavior_data = seq['BehaviorData2']
            variable_data = seq['VariableData']
            cold_data = seq['ConsolidatedOutputLinkData']
            cvld_data = seq['ConsolidatedVariableLinkData']
            clv_data = seq['ConsolidatedLinkedVariables']

            for (behavior_idx, behavior) in enumerate(behavior_data):
                if behavior['Behavior'] != 'None':
                    (behavior_type, behavior_class, junk) = behavior['Behavior'].split("'", 2)
                    if behavior_class.lower().startswith(bpd_name.lower()):
                        behavior_class = behavior_class[len(bpd_name)+1:]
                else:
                    behavior_type = ''
                    behavior_class = 'None'

                var_extra = get_var_extra(behavior['LinkedVariables']['ArrayIndexAndLength'])

                print('  behavior_{}_{} [label=<[{}] {}{}>];'.format(
                    seq_idx,
                    behavior_idx,
                    behavior_idx,
                    behavior_class,
                    var_extra,
                    ), file=odf)
            print('', file=odf)

        for (seq_idx, seq) in enumerate(bpd['BehaviorSequences']):

            seq_name = seq['BehaviorSequenceName']
            event_data = seq['EventData2']
            behavior_data = seq['BehaviorData2']
            variable_data = seq['VariableData']
            cold_data = seq['ConsolidatedOutputLinkData']
            cvld_data = seq['ConsolidatedVariableLinkData']
            clv_data = seq['ConsolidatedLinkedVariables']

            for (event_idx, event) in enumerate(event_data):
                if event['UserData']['bEnabled'] == 'True':
                    follow(event['OutputLinks']['ArrayIndexAndLength'],
                            cold_data,
                            behavior_data,
                            'event_{}_{}'.format(seq_idx, event_idx),
                            seq_idx,
                            odf)

            print('', file=odf)

        print('', file=odf)
        print('}', file=odf)
