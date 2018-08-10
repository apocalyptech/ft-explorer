#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

def get_sequences_recurs(data, obj_name):
    to_return = set([obj_name])
    #print(obj_name)
    obj_struct = data.get_struct_by_full_object(obj_name)
    seq_list = []
    if 'SequenceObjects' in obj_struct:
        seq_list.extend(obj_struct['SequenceObjects'])
    if 'NestedSequences' in obj_struct:
        seq_list.extend(obj_struct['NestedSequences'])
    for seq_name in seq_list:
        if seq_name.startswith("Sequence'"):
            (junk1, new_seq_obj_name, junk2) = seq_name.split("'", 2)
            to_return.update(get_sequences_recurs(data, new_seq_obj_name))
    return to_return

data = Data('BL2')
for (label, level) in data.get_levels():
    main_seq_name = '{}.TheWorld:PersistentLevel.Main_Sequence'.format(level)
    #print('{} ({})'.format(label, level))
    #for seq_name in sorted(get_sequences_recurs(data, main_seq_name)):
    #    print(' * {}'.format(seq_name))
    #print('')
    print('\'{}\': ['.format(level))
    for seq_name in sorted(get_sequences_recurs(data, main_seq_name)):
        print('    \'{}\','.format(seq_name))
    print('    ],')
