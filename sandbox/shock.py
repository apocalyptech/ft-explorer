#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

data = Data('BL2')
for aidef in data.get_all_by_type('AIClassDefinition'):
    structure = data.get_node_by_full_object(aidef).get_structure()
    chance_modifier = None
    duration_modifier = None
    damage_impact_modifier = None
    damage_status_modifier = None
    report = False
    if 'BaseShockChanceResistanceModifier' in structure:
        value = round(float(structure['BaseShockChanceResistanceModifier']['BaseValueConstant']), 6)
        if value != 1:
            chance_modifier = value
            report = True
    if 'BaseShockDurationResistanceModifier' in structure:
        value = round(float(structure['BaseShockDurationResistanceModifier']['BaseValueConstant']), 6)
        if value != 1:
            duration_modifier = value
            report = True
    if 'BaseShockDamageModifiers' in structure:
        value = round(float(structure['BaseShockDamageModifiers']['ResistanceToImpact']['BaseValueConstant']), 6)
        if value != 1:
            damage_impact_modifier = value
            report = True
        value = round(float(structure['BaseShockDamageModifiers']['ResistanceToStatusEffect']['BaseValueConstant']), 6)
        if value != 1:
            damage_status_modifier = value
            report = True

    if report:
        print(aidef)
        if chance_modifier is not None:
            print("\tBaseShockChanceResistanceModifier: {}".format(chance_modifier))
        if duration_modifier is not None:
            print("\tBaseShockDurationResistanceModifier: {}".format(duration_modifier))
        if damage_impact_modifier is not None:
            print("\tResistanceToImpact: {}".format(damage_impact_modifier))
        if damage_status_modifier is not None:
            print("\tResistanceToStatusEffect: {}".format(damage_status_modifier))
        print('')
