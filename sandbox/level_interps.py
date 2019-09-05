#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
import sys
import json
import lzma
from ftexplorer.data import Data
        
# Finding all SeqAct_Interp objects for the specified level, and reporting
# their PlayRates and what variable labels they bind to

# Grab an arg first
level_name_arg = sys.argv[1]

# Cache info if we haven't already
game = 'BL2'
data = Data(game)
cache_filename = 'level_interps_{}.json.xz'.format(game)
if not os.path.exists(cache_filename):
    with lzma.open(cache_filename, 'wt') as df:
        level_prefixes = []
        level_interps = {}
        for (level_name, level_package) in data.get_levels():
            for sub_level_name in data.get_level_package_nodes(level_package):
                level_prefixes.append((level_package, '{}.Main_Sequence'.format(sub_level_name[0])))
        for interp_name in data.get_all_by_type('SeqAct_Interp'):
            for (level_package, seq_prefix) in level_prefixes:
                seq_prefix = seq_prefix.lower()
                if interp_name.lower().startswith(seq_prefix):
                    if level_package not in level_interps:
                        level_interps[level_package] = []
                    level_interps[level_package].append(interp_name)
                    break
        json.dump(level_interps, df)
else:
    with lzma.open(cache_filename, 'rt') as df:
        level_interps = json.load(df)

# Now look through the requested level's seqact_interps
for interp_name in level_interps[level_name_arg]:
    interp_data = data.get_struct_by_full_object(interp_name)
    playrate = interp_data['PlayRate']
    interp_vars = []
    data_vars = set()
    interpdata_names = set()
    if 'VariableLinks' in interp_data and interp_data['VariableLinks'] != '' and interp_data['VariableLinks'] != 'None':
        for interp_var in interp_data['VariableLinks']:
            interp_vars.append(interp_var['LinkDesc'].strip('"'))
            if 'LinkedVariables' in interp_var and interp_var['LinkedVariables'] != '' and interp_var['LinkedVariables'] != 'None':
                # Working around a bug in our struct processing!  These will always be a string.  Must split on our own.
                linked_variables = interp_var['LinkedVariables'].split(',')
                for linked in linked_variables:
                    linkedvar_name = Data.get_attr_obj(linked)
                    if 'InterpData_' in linkedvar_name:
                        interpdata_names.add(linkedvar_name)
                        interpdata_data = data.get_struct_by_full_object(linkedvar_name)
                        if 'InterpGroups' in interpdata_data and interpdata_data['InterpGroups'] != '' and interpdata_data['InterpGroups'] != 'None':
                            for inner_group_full in interpdata_data['InterpGroups']:
                                inner_group_name = Data.get_attr_obj(inner_group_full)
                                inner_group = data.get_struct_by_full_object(inner_group_name)
                                data_vars.add(inner_group['GroupName'])
                            pass
                        else:
                            data_vars.add('(empty)')
    print('{} - Play Rate: {}'.format(interp_name, playrate))
    print(' * Vars: {}'.format(', '.join(interp_vars)))
    if len(data_vars) > 0:
        print(' * InterpData Names: {}'.format(', '.join(data_vars)))
        print(' * (From: {})'.format(','.join(interpdata_names)))
    print('')

