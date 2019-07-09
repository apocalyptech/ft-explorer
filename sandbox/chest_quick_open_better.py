#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# A better version of this...
#
# Requires data from AnimNodeSequence, WillowAnimNode_Simple, and WillowAnimTree,
# which is not part of the default ft-explorer set.

from ftexplorer.data import Data

def get_twos_compliment(val):
    val = int(val)
    one = val >> 16
    two = val & 0xFF
    return (one, two)

found_trees = set()
bpd_stmts = []
disable_stmts = []

data = Data('BL2')
for obj_name in sorted(data.get_all_by_type('InteractiveObjectDefinition')):
    obj_struct = data.get_struct_by_full_object(obj_name)
    bpd_name = Data.get_struct_attr_obj(obj_struct, 'BehaviorProviderDefinition')
    if bpd_name:
        bpd_node = data.get_node_by_full_object(bpd_name)

        # Remove any delay if we have an immediate AttachItems behavior after
        # an Event.  This may or may not catch everything.
        bpd_struct = bpd_node.get_structure()
        for seq_idx, seq in enumerate(bpd_struct['BehaviorSequences']):
            for cold_idx, cold in enumerate(seq['ConsolidatedOutputLinkData']):
                if float(cold['ActivateDelay']) > 0:
                    bpd_stmts.append('set {} BehaviorSequences[{}].ConsolidatedOutputLinkData[{}].ActivateDelay {}'.format(
                        bpd_name, seq_idx, cold_idx, round(float(cold['ActivateDelay'])/5, 3),
                        ))

        # Output a statement to ensure that attached items are immediately
        # available
        for child in bpd_node.get_children_with_name('behavior_attachitems'):
            child_struct = child.get_structure()
            if child_struct['bDisablePickups'] == 'True':
                disable_stmts.append('set {}.{} bDisablePickups False'.format(bpd_name, child.name))

        # Get a list of animation trees which are in use by the container
        trees = set()
        for child in bpd_node.get_children_with_name('behavior_simpleanimplay'):
            child_struct = child.get_structure()
            found_trees.add(Data.get_struct_attr_obj(child_struct, 'Tree'))

print('Trees:')
print('')
for tree in sorted(found_trees):
    tree_obj = data.get_struct_by_full_object(tree)
    if 'AnimTickArray' in tree_obj:
        for tickarray in sorted(tree_obj['AnimTickArray']):
            if tickarray.startswith('WillowAnimNode_Simple'):
                print('set {} PlayRate 5'.format(tickarray.split("'")[1]))
print('')

print('Items available at spawn:')
print('')
for stmt in disable_stmts:
    print(stmt)
print('')

print('Item spawn delay:')
print('')
for stmt in bpd_stmts:
    print(stmt)
print('')
