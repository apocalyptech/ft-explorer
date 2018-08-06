#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:
import re
import sys
from ftexplorer.data import Data

# What to inspect
control = {
        'BL2': [
            ('Arid Nexus - Badlands', 'Stockade_P'),
            ('Arid Nexus - Boneyard', 'Fyrestone_P'),
            ('Bloodshot Ramparts', 'DamTop_P'),
            ('Bloodshot Stronghold', 'Dam_P'),
            ('Bunker', 'Boss_Cliffs_P'),
            ('Caustic Caverns', 'Caverns_P'),
            ('Control Core Angel', 'VOGChamber_P'),
            ('Dust', 'Interlude_P'),
            ('End of the Line', 'TundraTrain_P'),
            ('Eridium Blight', 'Ash_P'),
            ('Fink\'s Slaughterhouse', 'BanditSlaughter_P'),
            ('Fridge', 'Fridge_P'),
            ('Friendship Gulag', 'HypInterlude_P'),
            ('Frostburn Canyon', 'IceCanyon_P'),
            ('Hero\'s Pass', 'FinalBossAscent_P'),
            ('Highlands Outwash', 'Outwash_P'),
            ('Highlands', 'Grass_P'),
            ('Holy Spirits', 'Luckys_P'),
            ('Lynchwood', 'Grass_Lynchwood_P'),
            ('Natural Selection Annex', 'CreatureSlaughter_P'),
            ('Opportunity', 'HyperionCity_P'),
            ('Ore Chasm', 'RobotSlaughter_P'),
            ('Sanctuary (post liftoff)', 'SanctuaryAir_P'),
            ('Sanctuary (pre liftoff)', 'Sanctuary_P'),
            ('Sanctuary Hole', 'Sanctuary_Hole_P'),
            ('Sawtooth Cauldron', 'CraterLake_P'),
            ('Southern Shelf - Bay', 'Cove_P'),
            ('Southern Shelf', 'SouthernShelf_P'),
            ('Southpaw Steam + Power', 'SouthpawFactory_P'),
            ('Terramorphous Peak', 'ThresherRaid_P'),
            ('Thousand Cuts', 'Grass_Cliffs_P'),
            ('Three Horns Divide', 'Ice_P'),
            ('Three Horns Valley', 'Frost_P'),
            ('Tundra Express', 'TundraExpress_P'),
            ('Vault of the Warrior', 'Boss_Volcano_P'),
            ('Wildlife Exploitation Preserve', 'PandoraPark_P'),
            ('Windshear Waste', 'Glacial_P'),
            ('Hayter\'s Folly', 'Orchid_Caves_P'),
            ('Leviathan\'s Lair', 'Orchid_WormBelly_P'),
            ('Magnys Lighthouse', 'Orchid_Spire_P'),
            ('Oasis', 'Orchid_OasisTown_P'),
            ('Rustyards', 'Orchid_ShipGraveyard_P'),
            ('Washburne Refinery', 'Orchid_Refinery_P'),
            ('Wurmwater', 'Orchid_SaltFlats_P'),
            ('Arena (final boss)', 'Iris_DL1_TAS_P'),
            ('Arena', 'Iris_DL1_P'),
            ('Badass Crater Bar', 'Iris_Moxxi_P'),
            ('Badass Crater of Badassitude', 'Iris_Hub_P'),
            ('Beatdown', 'Iris_DL2_P'),
            ('Forge', 'Iris_DL3_P'),
            ('Pyro Pete\'s Bar', 'Iris_DL2_Interior_P'),
            ('Southern Raceway', 'Iris_Hub2_P'),
            ('Ardorton Station', 'Sage_PowerStation_P'),
            ('Candlerakk\'s Crag', 'Sage_Cliffs_P'),
            ('H.S.S. Terminus', 'Sage_HyperionShip_P'),
            ('Hunter\'s Grotto', 'Sage_Underground_P'),
            ('Scylla\'s Grove', 'Sage_RockForest_P'),
            ('Dark Forest', 'Dark_Forest_P'),
            ('Dragon Keep', 'CastleKeep_P'),
            ('Flamerock Refuge', 'Village_P'),
            ('Hatred\'s Shadow', 'CastleExterior_P'),
            ('Immortal Woods', 'Dead_Forest_P'),
            ('Lair of Infinite Agony', 'Dungeon_P'),
            ('Mines of Avarice', 'Mines_P'),
            ('Murderlin\'s Temple', 'TempleSlaughter_P'),
            ('Unassuming Docks', 'Docks_P'),
            ('Winged Storm', 'DungeonRaid_P'),
            ('Raid on Digistruct Peak', 'TestingZone_P'),
            ('Hallowed Hollow', 'Pumpkin_Patch_P'),
            ('Gluttony Gulch', 'Hunger_P'),
            ('Marcus\'s Mercenary Shop', 'Xmas_P'),
            ('Rotgut Distillery', 'Distillery_P'),
            ('Wam Bam Island', 'Easter_P'),
            ],
        'TPS': [
            ('Abandoned Training Facility', 'MoonSlaughter_P'),
            ('Concordia', 'Spaceport_P'),
            ('Crisis Scar', 'ComFacility_P'),
            ('Eleseer', 'InnerCore_P'),
            ('Eye of Helios', 'LaserBoss_P'),
            ('Helios Station', 'MoonShotIntro_P'),
            ('Hyperion Hub of Heroism', 'CentralTerminal_P'),
            ('Jack\'s Office', 'JacksOffice_P'),
            ('Lunar Launching Station', 'Laser_P'),
            ('Meriff\'s Office', 'Meriff_P'),
            ('Outfall Pumping Station', 'Digsite_Rk5arena_P'),
            ('Outlands Canyon', 'Outlands_P2'),
            ('Outlands Spur', 'Outlands_P'),
            ('Pity\'s Fall', 'Wreck_P'),
            ('Regolith Range', 'Deadsurface_P'),
            ('Research and Development', 'RandDFacility_P'),
            ('Serenity\'s Waste', 'Moonsurface_P'),
            ('Stanton\'s Liver', 'StantonsLiver_P'),
            ('Sub-Level 13', 'Sublevel13_P'),
            ('Titan Industrial Facility', 'DahlFactory_P'),
            ('Titan Robot Production Plant', 'DahlFactory_Boss'),
            ('Triton Flats', 'Moon_P'),
            ('Tycho\'s Ribs', 'Access_P'),
            ('Veins of Helios', 'InnerHull_P'),
            ('Vorago Solitude', 'Digsite_P'),
            ('Cluster 00773 P4ND0R4', 'Ma_LeftCluster_P'),
            ('Cluster 99002 0V3RL00K', 'Ma_RightCluster_P'),
            ('Cortex', 'Ma_SubBoss_P'),
            ('Deck 13 1/2', 'Ma_Deck13_P'),
            ('Deck 13.5', 'Ma_FinalBoss_P'),
            ('Motherlessboard', 'Ma_Motherboard_P'),
            ('Nexus', 'Ma_Nexus_P'),
            ('Subconscious', 'Ma_Subconscious_P'),
            ('Holodome', 'Eridian_Slaughter_P'),
            ],
    }

# mook
#control = {
#        'BL2': [
#            ('Highlands', 'Grass_P'),
#            ],
#        }

popdefs = {}
def get_spawns_from_popdef(popdef_name, data):

    global popdefs
    if popdef_name in popdefs:
        return popdefs[popdef_name]

    popdef_set = set()
    popdef_struct = data.get_node_by_full_object(popdef_name).get_structure()
    for archetype in popdef_struct['ActorArchetypeList']:
        if archetype['SpawnFactory'] != 'None':
            spawnfactory_name = archetype['SpawnFactory'].split("'", 2)[1]
            sf_struct = data.get_node_by_full_object(spawnfactory_name).get_structure()
            if 'PawnBalanceDefinition' in sf_struct:
                if sf_struct['PawnBalanceDefinition'] != 'None':
                    popdef_set.add(sf_struct['PawnBalanceDefinition'].split("'", 2)[1])
            elif 'PopulationDef' in sf_struct:
                new_popdef_name = sf_struct['PopulationDef'].split("'", 2)[1]
                popdef_set = popdef_set.union(get_spawns_from_popdef(new_popdef_name, data))
            elif 'WillowAIPawnArchetype' in sf_struct:
                # This is weird, might be just for mission NPCs...
                popdef_set.add('({})'.format(sf_struct['WillowAIPawnArchetype'].split("'", 2)[1]))
            elif 'VehicleArchetype' in sf_struct:
                popdef_set.add(sf_struct['VehicleArchetype'].split("'", 2)[1])
            elif 'ObjectBalanceDefinition' in sf_struct:
                pass
            else:
                raise Exception('Not sure what to do: {}'.format(spawnfactory_name))

    popdefs[popdef_name] = popdef_set
    return popdef_set

for game, levelnames in control.items():
    popdefs = {}
    print('Processing {}'.format(game))
    print('==============')
    print('')
    data = Data(game)
    for (english, levelname) in levelnames:
        
        # Get the info on what objects we need to load.
        level_packages = ['{}.TheWorld:PersistentLevel'.format(levelname)]
        node = data.get_node_by_full_object('{}.TheWorld'.format(levelname))
        for childname, child in node.children.items():
            if childname[:14].lower() == 'levelstreaming':
                childstruct = child.get_structure()
                if childstruct['LoadedLevel'] != 'None':
                    level_packages.append(childstruct['LoadedLevel'].split("'", 2)[1])

        # Report
        #print(levelname)
        #for package in level_packages:
        #    print(' * {}'.format(package))
        #print('')

        # Now loop through 'em to get all the population definitions
        dens = {}
        for package in level_packages:
            package_obj = data.get_node_by_full_object(package)
            for childname, child in package_obj.children.items():
                if childname[:24].lower() == 'populationopportunityden':
                    childstruct =  child.get_structure()
                    if childstruct != {}:
                        if childstruct['PopulationDef'] != 'None':
                            popdef = childstruct['PopulationDef'].split("'", 2)[1]
                            if popdef not in dens:
                                dens[popdef] = 0
                            dens[popdef] += 1

        # Report
        #print(levelname)
        #for popdef, count in sorted(dens.items()):
        #    print(' * {}x {}'.format(count, popdef))
        #print('')

        # Loop through our found dens and find out what things may spawn
        possible_spawns = set()
        for popdef_name in dens.keys():
            for spawn in get_spawns_from_popdef(popdef_name, data):
                possible_spawns.add(spawn)

        # Report
        print('{} ({})'.format(english, levelname))
        for spawn in sorted(possible_spawns):
            print(' * {}'.format(spawn))
        print('')

    print('')
