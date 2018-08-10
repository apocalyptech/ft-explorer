#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

# So, I've seen this coming for awhile.  We've never actually handled quotes
# properly, and I've gotten away with it because nothing I've wanted to
# programmatically deal with has ever had a quoted comma in it.  Well,
# the BPD grapher finally came across one of those, specifically:
#
#   GD_Shields.Skills.Spike_Shield_Skill_CorrosiveLegendary:BehaviorProviderDefinition_0
#
# So, just a little util to trigger that parsing, so that I can finally
# address that.
#
# ... and actually, the "fix" for this probably only really handles one
# specific case.  I wouldn't be surprised if something else comes to bite
# me related to quotes again.

data = Data('TPS')
node = data.get_node_by_full_object('GD_Shields.Skills.Spike_Shield_Skill_CorrosiveLegendary:BehaviorProviderDefinition_0')
node_struct = node.get_structure()
print(node_struct)

