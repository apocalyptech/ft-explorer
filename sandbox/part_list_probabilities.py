#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import csv
import sys
from ftexplorer.data import Data, Weight

# Write out a CSV of part probabilities

#games = ['BL2']
games = ['BL2', 'TPS']
valid_item_def_types = {
        'Shield',
        'GrenadeMod',
        'Artifact',
        'ClassMod',
        }
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
            ]),
    }

def process_part_list_inner(df, wp, caids, label):
    """
    Given a struct `wp` which contains the attribute 'WeightedParts`, and
    a dict `caids` which contains the processed `ConsolidatedAttributeInitData`
    data, process the part list and write to `df`
    """

    attr_parts = []
    for part in wp['WeightedParts']:
        part_name = Data.get_attr_obj(part['Part']).split('.')[-1]
        try:
            if caids[int(part['MinGameStageIndex'])] >= 100:
                print('')
                print('Skipping 100+ MinGameStageIndex in {} {}'.format(partlist_name, label))
                continue
        except KeyError:
            # This happens at least in GD_Anemone_Weapons.Rocket_Launcher.RL_Maliwan_5_Pyrophobia
            # ... we don't understand BVA, and the mingamestageindex happens to point to a
            # CAID which has one of those.  It's the only one in there, though, and this
            # check is less important anyway, so whatever.  Ignore it.
            print('Couldn\'t get MinGameStageIndex for {} {}'.format(partlist_name, label))
            pass
        if 'Manufacturers' not in part or not part['Manufacturers'] or part['Manufacturers'] == '':
            attr_parts.append((part_name, 100))
        elif part['Manufacturers'][0]['Manufacturer'] is None or part['Manufacturers'][0]['Manufacturer'] == 'None':
            attr_parts.append((part_name, caids[int(part['DefaultWeightIndex'])]))
        else:
            print('')
            raise Exception('Have not implemented Manufacturer yet...')

    total_weight = sum([p[1] for p in attr_parts])
    for (part, weight) in attr_parts:
        df.writerow({
            'game': game,
            'balance': baldef_name,
            'parttype': label,
            'part': part,
            'ind_weight': weight,
            'total_weight': total_weight,
            'pct': round(weight/total_weight*100, 1),
            })

def process_caid(obj_struct):
    """
    Given an `obj_struct` which contains a `ConsolidatedAttributeInitData` structure,
    process it into a dict which is more useful to us.
    """
    caids = {}
    for (idx, caid) in enumerate(obj_struct['ConsolidatedAttributeInitData']):
        #caids[idx] = Weight(caid).value
        try:
            caids[idx] = Weight(caid).value
        except Exception:
            # If something tries to reference this later on, we'll die then.
            pass
    return caids

def process_weapon_part_list(data, df, partlist_name, part_attributes):

    try:
        partlist = data.get_struct_by_full_object(partlist_name)
    except KeyError:
        df.writerow({
            'game': game,
            'balance': baldef_name,
            'parttype': 'ERROR',
            'part': 'ERROR',
            'pct': 'ERROR',
            })
        return
    
    # First get our CAID data
    caids = process_caid(partlist)

    # Now loop through
    for attr in part_attributes:
        if attr in partlist:
            if partlist[attr]['bEnabled'] == 'False':
                continue
            if 'WeightedParts' not in partlist[attr] or partlist[attr] == '':
                continue
            process_part_list_inner(df, partlist[attr], caids, attr)

def process_item_part_list(data, df, partlist_name, part_attributes):

    try:
        partlist = data.get_struct_by_full_object(partlist_name)
    except KeyError:
        df.writerow({
            'game': game,
            'balance': baldef_name,
            'parttype': 'ERROR',
            'part': 'ERROR',
            'pct': 'ERROR',
            })
        return
    
    # First get our CAID data

    for attr in part_attributes:
        if attr in partlist and partlist[attr] != '' and partlist[attr] != 'None':
            inner_part = data.get_struct_attr_obj_real(partlist, attr)
            caids = process_caid(inner_part)
            process_part_list_inner(df, inner_part, caids, 'bloop')

def status(text):
    max_len = 100
    if len(text) > max_len:
        text = '{}...'.format(text[:max_len])
    sys.stdout.write("{}{}\r".format(text, ' '*(max_len-len(text))))

with open('part_list_probabilities.csv', 'w', newline='') as csvfile:
    fieldnames = ['game', 'balance', 'parttype', 'part', 'ind_weight', 'total_weight', 'pct']
    df = csv.DictWriter(csvfile, fieldnames=fieldnames)
    df.writeheader()

    for game in games:

        data = Data(game)

        # Weapons
        if False:
            for baldef_name in sorted(data.get_all_by_type('WeaponBalanceDefinition')):

                # Don't process anything in the blacklist
                if baldef_name in blacklist[game]:
                    continue

                status('Processing {}'.format(baldef_name))
                baldef_struct = data.get_struct_by_full_object(baldef_name)
                partlist_name = Data.get_struct_attr_obj(baldef_struct, 'RuntimePartListCollection')
                if partlist_name:
                    process_weapon_part_list(data, df, partlist_name, [
                        'BodyPartData', 'GripPartData', 'BarrelPartData',
                        'SightPartData', 'StockPartData', 'ElementalPartData',
                        'Accessory1PartData', 'Accessory2PartData',
                        ])

        # Items
        if True:
            found_invalid_invdef_types = set()
            for baldef_name in sorted(data.get_all_by_type('InventoryBalanceDefinition')):

                # Don't process anything in the blacklist
                if baldef_name in blacklist[game]:
                    continue

                status('Processing {}'.format(baldef_name))
                baldef_struct = data.get_struct_by_full_object(baldef_name)
                invdef_type = baldef_struct['InventoryDefinition'][:baldef_struct['InventoryDefinition'].find('Definition')]
                if invdef_type not in valid_item_def_types:
                    found_invalid_invdef_types.add(invdef_type)
                    continue
                invdef_name = Data.get_struct_attr_obj(baldef_struct, 'InventoryDefinition')

                process_item_part_list(data, df, invdef_name, [
                    'AlphaParts', 'BetaParts', 'GammaParts', 'DeltaParts',
                    'EpsilonParts', 'ZetaParts', 'EtaParts', 'ThetaParts',
                    'MaterialParts',
                    ])

            print('')
            print(found_invalid_invdef_types)
