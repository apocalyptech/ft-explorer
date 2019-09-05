#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

# Finding damage sources which use WillowGame.WillowDmgSource_Skill as
# a DamageSource but don't have a damage type defined.  This causes the
# damage to come across just as "Skill" damage which can't be usefully
# blocked (at least by enemy pawns) without merging in
# D_Attributes.DamageSourceModifiers.ReceivedSkillDamageModifier
# somehow, which only exists for Sal and Zer0, I believe.

# Data types here were chosen just by searching for WillowGame.WillowDmgSource_Skill

print('Classes which appear to cause *only* Skill damage:')
print('')

data = Data('BL2')
found_types = set()
names = data.get_all_by_type('Behavior_CauseDamage')
names.extend(data.get_all_by_type('Behavior_FireBeam'))
names.extend(data.get_all_by_type('MeleeDefinition'))
names.extend(data.get_all_by_type('WillowDamageArea'))

for cd_name in names:
    cd = data.get_struct_by_full_object(cd_name)
    if 'WillowGame.WillowDmgSource_Skill' in cd['DamageSource']:
        if cd['DamageTypeDefinition'] == 'None':
            print(' * {}'.format(cd_name))
        else:
            found_types.add(cd['DamageTypeDefinition'])

for exp_name in data.get_all_by_type('Behavior_Explode'):
    exp = data.get_struct_by_full_object(exp_name)
    if 'WillowGame.WillowDmgSource_Skill' in exp['DamageSource']:
        expdef = data.get_struct_attr_obj_real(exp, 'Definition')
        if expdef['DamageTypeDef'] == 'None':
            print(' * {}'.format(exp_name))
        else:
            found_types.add(expdef['DamageTypeDef'])

reported_skills = set()
for skill_name in data.get_all_by_type('SkillDefinition'):
    skill = data.get_struct_by_full_object(skill_name)
    if 'DamageEvents' in skill and skill['DamageEvents'] != '' and skill['DamageEvents'] != 'None':
        for de in skill['DamageEvents']:
            for const in de['EventConstraints']:
                if 'WillowGame.WillowDmgSource_Skill' in const['DamageSourceConstraint']:
                    if skill_name not in reported_skills:
                        print(' * ({})'.format(skill_name))
                        reported_skills.add(skill_name)
                        break

print('')
print('Damage types found while looping:')
print('')
for found in sorted(found_types):
    print(' * {}'.format(found))
