#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# For Our Lord, &c.

from ftexplorer.data import Data
from modprocessor import ModProcessor

lines = []
lines.append('BL2')
lines.append('#<omg>')
lines.append('')

data = Data('BL2')
for (label, level) in data.get_levels():
    print('Processing {}'.format(label))
    lines.append('#<{}>'.format(label))
    lines.append('')
    for package in data.get_level_package_names(level):
        main_node = data.get_node_by_full_object(package)
        children = list(main_node.get_children_with_name('populationopportunitypoint'))
        children.extend(list(main_node.get_children_with_name('willowpopulationopportunitypoint')))
        for child in children:
            childstruct = child.get_structure()
            lines.append('  level {} set {}.{} SpawnAndCullRadius 999999999'.format(level, package, child))
            lines.append('')
    lines.append('')
    lines.append('#</{}>'.format(label))
    lines.append('')

lines.append('')
lines.append('#</omg>')

print('writing to ourlord.blcm')
mp = ModProcessor()
mp.human_str_to_blcm_filename("\n".join(lines), 'ourlord.blcm')
