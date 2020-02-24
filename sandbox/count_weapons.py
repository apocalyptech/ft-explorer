#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data, Weight

# This is a bit silly, just got curious.

verbose = False
if len(sys.argv) > 1:
    if sys.argv[1][:2].lower() == '-v':
        verbose = True

# TODO: Updated data packages for DLC5 made things a bit screwy; this probably
# won't show the correct numbers anymore.  BL2 will need a *ton* of blacklists,
# probably, and the new data package seems to have broken some TPS balances
# as well, since I'd ended up regenerating my own TPS data as well.  Meh.

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

            # We should actually probably add a *lot* of Anemone balances to
            # the blacklist.  Just doing any which are Actually Problematic
            # right now, though.
            'GD_Anemone_Weapons.A_Weapons.AR_Bandit_3_Rare_Alien_Shock',
            'GD_Anemone_Weapons.A_Weapons.AR_Bandit_3_Rare_Alien_Slag',
            'GD_Anemone_Weapons.Rocket_Launcher.RL_Maliwan_5_Pyrophobia',
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

            # Boo, updated data packages don't like these now:
            'GD_Cork_Weap_SniperRifles.A_Weapons_Unique.Sniper_Jakobs_3_Trespasser',
            'GD_Weap_Pistol.A_Weapons_Unique.Pistol_Maliwan_3_Rubi',
            ]),
    }

for game in ['BL2', 'TPS']:
    total_count = 0
    total_count_no_luneshine = 0
    data = Data(game)
    for baldef_name in sorted(data.get_all_by_type('WeaponBalanceDefinition')):

        # Don't process anything in the blacklist
        if baldef_name in blacklist[game]:
            continue

        baldef_struct = data.get_struct_by_full_object(baldef_name)
        partlist_name = Data.get_struct_attr_obj(baldef_struct, 'RuntimePartListCollection')
        if partlist_name:
            partlist = data.get_struct_by_full_object(partlist_name)
            
            # First get our CAID data
            caids = {}
            for (idx, caid) in enumerate(partlist['ConsolidatedAttributeInitData']):
                caids[idx] = Weight(caid).value

            # Now loop through
            gun_types = 1
            gun_types_no_luneshine = 1
            for attr in ['BodyPartData', 'GripPartData', 'BarrelPartData',
                    'SightPartData', 'StockPartData', 'ElementalPartData',
                    'Accessory1PartData', 'Accessory2PartData']:
                if attr in partlist:
                    part_count = 0
                    part_count_no_luneshine = 0
                    zero_weights = 0
                    if partlist[attr]['bEnabled'] == 'False':
                        continue
                    if 'WeightedParts' not in partlist[attr] or partlist[attr] == '':
                        continue
                    for part in partlist[attr]['WeightedParts']:
                        if caids[int(part['DefaultWeightIndex'])] == 0:
                            zero_weights += 1
                            continue
                        if caids[int(part['MinGameStageIndex'])] >= 100:
                            continue
                        part_count += 1
                        if 'Moonstone_Attachment' not in part['Part']:
                            part_count_no_luneshine += 1

                    # Looks like many gun types technically weight everything in
                    # an individual parts list at zero, and apparently that just
                    # makes them all equally likely (instead of disallowing that
                    # part slot entirely).  So, if *all* the weights were zero,
                    # add them all in.
                    if zero_weights > 0 and zero_weights == len(partlist[attr]['WeightedParts']):
                        for part in partlist[attr]['WeightedParts']:
                            if caids[int(part['MinGameStageIndex'])] >= 100:
                                continue
                            part_count += 1
                            if 'Moonstone_Attachment' not in part['Part']:
                                part_count_no_luneshine += 1

                    #print('{}: {} part(s)'.format(attr, part_count))
                    if part_count > 0:
                        gun_types *= part_count
                    if part_count_no_luneshine > 0:
                        gun_types_no_luneshine *= part_count_no_luneshine
            
            # And finally, add this to our total
            if verbose:
                print('{} {}: {:,}'.format(game, baldef_name, gun_types))
                if game == 'TPS':
                    print('{} {}: {:,} (without Luneshine)'.format(
                        game,
                        baldef_name,
                        gun_types_no_luneshine,
                        ))
            total_count += gun_types
            total_count_no_luneshine += gun_types_no_luneshine
            if verbose and game == 'TPS':
                print('Running totals: {}, {} ({:0.1f}x)'.format(
                    total_count,
                    total_count_no_luneshine,
                    total_count/total_count_no_luneshine,
                    ))

    # Report on the total number of guns per game
    print('{}: {:,} unique guns'.format(game, total_count))
    if game == 'TPS':
        print('{}: {:,} unique guns (without luneshine)'.format(game, total_count_no_luneshine))
