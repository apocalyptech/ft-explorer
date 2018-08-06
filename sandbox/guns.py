#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Loops through our FT-Explorer data to find unique/legendary weapons
# and generate a bunch of hotfixes which make them guaranteed to drop
# with Luneshine.  For most weapons, this is just disabling the "no
# luneshine" option (if we remove the option entirely, vanilla non-
# Luneshine'd guns loaded with this patch would be removed, but
# simply disabling it works fine).  A handful of other guns were
# missing a Luneshine accessory definition stanza entirely, so we add
# that in, for those.

# This requires my FT Explorer project from https://github.com/apocalyptech/ft-explorer
# In the end it's probably best to copy it in the base dir of that,
# and run it from there.

import re
import sys
from ftexplorer.data import Data

print('Loading weapon list')
weapons = [
    'gd_cork_weap_assaultrifle.A_Weapons_Legendary.AR_Dahl_5_MajorTom',
    'gd_cork_weap_assaultrifle.A_Weapons_Legendary.AR_Jakobs_5_HammerBreaker',
    'gd_cork_weap_assaultrifle.A_Weapons_Legendary.AR_Torgue_5_KerBoom',
    'gd_cork_weap_assaultrifle.A_Weapons_Legendary.AR_Vladof_5_Shredifier',
    'gd_cork_weap_assaultrifle.A_Weapons_Unique.AR_Jakobs_3_Wallop',
    'gd_cork_weap_assaultrifle.A_Weapons_Unique.AR_Vladof_3_Hail',
    'gd_cork_weap_assaultrifle.A_Weapons_Unique.AR_Vladof_3_IceScream',
    'gd_cork_weap_assaultrifle.A_Weapons_Unique.AR_Vladof_3_OldPainful',
    'GD_Cork_Weap_Lasers.A_Weapons_Legendary.Laser_Dahl_5_Ricochet',
    'GD_Cork_Weap_Lasers.A_Weapons_Legendary.Laser_Dahl_5_ZX1',
    'GD_Cork_Weap_Lasers.A_Weapons_Legendary.Laser_Old_Hyperion_5_Excalibastard',
    'GD_Cork_Weap_Lasers.A_Weapons_Legendary.Laser_Tediore_5_Tesla',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Dahl_3_Firestarta',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Hyperion_3_Mining',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Maliwan_3_Blizzard',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Maliwan_3_VibraPulse',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Maliwan_4_Egun',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Maliwan_4_Rosie',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Maliwan_4_SavorySideSaber',
    'GD_Cork_Weap_Lasers.A_Weapons_Unique.Laser_Tediore_3_Vandergraffen',
    'GD_Cork_Weap_Launchers.A_Weapons_Legendary.RL_Bandit_5_BadaBoom',
    'GD_Cork_Weap_Launchers.A_Weapons_Legendary.RL_Bandit_5_Thingy',
    'GD_Cork_Weap_Launchers.A_Weapons_Legendary.RL_Maliwan_5_Cryophobia',
    'GD_Cork_Weap_Launchers.A_Weapons_Legendary.RL_Torgue_5_Nukem',
    'GD_Cork_Weap_Launchers.A_Weapons_Legendary.RL_Vladof_5_Mongol',
    'GD_Cork_Weap_Launchers.A_Weapons_Unique.RL_Tediore_3_Rocketeer',
    'GD_Cork_Weap_Launchers.A_Weapons_Unique.RL_Torgue_3_Creamer',
    'GD_Cork_Weap_Pistol.A_Weapons_Legendary.Pistol_Bandit_5_Zim',
    'GD_Cork_Weap_Pistol.A_Weapons_Legendary.Pistol_Dahl_5_Blowfly',
    'GD_Cork_Weap_Pistol.A_Weapons_Legendary.Pistol_Jakobs_5_Maggie',
    'GD_Cork_Weap_Pistol.A_Weapons_Legendary.Pistol_Tediore_5_Shooterang',
    'GD_Cork_Weap_Pistol.A_Weapons_Legendary.Pistol_Torgue_5_88Fragnum',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Dahl_3_GwensOtherHead',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Hyperion_3_Fibber',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Hyperion_3_Globber',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Hyperion_3_LadyFist',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Jakobs_3_Smasher',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Jakobs_CyberColt',
    'GD_Cork_Weap_Pistol.A_Weapons_Unique.Pistol_Maliwan_3_Moxxis_Probe',
    'GD_Cork_Weap_SMG.A_Weapons_Legendary.SMG_Dahl_5_Torrent',
    'GD_Cork_Weap_SMG.A_Weapons_Legendary.SMG_Hyperion_5_Bitch',
    'GD_Cork_Weap_SMG.A_Weapons_Legendary.SMG_Maliwan_5_HellFire',
    'GD_Cork_Weap_SMG.A_Weapons_Legendary.SMG_Tediore_5_IVF',
    'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Bandit_3_MareksMouth',
    'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Bandit_3_MeatGrinder',
    'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Maliwan_3_BadTouch',
    'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Maliwan_3_GoodTouch',
    'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Old_Hyperion_BlackSnake',
    'GD_Cork_Weap_Shotgun.A_Weapons_Legendary.SG_Bandit_5_SledgesShotgun',
    'GD_Cork_Weap_Shotgun.A_Weapons_Legendary.SG_Hyperion_5_ConferenceCall',
    'GD_Cork_Weap_Shotgun.A_Weapons_Legendary.SG_Jakobs_5_Striker',
    'GD_Cork_Weap_Shotgun.A_Weapons_Legendary.SG_Torgue_5_Flakker',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Bandit_3_Boganella',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Jakobs_3_Moonface',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Jakobs_Boomacorn',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Jakobs_TooScoops',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Old_Hyperion_3_Bullpup',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Tediore_3_Octo',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Torgue_3_JackOCannon',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Torgue_3_Torguemada',
    'GD_Cork_Weap_Shotgun.A_Weapons_Unique.SG_Torgue_3_Wombat',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Legendary.Sniper_Dahl_5_Pitchfork',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Legendary.Sniper_Hyperion_5_Invader',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Legendary.Sniper_Jakobs_5_Skullmasher',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Legendary.Sniper_Maliwan_5_Magma',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Legendary.Sniper_Vladof_5_Longnail',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Unique.Sniper_Dahl_3_WetWeek',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Unique.Sniper_Jakobs_3_Razorback',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Unique.Sniper_Maliwan_3_ChereAmie',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Unique.Sniper_Vladof_3_TheMachine',
    'GD_Cypressure_Weapons.A_Weapons_Unique.AR_Bandit_3_BossNova',
    'GD_Cypressure_Weapons.A_Weapons_Unique.SG_Hyperion_3_CompanyMan',
    'GD_Cypressure_Weapons.A_Weapons_Unique.SG_Torgue_3_Landscaper2',
    'GD_Cypressure_Weapons.A_Weapons_Unique.SMG_Bandit_3_FastTalker',
    'GD_Ma_Weapons.A_Weapons_Legendary.AR_Bandit_5_Fusillade',
    'GD_Ma_Weapons.A_Weapons_Legendary.Laser_Hyperion_5_LongestYard',
    'GD_Ma_Weapons.A_Weapons_Legendary.Laser_Maliwan_5_FusionBeam',
    'GD_Ma_Weapons.A_Weapons_Legendary.Laser_Maliwan_5_Thunderfire',
    'GD_Ma_Weapons.A_Weapons_Legendary.Laser_Tediore_5_LaserDisker',
    'GD_Ma_Weapons.A_Weapons_Legendary.Pistol_Jakobs_5_LuckCannon',
    'GD_Ma_Weapons.A_Weapons_Legendary.Pistol_Vladof_5_Expander',
    'GD_Ma_Weapons.A_Weapons_Legendary.RL_Tediore_5_KanedasLaser',
    'GD_Ma_Weapons.A_Weapons_Legendary.SG_Jakobs_5_Flayer',
    'GD_Ma_Weapons.A_Weapons_Legendary.SMG_Hyperion_5_CheatCode',
    'GD_Ma_Weapons.A_Weapons_Legendary.Sniper_Old_Hyperion_5_OmniCannon',
    'GD_Ma_Weapons.A_Weapons_Unique.Laser_Dahl_6_Glitch_HeartfullSplodger',
    'GD_Ma_Weapons.A_Weapons_Unique.Laser_Maliwan_3_Enlightenment',
    'GD_Ma_Weapons.A_Weapons_Unique.Laser_Maliwan_3_Minac',
    'GD_Ma_Weapons.A_Weapons_Unique.Pistol_Bandit_3_PartyPopper',
    'GD_Ma_Weapons.A_Weapons_Unique.Pistol_Maliwan_3_HardReboot',
    'GD_Ma_Weapons.A_Weapons_Unique.SMG_Bandit_6_Glitch_CutieKiller',
    'GD_Petunia_Weapons.AssaultRifles.AR_Bandit_3_CryBaby',
    'GD_Petunia_Weapons.Launchers.RL_Vladof_5_Menace',
    'GD_Petunia_Weapons.Pistols.Pistol_Hyperion_3_T4sr',
    'GD_Petunia_Weapons.SMGs.SMG_Tediore_3_Boxxy',
    'GD_Petunia_Weapons.Shotguns.SG_Tediore_3_PartyLine',
    'GD_Petunia_Weapons.Snipers.Sniper_Jakobs_3_Plunkett',
    'GD_Weap_Pistol.A_Weapons_Legendary.Pistol_Hyperion_5_LogansGun',
    'GD_Weap_SMG.A_Weapons_Unique.SMG_Dahl_3_Fridgia',
    'GD_Weap_SMG.A_Weapons_Unique.SMG_Maliwan_3_Frostfire',
    'GD_Weap_SniperRifles.A_Weapons_Unique.Sniper_Hyperion_3_FremingtonsEdge',
    ]

# Some weapons get a pass because they have custom Luneshine attachments
# (or, in some cases, are glitch guns)
weap_exclude = set([
    'GD_Cork_Weap_SMG.A_Weapons_Unique.SMG_Bandit_3_MareksMouth',
    'GD_Ma_Weapons.A_Weapons_Unique.Laser_Dahl_6_Glitch_HeartfullSplodger',
    'GD_Ma_Weapons.A_Weapons_Unique.SMG_Bandit_6_Glitch_CutieKiller',
    'GD_Petunia_Weapons.AssaultRifles.AR_Bandit_3_CryBaby',
    'GD_Cork_Weap_SniperRifles.A_Weapons_Legendary.Sniper_Vladof_5_Longnail',
    ])

print('Loading TPS index')
data = Data('TPS')

print('Checking data')
hotfix_idx = 0
create_luneshine_attachments = []
for weapon_obj in weapons:

    if weapon_obj in weap_exclude:
        continue

    node = data.get_node_by_full_object(weapon_obj)
    struct = node.get_structure()
    if 'RuntimePartListCollection' in struct:
        (junk1, runtime_parts, junk2) = struct['RuntimePartListCollection'].split("'", 2)
    else:
        raise Exception('No runtime part list found for {}'.format(weapon_obj))

    if runtime_parts:
        partnode = data.get_node_by_full_object(runtime_parts)
        struct = partnode.get_structure()

        parts = struct['GripPartData']['WeightedParts']
        if len(parts) == 1:
            print('{}: {}'.format(weapon_obj, len(parts)))
