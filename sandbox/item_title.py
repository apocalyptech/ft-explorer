#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
import traceback
from ftexplorer.data import Data

print('Note: this does not find class mod titles, which have')
print('parts like weapons/grenades but whose titles are found')
print('via their InventoryDefinition instead.')
print('')

data = Data('BL2')

def title_from_partdef(data, partlist):
    for part_def in partlist['WeightedParts']:
        part = data.get_struct_attr_obj_real(part_def, 'Part')
        if part:
            if 'TitleList' in part:
                for title_def in part['TitleList']:
                    title = data.get_struct_by_full_object(Data.get_attr_obj(title_def))
                    print(title['PartName'])
        else:
            raise Exception('No definitions!')

def print_title(bal_name):
    try:
        bal_struct = data.get_struct_by_full_object(bal_name)
        if 'ItemName' in bal_struct:
            top_level = 'ItemName'
        elif 'RuntimePartListCollection' in bal_struct:
            top_level = 'RuntimePartListCollection'
        elif 'PartListCollection' in bal_struct:
            top_level = 'PartListCollection'
        else:
            raise Exception('Unknown top-level attribute')

        if bal_struct[top_level] == 'None':
            # This should match on shields

            if 'InventoryDefinition' in bal_struct:
                inv_def = data.get_struct_attr_obj_real(bal_struct, 'InventoryDefinition')
                if 'TitleList' in inv_def:
                    for title_def in inv_def['TitleList']:
                        title = data.get_struct_by_full_object(Data.get_attr_obj(title_def))
                        print(title['PartName'])
                else:
                    for partlist_name in ['AlphaParts', 'BetaParts', 'GammaParts', 'DeltaParts']:
                        if partlist_name in inv_def and inv_def[partlist_name] != 'None':
                            partlist = data.get_struct_attr_obj_real(inv_def, partlist_name)
                            title_from_partdef(data, partlist)
                #elif 'AlphaParts' in inv_def:
                #    #print(inv_def)
                #    #title_from_partdef(data, inv_def, 'AlphaParts')
                #else:
                #    raise Exception('No mid-level attribute found')
            else:
                raise Exception('Exhausted possible top-level attributes')

        else:
            # This should match on weapons, relics, and grenade mods

            if top_level == 'ItemName':
                # This'll match on relics
                print(bal_struct['ItemName'])

            else:
                # Weapons and grenade mods
                partlist = data.get_struct_attr_obj_real(bal_struct, top_level)
                if 'BarrelPartData' in partlist:
                    to_get = 'BarrelPartData'
                elif 'AlphaPartData' in partlist:
                    to_get = 'AlphaPartData'
                else:
                    raise Exception('No understood part type found')
                title_from_partdef(data, partlist[to_get])

    except Exception as e:
        (ex_type, ex_val, ex_tb) = sys.exc_info()
        print('Error getting title: {}: {}'.format(ex_type.__name__, e))
        print('')
        traceback.print_exception(*sys.exc_info(), file=sys.stderr)


if len(sys.argv) > 1:
    for name in sys.argv[1:]:
        print('{}:'.format(name))
        print('')
        print_title(name)
        print('')
else:
    while True:
        sys.stdout.write('Input an item/weapon Definition> ')
        sys.stdout.flush()
        bal_name = sys.stdin.readline().strip()
        if bal_name.lower() == 'quit' or bal_name.lower() == 'exit':
            break
        print('')
        print_title(bal_name)
        print('')
