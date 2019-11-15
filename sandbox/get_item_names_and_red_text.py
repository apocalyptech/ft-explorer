#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

# Attempts to correlate weapon, shield, and grenade red text to the items themselves,
# basically just to ease creating a Red Text Explainer, basically.
#
# The code is pretty awful, sorry about that.  There's a million different places
# where item names and CustomPresentations can get defined, and I've let all sorts
# of duplicated code all over the place here.

# Does not get TPS's Cry Baby properly, though I'm not surprised since that
# one's rather weird.
#
# Also doesn't get TPS's Cutie Killer or Heartfull Splodger

games = ['TPS']
#games = ['BL2', 'TPS']
blacklist = {
        'BL2': set([
            'GD_Allium_TG_Plot_M01Data.Weapons.Weapon_JabberSlagWeapon',
            'GD_Flynt.Weapons.AR_Flynt',
            'GD_Iris_MotorMama.Weapons.LauncherCustom',
            'GD_Leprechaun.Weapons.SG_Leprechaun',
            'GD_Lilac_SkillsBase.Buzzaxe.Buzzaxe',
            'GD_Orchid_BossWeapons.AssaultRifle.AR_Jakobs_3_Stinkpot_Nodrop',
            'GD_Orchid_BossWeapons.RPG.Ahab.Orchid_Boss_Ahab_Balance_NODROP',
            'GD_Sage_HarpoonGun.Balance.Sage_HarpoonGun_Balance',
            'GD_Weap_AssaultRifle.A_Weapons_Elemental.AR_Bandit_2_Fire',
            'GD_Weap_AssaultRifle.A_Weapons_Unique.AR_Dahl_1_GBX',
            'GD_Weap_SMG.A_Weapons_Unique.SMG_Gearbox_1',
            'GD_Weap_Scorpio.A_Weapon.WeapBalance_Scorpio',
            'GD_Weap_SniperRifles.A_Weapons.Sniper_Maliwan_4_Mordecai',
            'GD_Weap_SniperRifles.A_Weapons_Unique.Sniper_Gearbox_1',
            'WillowGame.Default__WeaponBalanceDefinition',
            ]),
        'TPS': set([
            'Evyn_Test.A_Weapons.Pistol_Bandit_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.Pistol_Dahl_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.Pistol_Hyperion_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.Pistol_Maliwan_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.Pistol_Tediore_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.SMG_Bandit_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.SMG_Dahl_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.SMG_Hyperion_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.SMG_Maliwan_2_Uncommon_Ice',
            'Evyn_Test.A_Weapons.SMG_Tediore_2_Uncommon_Ice',
            'GD_Cork_Weap_Lasers.A_Weapons_Enemy_DahlOnly.Laser_Dahl_HypBarrel',
            'GD_Cork_Weap_Lasers.A_Weapons_Mission.Laser_Dahl_1_Zap',
            'GD_Cork_Weap_Lasers.A_Weapons_Mission.Laser_Dahl_1_Zap2',
            'GD_Cork_Weap_Lasers.A_Weapons_Mission.Laser_Dahl_1_Zap3',
            'GD_Cork_Weap_Lasers.A_Weapons_Mission.Laser_Dahl_3_Zap4',
            'GD_Cork_Weap_Lasers.A_Weapons_Mission.Laser_Maliwan_PerfectHibernation',
            'GD_Cork_Weap_Pistol.A_Weapons_Elemental.Pistol_01_Ice',
            'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Starter_Dahl_Wilhelm',
            'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Starter_Hyperion_JackD',
            'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Starter_Jakobs_Nisha',
            'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Starter_Maliwan_Athena',
            'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Starter_Torgue_Anna',
            'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Starter_Vladof_Fragtrap',
            'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Maliwan_BankReward',
            'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Starter_Hyperion_JackD',
            'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Starter_Tediore_Fragtrap',
            'GD_Cork_Weap_Shotgun.A_Weapons_Unique.Shotgun_Starter_Hyperion_Wilhelm',
            'GD_Cork_Weap_Shotgun.A_Weapons_Unique.Shotgun_Starter_Torgue_Anna',
            'GD_Cork_Weap_SniperRifles.A_Weapons_Unique.Sniper_Starter_Jakobs_Nisha',
            'GD_DahlPowersuit_Knuckle.Weapons.Knuckle_Laser_Dahl',
            'GD_DahlShared.WeaponBalance.Laser_Dahl_2_Uncommon_DahlBarrel',
            'GD_DahlShared.WeaponBalance.Laser_Dahl_3_Rare_DahlBarrel',
            'GD_DahlShared.WeaponBalance.Laser_Dahl_EnemyUse_DahlBarrel',
            'GD_Enforcer_Skills.Weapon.Laser_VengenceCannon',
            'GD_Ma_SH4D0W-TP.Weapon.WeaponBalance_DahlBlasterOnly',
            'GD_Ma_ShadowClone.Weapon.WeaponBalance_ShadowCloneBlaster',
            'GD_Prototype_BuzzAxe.A_Weapons.BalanceDef_FragTrap_BuzzAxe',
            'GD_Prototype_Dummy.A_Weapons.WeapBalance_MinionTrapTurret',
            'GD_Prototype_Stethoscope.A_Weapons.Laser_Stethoscope',
            'GD_Weap_AssaultRifle.A_Weapons_Elemental.AR_Bandit_2_Fire',
            'GD_Weap_AssaultRifle.A_Weapons_Unique.AR_Dahl_1_GBX',
            'GD_Weap_Pistol.A_Weapons_Elemental.Pistol_Maliwan_2_Fire',
            'GD_Weap_Pistol.A_Weapons_Unique.Pistol_Dahl_Starter',
            'GD_Weap_SMG.A_Weapons_Unique.SMG_Gearbox_1',
            'GD_Weap_SniperRifles.A_Weapons_Unique.Sniper_Gearbox_1',
            'gd_cork_weap_assaultrifle.A_Weapons_Unique.AR_Starter_Vladof_Athena',
            'WillowGame.Default__WeaponBalanceDefinition',
            ]),
    }

def get_presentations(data, base_obj):
    customs = set()
    if 'CustomPresentations' in base_obj and base_obj['CustomPresentations'] != '':
        for cp_full in base_obj['CustomPresentations']:
            cp_name = Data.get_attr_obj(cp_full)
            cp = data.get_struct_by_full_object(cp_name)
            if 'NoConstraintText' in cp and cp['NoConstraintText'] != '':
                customs.add((cp_name, cp['NoConstraintText']))
            if 'Description' in cp and cp['Description'] != '':
                # Have to work around a deficiency in our data processing
                # (should probably just check for `type(foo) == dict` and solve it more generally, eh?)
                if cp['Description'] == {'E ': ' mc^(OMG)/wtf'}:
                    customs.add((cp_name, 'E = mc^(OMG)/wtf'))
                elif cp['Description'] == {'5+7+1': 'Zero'}:
                    customs.add((cp_name, '5+7+1=Zero'))
                else:
                    customs.add((cp_name, cp['Description']))
    return customs

def get_names(data, partdef, attr_name, get_customs=False):
    names = set()
    customs = set()
    if attr_name in partdef and partdef[attr_name] != '':
        for namepart_full in partdef[attr_name]:
            namepart_name = Data.get_attr_obj(namepart_full)
            namepart = data.get_struct_by_full_object(namepart_name)
            if 'PartName' in namepart and namepart['PartName'] != '':
                names.add(namepart['PartName'])
            if get_customs:
                customs |= get_presentations(data, namepart)
    if get_customs:
        return (list(names), list(customs))
    else:
        return list(names)

for game in games:

    data = Data(game)

    # Weapons
    if True:
        for baldef_name in sorted(data.get_all_by_type('WeaponBalanceDefinition')):

            # Don't process anything in the blacklist
            if baldef_name in blacklist[game]:
                continue

            baldef_struct = data.get_struct_by_full_object(baldef_name)
            try:
                partlist = data.get_struct_attr_obj_real(baldef_struct, 'RuntimePartListCollection')
            except KeyError:
                partlist = data.get_struct_attr_obj_real(baldef_struct, 'WeaponPartListCollection')
            # Only really interested in the Barrel, since I'm after red-text guns.
            for part_dict in partlist['BarrelPartData']['WeightedParts']:
                partdef = data.get_struct_attr_obj_real(part_dict, 'Part')
                prefixes = get_names(data, partdef, 'PrefixList')
                (names, customs) = get_names(data, partdef, 'TitleList', get_customs=True)
                if len(prefixes) == 0:
                    prefix = ''
                elif len(prefixes) == 1:
                    prefix = '{} '.format(prefixes[0])
                else:
                    prefix = '({}) '.format(', '.join(prefixes))

                if len(names) == 0:
                    name = ''
                elif len(names) == 1:
                    name = names[0]
                else:
                    name = '({})'.format(', '.join(names))

                report_name = '{}{}'.format(prefix, name)
                if report_name != '' and len(customs) > 0:
                    print(report_name)
                    print('    {}'.format(baldef_name))
                    for (cp_name, cp_val) in customs:
                        print('    {} | {}'.format(cp_name, cp_val))
                    print('')

    # Grenades and Shields
    itemname_blacklist = {'Grenade Mod', 'Arcane Grenade', 'Orb Shield'}
    if True:

        for baldef_name in sorted(data.get_all_by_type('InventoryBalanceDefinition')):

            # Don't process anything in the blacklist
            if baldef_name in blacklist[game]:
                continue

            names = set()
            customs = set()
            prefixes = set()
            baldef_struct = data.get_struct_by_full_object(baldef_name)
            if 'GrenadeModDefinition' in baldef_struct['InventoryDefinition'] or 'ShieldDefinition' in baldef_struct['InventoryDefinition']:

                # We might have presentations in the InventoryDefinition
                invdef = data.get_struct_attr_obj_real(baldef_struct, 'InventoryDefinition')
                customs |= get_presentations(data, invdef)

                # The InvDef might have an ItemName
                if 'ItemName' in invdef and invdef['ItemName'] != '':
                    if invdef['ItemName'] not in itemname_blacklist:
                        names.add(invdef['ItemName'])

                # ... it also might have Titles and prefixes
                prefixes |= set(get_names(data, invdef, 'PrefixList'))
                (new_names, new_customs) = get_names(data, invdef, 'TitleList', get_customs=True)
                names |= set(new_names)
                customs |= set(new_customs)

                # The InvDef itself may have (Alpha|Beta|Gamma|Delta)Parts attrs
                #for attr_name in ['AlphaParts', 'BetaParts', 'GammaParts', 'DeltaParts']:
                for attr_name in ['DeltaParts']:
                    if attr_name in invdef and invdef[attr_name] != '' and invdef[attr_name] != 'None':
                        part_obj = data.get_struct_attr_obj_real(invdef, attr_name)
                        if 'WeightedParts' in part_obj and part_obj['WeightedParts'] != '':
                            for part_struct in part_obj['WeightedParts']:
                                part = data.get_struct_attr_obj_real(part_struct, 'Part')

                                customs |= get_presentations(data, part)

                                prefixes |= set(get_names(data, part, 'PrefixList'))
                                (new_names, new_customs) = get_names(data, part, 'TitleList', get_customs=True)
                                names |= set(new_names)
                                customs |= set(new_customs)

                # Look for stuff in the PartListCollection, if we have it
                if baldef_struct['PartListCollection'] != 'None':
                    plc = data.get_struct_attr_obj_real(baldef_struct, 'PartListCollection')

                    # I think that useful things (that we're looking for anyway) are in Alpha and Beta.
                    # Shields use at least Delta as well, too...
                    for attr_name in ['AlphaPartData', 'BetaPartData', 'DeltaPartData']:
                        for part_struct in plc[attr_name]['WeightedParts']:
                            part = data.get_struct_attr_obj_real(part_struct, 'Part')

                            customs |= get_presentations(data, part)

                            prefixes |= set(get_names(data, part, 'PrefixList'))
                            (new_names, new_customs) = get_names(data, part, 'TitleList', get_customs=True)
                            names |= set(new_names)
                            customs |= set(new_customs)
                
                prefix_list = list(prefixes)
                if len(prefix_list) == 0:
                    prefix = ''
                elif len(prefix_list) == 1:
                    prefix = '{} '.format(prefix_list[0])
                else:
                    prefix = '({}) '.format(', '.join(prefix_list))

                name_list = list(names)
                if len(name_list) == 0:
                    name = ''
                elif len(name_list) == 1:
                    name = name_list[0]
                else:
                    name = '({})'.format(', '.join(name_list))

                report_name = '{}{}'.format(prefix, name)
                if report_name != '' and len(customs) > 0:
                    print(report_name)
                    print('    {}'.format(baldef_name))
                    for (cp_name, cp_val) in customs:
                        print('    {} | {}'.format(cp_name, cp_val))
                    print('')
