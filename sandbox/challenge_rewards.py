#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

#data = Data('BL2')
data = Data('TPS')

affected = {}
for challenge_def in data.get_all_by_type('ChallengeDefinition'):
    challenge_struct = data.get_node_by_full_object(challenge_def).get_structure()
    if 'Levels' in challenge_struct:
        for (idx, level) in enumerate(challenge_struct['Levels']):
            reward = Data.get_struct_attr_obj(level, 'RewardItemPool')
            if reward:
                affected[reward] = (
                        challenge_struct['ChallengeName'],
                        challenge_struct['Description'],
                        idx + 1,
                        )

print('Pool | Name | Level | Description')
print('--- | --- | --- | ---')
for reward in sorted(affected.keys()):
    (name, desc, num) = affected[reward]
    print('`{}` | {} | {} | {}'.format(reward, name, num, desc))
