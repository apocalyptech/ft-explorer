#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

print('This is just used to compare some basic info between versions')
print('of guns.  Only prints out some real basic info, does not include')
print('things like firing mode definitions, BPDs, etc...')
print('')
print(sys.argv[1])
print('-'*len(sys.argv[1]))
print('')

data = Data('BL2')

bal = data.get_struct_by_full_object(sys.argv[1])
plc = data.get_struct_attr_obj_real(bal, 'RuntimePartListCollection')

for parttype in ['Body', 'Grip', 'Barrel', 'Sight', 'Stock', 'Elemental', 'Accessory1']:
    part_list = []
    for pd in plc['{}PartData'.format(parttype)]['WeightedParts']:
        part_list.append(' * {}'.format(pd['Part'].split("'")[1]))

    print('{}:'.format(parttype))
    for part in sorted(part_list):
        print(part)
    print('')

# Get barrel effects
barrel = data.get_struct_attr_obj_real(plc['BarrelPartData']['WeightedParts'][0], 'Part')
if 'WeaponAttributeEffects' in barrel and barrel['WeaponAttributeEffects'] != 'None':
    print('Weapon Attribute Effects:')
    print('')
    for effect in barrel['WeaponAttributeEffects']:
        print(' * {} - {} - {},{},{},{}'.format(
            Data.get_struct_attr_obj(effect, 'AttributeToModify'),
            effect['ModifierType'],
            effect['BaseModifierValue']['BaseValueConstant'],
            effect['BaseModifierValue']['BaseValueAttribute'],
            effect['BaseModifierValue']['InitializationDefinition'],
            effect['BaseModifierValue']['BaseValueScaleConstant'],
            ))
    print('')

if 'AttributeSlotUpgrades' in barrel and barrel['AttributeSlotUpgrades'] != 'None':
    print('Weapon Attribute Slot Upgrades:')
    print('')
    for upgrade in barrel['AttributeSlotUpgrades']:
        print(' * {}: {}'.format(
            upgrade['SlotName'],
            upgrade['GradeIncrease'],
            ))
