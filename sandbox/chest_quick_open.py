#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

def get_twos_compliment(val):
    val = int(val)
    one = val >> 16
    two = val & 0xFF
    return (one, two)

data = Data('BL2')
for obj_name in sorted(data.get_all_by_type('InteractiveObjectDefinition')):
    obj_struct = data.get_struct_by_full_object(obj_name)
    bpd_name = Data.get_struct_attr_obj(obj_struct, 'BehaviorProviderDefinition')
    shown_title = False
    if bpd_name:
        bpd_node = data.get_node_by_full_object(bpd_name)

        # Remove any delay if we have an immediate AttachItems behavior after
        # an Event.  This may or may not catch everything.
        bpd_struct = bpd_node.get_structure()
        for (seq_idx, seq) in enumerate(bpd_struct['BehaviorSequences']):
            for event in seq['EventData2']:
                (start_idx, count) = get_twos_compliment(event['OutputLinks']['ArrayIndexAndLength'])
                for cold_idx in range(start_idx, start_idx+count):
                    cold = seq['ConsolidatedOutputLinkData'][cold_idx]
                    if cold['ActivateDelay'] != '0.000000':
                        ad = float(cold['ActivateDelay'])
                        (link_id, behavior_idx) = get_twos_compliment(cold['LinkIdAndLinkedBehavior'])
                        behavior = seq['BehaviorData2'][int(behavior_idx)]
                        if 'AttachItems' in behavior['Behavior']:
                            if not shown_title:
                                print(obj_name)
                                shown_title = True
                            print('set {} BehaviorSequences[{}].ConsolidatedOutputLinkData[{}].ActivateDelay {:0.6f}'.format(
                                bpd_name,
                                seq_idx,
                                cold_idx,
                                ad/5.0,
                                ))

        # Output a statement to ensure that attached items are immediately
        # available
        for child in bpd_node.get_children_with_name('behavior_attachitems'):
            child_struct = child.get_structure()
            if child_struct['bDisablePickups'] == 'True':
                if not shown_title:
                    print(obj_name)
                    shown_title = True
                print('set {}.{} bDisablePickups False'.format(bpd_name, child.name))

        # Get a list of animation trees which are in use by the container
        trees = set()
        for child in bpd_node.get_children_with_name('behavior_simpleanimplay'):
            child_struct = child.get_structure()
            trees.add(Data.get_struct_attr_obj(child_struct, 'Tree'))
        for tree in trees:
            if not shown_title:
                print(obj_name)
                shown_title = True
            print(tree)
        if shown_title:
            print('')

