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

        # Output a statement to ensure that attached items are immediately
        # available
        children = list(bpd_node.get_children_with_name('behavior_attachitems'))
        if len(children) > 1:
            print('{}: {}'.format(bpd_name, len(children)))
