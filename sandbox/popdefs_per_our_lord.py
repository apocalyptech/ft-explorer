#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# For Our Lord, &c.

from ftexplorer.data import Data
from modprocessor import ModProcessor

zones = [
        ('Spawn Zone 1', 'GD_Orchid_RakkHive.Animation.Anim_RakkHive_Shake:BehaviorProviderDefinition_0.Behavior_AISpawn_43'),
        ('Spawn Zone 2', 'GD_Orchid_RakkHive.Animation.Anim_RakkHive_Shake:BehaviorProviderDefinition_0.Behavior_AISpawn_44'),
        ('Spawn Zone 3', 'GD_Orchid_RakkHive.Animation.Anim_RakkHive_Shake:BehaviorProviderDefinition_0.Behavior_AISpawn_45'),
        ('Spawn Zone 4', 'GD_Orchid_RakkHive.Animation.Anim_RakkHive_Shake:BehaviorProviderDefinition_0.Behavior_AISpawn_46'),
        ]

popdefs_per_level = {}
popdef_short_names = {}

data = Data('BL2')

# First figure out which popdefs are in which levels
for (label, level) in data.get_levels():
    popdefs_per_level[level] = set()
    for package in data.get_level_package_names(level):
        main_node = data.get_node_by_full_object(package)
        for worldinfo in main_node.get_children_with_name('worldinfo'):
            worldstruct = worldinfo.get_structure()
            if 'ClientDestroyedActorContent' in worldstruct:
                for content in worldstruct['ClientDestroyedActorContent']:
                    if content.startswith('WillowPopulationDefinition'):
                        popdefs_per_level[level].add(content)
                        popdef_short_names[content] = None

# Pre-process the "short" popdef names that we'll use in the categories
for popdef_name in popdef_short_names.keys():
    (_, obj_name, _) = popdef_name.split("'")
    last_component = obj_name.split('.')[-1]
    if last_component.startswith('PopDef_'):
        popdef_short_names[popdef_name] = last_component[7:]
    else:
        popdef_short_names[popdef_name] = last_component

# Okay, we're ready to actually generate.

lines = []
lines.append('BL2')
lines.append('#<omg>')
lines.append('')

def sortkey_popdef(full_name):
    global popdef_short_names
    return popdef_short_names[full_name]

for (level_label, level_name) in data.get_levels():

    if level_name in popdefs_per_level:

        lines.append('#<{}>'.format(level_label))
        lines.append('')

        for (zone_label, zone_obj) in zones:

            lines.append('#<{}><mut>'.format(zone_label))
            lines.append('')

            for popdef_full in sorted(popdefs_per_level[level_name], key=sortkey_popdef):
                popdef_short = popdef_short_names[popdef_full]
                lines.append('#<{}>'.format(popdef_short))
                lines.append('')

                lines.append('level {} set {} PopDef {}'.format(
                    level_name,
                    zone_obj,
                    popdef_full,
                    ))
                lines.append('')

                lines.append('#</{}>'.format(popdef_short))
                lines.append('')

            lines.append('#</{}>'.format(zone_label))
            lines.append('')

        lines.append('#</{}>'.format(level_label))
        lines.append('')

lines.append('')
lines.append('#</omg>')

print('writing to ourlord3.blcm')
mp = ModProcessor()
mp.human_str_to_blcm_filename("\n".join(lines), 'ourlord3.blcm')
