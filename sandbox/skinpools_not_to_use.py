#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# cataloguing the skinpools to avoid if you don't want to step on
# challenge rewards

from ftexplorer.data import Data

# BL2
reward_pools_challenges = [
        'GD_CustomItemPools_MainGame.Rewards.BanditEpic',
        'GD_CustomItemPools_MainGame.Rewards.BanditUncommon',
        'GD_CustomItemPools_MainGame.Rewards.BlueBold',
        'GD_CustomItemPools_MainGame.Rewards.BlueBoldAccent',
        'GD_CustomItemPools_MainGame.Rewards.BluePale',
        'GD_CustomItemPools_MainGame.Rewards.BluePattern',
        'GD_CustomItemPools_MainGame.Rewards.CyanBold',
        'GD_CustomItemPools_MainGame.Rewards.DahlEpic',
        'GD_CustomItemPools_MainGame.Rewards.Gray',
        'GD_CustomItemPools_MainGame.Rewards.GreenBold',
        'GD_CustomItemPools_MainGame.Rewards.GreenBoldAccent',
        'GD_CustomItemPools_MainGame.Rewards.GreenPale',
        'GD_CustomItemPools_MainGame.Rewards.Head1',
        'GD_CustomItemPools_MainGame.Rewards.HyperionEpic',
        'GD_CustomItemPools_MainGame.Rewards.HyperionUncommon',
        'GD_CustomItemPools_MainGame.Rewards.JakobsEpic',
        'GD_CustomItemPools_MainGame.Rewards.MaliwanEpic',
        'GD_CustomItemPools_MainGame.Rewards.MaliwanUncommon',
        'GD_CustomItemPools_MainGame.Rewards.OrangeBold',
        'GD_CustomItemPools_MainGame.Rewards.OrangeBoldAccent',
        'GD_CustomItemPools_MainGame.Rewards.OrangePale',
        'GD_CustomItemPools_MainGame.Rewards.PinkPandoracorn',
        'GD_CustomItemPools_MainGame.Rewards.PurpleBold',
        'GD_CustomItemPools_MainGame.Rewards.RedBold',
        'GD_CustomItemPools_MainGame.Rewards.RedBoldAccent',
        'GD_CustomItemPools_MainGame.Rewards.RedPale',
        'GD_CustomItemPools_MainGame.Rewards.TedioreEpic',
        'GD_CustomItemPools_MainGame.Rewards.TorgueEpic',
        'GD_CustomItemPools_MainGame.Rewards.TorgueUncommon',
        'GD_CustomItemPools_MainGame.Rewards.VladofEpic',
        'GD_CustomItemPools_MainGame.Rewards.YellowBold',
        'GD_CustomItemPools_MainGame.Rewards.YellowPale',
    ]
reward_pools_missions = [
        'GD_CustomItemPools_Flax.Rewards.FlaxPumpkinHeads',
        'GD_CustomItemPools_Lobelia.Rewards.LobeliaHead',
        'GD_CustomItemPools_Lobelia.Rewards.LobeliaSkin',
        'GD_CustomItemPools_MainGame.Rewards.CyanPale',
        'GD_CustomItemPools_MainGame.Rewards.GreenPattern',
        'GD_CustomItemPools_MainGame.Rewards.Head6',
        'GD_CustomItemPools_MainGame.Rewards.Head7',
        'GD_CustomItemPools_MainGame.Rewards.Head9',
        'GD_CustomItemPools_MainGame.Rewards.JakobsUncommon',
        'GD_CustomItemPools_MainGame.Rewards.PurpleNinja',
        'GD_CustomItemPools_MainGame.Rewards.PurplePale',
        'GD_CustomItemPools_MainGame.Rewards.YellowBoldAccent',
        'GD_CustomItemPools_Orchid.Rewards.OrchidHeads',
        'GD_CustomItemPools_Sage.Rewards.SageHead',
        'GD_CustomItemPools_Sage.Rewards.SageSkin',
        'GD_CustomItemPools_allium.Rewards.AlliumTGHeads',
        'GD_CustomItemPools_allium.Rewards.AlliumXmasHeads',
        'GD_CustomItemPools_nasturtium.Rewards.NasturtiumEasterHeads',
        'GD_CustomItemPools_nasturtium.Rewards.NasturtiumVdayHeads',
    ]
safe_pools = [
        'GD_CustomItemPools_MainGame.Rewards.Borderlands1Head',
        'GD_CustomItemPools_MainGame.Rewards.Borderlands1Skin',
        'GD_CustomItemPools_MainGame.Rewards.DigitalEdHeads',
        'GD_CustomItemPools_MainGame.Rewards.DigitalEdSkins',
        'GD_CustomItemPools_MainGame.Rewards.Gearbox',
        'GD_CustomItemPools_Aster.Rewards.AsterHead',
        'GD_CustomItemPools_Aster.Rewards.AsterSkin',
        'GD_CustomItemPools_Flax.Rewards.FlaxSkins',
        'GD_CustomItemPools_Peony.Rewards.PeonyHeads',
        'GD_CustomItemPools_Peony.Rewards.PeonySkins',
    ]
#reward_pools = reward_pools_challenges + reward_pools_missions
reward_pools = safe_pools
data = Data('BL2')

# TPS
#reward_pools_challenges = [
#        'GD_CustomItemPools_MainGame.Rewards.BanditEpic',
#        'GD_CustomItemPools_MainGame.Rewards.BanditUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.BlueBold',
#        'GD_CustomItemPools_MainGame.Rewards.BlueNinja',
#        'GD_CustomItemPools_MainGame.Rewards.BluePattern',
#        'GD_CustomItemPools_MainGame.Rewards.CyanNinja',
#        'GD_CustomItemPools_MainGame.Rewards.CyanPale',
#        'GD_CustomItemPools_MainGame.Rewards.CyanPattern',
#        'GD_CustomItemPools_MainGame.Rewards.DahlEpic',
#        'GD_CustomItemPools_MainGame.Rewards.GreenBold',
#        'GD_CustomItemPools_MainGame.Rewards.GreenBoldAccent',
#        'GD_CustomItemPools_MainGame.Rewards.GreenPale',
#        'GD_CustomItemPools_MainGame.Rewards.Head005',
#        'GD_CustomItemPools_MainGame.Rewards.HyperionEpic',
#        'GD_CustomItemPools_MainGame.Rewards.HyperionUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.JakobsEpic',
#        'GD_CustomItemPools_MainGame.Rewards.JakobsUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.MaliwanEpic',
#        'GD_CustomItemPools_MainGame.Rewards.MaliwanUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.OrangePale',
#        'GD_CustomItemPools_MainGame.Rewards.OrangePattern',
#        'GD_CustomItemPools_MainGame.Rewards.PinkBold',
#        'GD_CustomItemPools_MainGame.Rewards.PinkPale',
#        'GD_CustomItemPools_MainGame.Rewards.PinkPandoracorn',
#        'GD_CustomItemPools_MainGame.Rewards.PurpleBold',
#        'GD_CustomItemPools_MainGame.Rewards.PurplePale',
#        'GD_CustomItemPools_MainGame.Rewards.RedPale',
#        'GD_CustomItemPools_MainGame.Rewards.RedPattern',
#        'GD_CustomItemPools_MainGame.Rewards.TedioreEpic',
#        'GD_CustomItemPools_MainGame.Rewards.TedioreUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.TorgueEpic',
#        'GD_CustomItemPools_MainGame.Rewards.TorgueUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.VladofEpic',
#        'GD_CustomItemPools_MainGame.Rewards.VladofUncommon',
#        'GD_CustomItemPools_MainGame.Rewards.YellowBoldAccent',
#        'GD_CustomItemPools_MainGame.Rewards.YellowPale',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin04',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin05',
#    ]
#reward_pools_missions = [
#        'GD_CustomItemPools_MainGame.Rewards.Black',
#        'GD_CustomItemPools_MainGame.Rewards.BlueBoldAccent',
#        'GD_CustomItemPools_MainGame.Rewards.BluePale',
#        'GD_CustomItemPools_MainGame.Rewards.GreenPattern',
#        'GD_CustomItemPools_MainGame.Rewards.Head003',
#        'GD_CustomItemPools_MainGame.Rewards.Head004',
#        'GD_CustomItemPools_MainGame.Rewards.PurpleDark',
#        'GD_CustomItemPools_MainGame.Rewards.SnickitSkin',
#        'GD_CustomItemPools_MainGame.Rewards.YellowPattern',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldHead02',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin08',
#        'GD_CustomItemPools_petunia.Rewards.PetuniaHeads',
#        'GD_CustomItemPools_petunia.Rewards.PetuniaSkins',
#    ]
#safe_pools = [
#        'GD_CustomItemPools_crocus.Rewards.BloodyHarvest',
#        'GD_CustomItemPools_crocus.Rewards.ManufacturerUnity',
#        'GD_CustomItemPools_crocus.Rewards.MercenaryDay',
#        'GD_CustomItemPools_crocus.Rewards.Pandoracorn',
#        'GD_CustomItemPools_MainGame.Rewards.Borderlands1Skin',
#        'GD_CustomItemPools_MainGame.Rewards.DigitalEdSkins',
#        'GD_CustomItemPools_MainGame.Rewards.Gearbox',
#        'GD_CustomItemPools_MainGame.Rewards.Gray',
#        'GD_CustomItemPools_Marigold.Rewards.CypressHead01',
#        'GD_CustomItemPools_Marigold.Rewards.CypressSkin01',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldHead07',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldHead08',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldHeadBoss',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin06',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin07',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin11',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin12',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin13',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin14',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin15',
#        'GD_CustomItemPools_Marigold.Rewards.MarigoldSkin16',
#    ]
##reward_pools = reward_pools_challenges + reward_pools_missions
##reward_pools = reward_pools_challenges
##reward_pools = reward_pools_missions
#reward_pools = safe_pools
#data = Data('TPS')

for pool in reward_pools:
    pool_struct = data.get_node_by_full_object(pool).get_structure()
    for item in pool_struct['BalancedItems']:
        innerpool = Data.get_struct_attr_obj(item, 'ItmPoolDefinition')
        print(innerpool)
