#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# For Our Lord, &c.

from ftexplorer.data import Data
from modprocessor import ModProcessor

data = Data('BL2')

lines = []
lines.append('BL2')
lines.append('#<omg>')
lines.append('')

# Loop through levels
for (label, level) in data.get_levels():
    lines.append('#<{}>'.format(label))
    lines.append('')
    for package in data.get_level_package_names(level):
        main_node = data.get_node_by_full_object(package)
        for soundvol in main_node.get_children_with_name('wwisesoundvolume'):
            soundvolstruct = soundvol.get_structure()
            if 'EnvironmentalEffects' in soundvolstruct and soundvolstruct['EnvironmentalEffects'] != '':
                for (idx, effect) in enumerate(soundvolstruct['EnvironmentalEffects']):
                    lines.append('level {} set {}.{} EnvironmentalEffects[{}].Effect None'.format(
                        level,
                        package,
                        soundvol.name,
                        idx
                        ))
                    lines.append('')
    lines.append('#</{}>'.format(label))
    lines.append('')

lines.append('')
lines.append('#</omg>')

print('writing to remove_wwise_audio_effects.blcm')
mp = ModProcessor()
mp.human_str_to_blcm_filename("\n".join(lines), 'remove_wwise_audio_effects.blcm')
