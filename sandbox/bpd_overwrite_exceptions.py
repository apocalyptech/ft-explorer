#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
from ftexplorer.data import Data

def compliment(number):
    """
    Returns a two's-compliment tuple for the given number.
    """
    number = int(number)
    one = (number >> 16)
    two = (number & 0xFF)
    return (one, two)

def get_named_vars(number, cvld_data):
    return_vars = set()
    (var_index, var_len) = compliment(number)
    for cvld_idx in range(var_index, var_index+var_len):
        cvld = cvld_data[cvld_idx]
        var_name = cvld['PropertyName']
        return_vars.add(var_name.strip('"').lower())

    return return_vars

data = Data('BL2')
objects = []
objects.extend(data.get_all_by_type('AIBehaviorProviderDefinition'))
objects.extend(data.get_all_by_type('BehaviorProviderDefinition'))

checks = {
        'behavior_delay_': set(['delay']),
        'behavior_randombranch_': set(['conditions']),
        'behavior_compare': set(['valuea', 'valueb', 'objecta', 'objectb', 'boolvalue', 'a', 'b']),
    }
check_keys = sorted(checks.keys())
correct = {}
false_positives = {}
for key in check_keys:
    correct[key] = []
    false_positives[key] = []

for (idx, bpd_name) in enumerate(objects):

    sys.stderr.write(str(idx))
    sys.stderr.write("\r")

    node = data.get_node_by_full_object(bpd_name)
    bpd = node.get_structure()

    for (seq_idx, seq) in enumerate(bpd['BehaviorSequences']):

        behavior_data = seq['BehaviorData2']
        cvld_data = seq['ConsolidatedVariableLinkData']

        for (behavior_idx, behavior) in enumerate(behavior_data):
            if behavior['Behavior'] != 'None':
                (behavior_type, behavior_class, junk) = behavior['Behavior'].split("'", 2)
                if behavior_class.lower().startswith(bpd_name.lower()):
                    behavior_class = behavior_class[len(bpd_name)+1:]
            else:
                continue

            class_lower = behavior_class.lower()
            class_matched = None
            for key in check_keys:
                if class_lower.startswith(key):
                    class_matched = key
                    break
            if not class_matched:
                continue

            report = '{}.{}'.format(bpd_name, behavior_class)
            named_vars = get_named_vars(
                    behavior['LinkedVariables']['ArrayIndexAndLength'],
                    cvld_data,
                    )

            if len(checks[class_matched] & named_vars) > 0:
                correct[class_matched].append(report)
            else:
                false_positives[class_matched].append(report)

print('', file=sys.stderr)
print('')
for key in check_keys:
    print('{}* w/ {}'.format(key, sorted(checks[key])))
    print('  Correct Hits: {}'.format(len(correct[key])))
    print('  False Positives: {}'.format(len(false_positives[key])))
    for fp in sorted(false_positives[key]):
        print('    * {}'.format(fp))
    print('')
