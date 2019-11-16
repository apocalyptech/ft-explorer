#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

run_station_check = False
#game = 'BL2'
game = 'TPS'
input_file = 'save_index_{}.txt'.format(game.lower())

data = Data(game)

# Get a list of all the last-visited locations
locations = {}
for obj_type in ['FastTravelStationDefinition', 'LevelTravelStationDefinition']:
    for obj_name in data.get_all_by_type(obj_type):
        obj_struct = data.get_struct_by_full_object(obj_name)
        (_, identifier) = obj_name.rsplit('.', 1)
        if obj_struct['StationLevelName'] != 'None':
            if run_station_check and identifier.lower() in locations:
                print('Overwriting {}: {} -> {}'.format(
                    identifier.lower(),
                    locations[identifier.lower()],
                    obj_struct['StationLevelName'].lower(),
                    ))
            if run_station_check and game == 'TPS' and identifier.lower() == 'cliffs':
                print('Warning: "cliffs" found in TPS...')
            locations[identifier.lower()] = obj_struct['StationLevelName'].lower()
if run_station_check:
    sys.exit(1)

# Get a list of mission objects to names
missions = {}
for obj_name in data.get_all_by_type('MissionDefinition'):
    obj_struct = data.get_struct_by_full_object(obj_name)
    missions[obj_name.lower()] = obj_struct['MissionName']

# Flip our data level dict so we can go from level ID to name
levels = {}
for (name, identifier) in data.levels[game]:
    if name == 'Sanctuary (pre liftoff)' or name == 'Sanctuary (post liftoff)':
        name = 'Sanctuary'
    levels[identifier.lower()] = name

with open(input_file) as df:
    idx = 0
    for line in df:
        (filename, last_visited, active_mission_list, turnin_mission_list) = line.strip().split('|')
        if active_mission_list == '':
            active_missions = []
        else:
            active_missions = active_mission_list.split(',')
        if turnin_mission_list == '':
            turnin_missions = []
        else:
            turnin_missions = turnin_mission_list.split(',')
        print('<tr class="row{}">'.format(idx % 2))
        print('<td class="filename"><a href="{}/{}">{}</a></td>'.format(game.lower(), filename, filename))
        # Some hardcoding here; I have no idea how to properly distinguish between GD_FastTravelStations.Zone2.Cliffs
        # and GD_Sage_FastTravel.Cliffs, though fortunately my file naming convention lets me fudge it.
        if last_visited.lower() == 'cliffs':
            if 'dlc3' in filename:
                print('<td class="in_map">{}</td>'.format(levels['sage_cliffs_p']))
            else:
                print('<td class="in_map">{}</td>'.format(levels['grass_cliffs_p']))
        else:
            print('<td class="in_map">{}</td>'.format(levels[locations[last_visited.lower()]]))
        if len(active_missions) > 0:
            print('<td class="active_missions">')
            print('<ul>')
            for name in active_missions:
                print('<li>{}</li>'.format(missions[name.lower()]))
            print('</ul>')
            print('</td>')
        else:
            print('<td class="empty_missions">&nbsp;</td>')
        if len(turnin_missions) > 0:
            print('<td class="turnin_missions">')
            print('<ul>')
            for name in turnin_missions:
                print('<li>{}</li>'.format(missions[name.lower()]))
            print('</ul>')
            print('</td>')
        else:
            print('<td class="empty_missions">&nbsp;</td>')
        print('</tr>')
        idx += 1

