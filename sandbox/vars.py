#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2018, CJ Kucera
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from ftexplorer.data import Data

data = Data('BL2')

for (name, streaming_obj, player_obj) in [
        ('Axton', 'GD_Soldier_Streaming.Pawn_Soldier', 'GD_Soldier.Character.CharClass_Soldier'),
        ('Gaige', 'GD_Tulip_Mechro_Streaming.Pawn_Mechromancer', 'GD_Tulip_Mechromancer.Character.CharClass_Mechromancer'),
        ('Krieg', 'GD_Lilac_Psycho_Streaming.Pawn_LilacPlayerClass', 'GD_Lilac_PlayerClass.Character.CharClass_LilacPlayerClass'),
        ('Maya', 'GD_Siren_Streaming.Pawn_Siren', 'GD_Siren.Character.CharClass_Siren'),
        ('Salvador', 'GD_Mercenary_Streaming.Pawn_Mercenary', 'GD_Mercenary.Character.CharClass_Mercenary'),
        ('Zero', 'GD_Assassin_Streaming.Pawn_Assassin', 'GD_Assassin.Character.CharClass_Assassin'),
        ]:

    print('{}:'.format(name))
    struct_streaming = data.get_node_by_full_object(streaming_obj).get_structure()
    struct_player = data.get_node_by_full_object(player_obj).get_structure()
    print(' * Player GroundSpeed: {}'.format(struct_player['GroundSpeed']))
    print(' * Streaming GroundSpeed: {}'.format(struct_streaming['GroundSpeed']))
    print(' * Streaming GroundSpeedBaseValue: {}'.format(struct_streaming['GroundSpeedBaseValue']))
    print(' * Player AirSpeed: {}'.format(struct_player['AirSpeed']))
    print(' * Streaming AirSpeed: {}'.format(struct_streaming['AirSpeed']))
    print(' * Streaming AirSpeedBaseValue: {}'.format(struct_streaming['AirSpeedBaseValue']))
    print(' * Player JumpZ: {}'.format(struct_player['JumpZ']))
    print(' * Streaming JumpZ: {}'.format(struct_streaming['JumpZ']))
    print(' * Streaming JumpZBaseValue: {}'.format(struct_streaming['JumpZBaseValue']))
    print(' * Player CrouchedPct: {}'.format(struct_player['CrouchedPct']))
    print(' * Streaming CrouchedPct: {}'.format(struct_streaming['CrouchedPct']))
    print('')


struct = data.get_node_by_full_object('GD_PlayerShared.injured.PlayerInjuredDefinition').get_structure()
print('Global InjuredMovementSpeed: {}'.format(struct['InjuredMovementSpeed']))
struct = data.get_node_by_full_object('GD_Globals.General.Globals').get_structure()
print('Global PlayerAirControl: {}'.format(struct['PlayerAirControl']))
print('')
