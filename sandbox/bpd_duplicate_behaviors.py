#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import sys
import struct
from ftexplorer.data import Data

# Finds BPDs with multiple BehaviorSequences, where the same Behavior
# is used in more than one of those BehaviorSequences


def parse_arrayindexandlength(number):
    """
    Returns an array index and length tuple for the given number.
    """
    # Could just use >> and & for this, but since we have to be more
    # careful with LinkIdAndLinkedBehavior anyway, since that one's
    # weirder, we may as well just use struct here, as well.
    number = int(number)
    byteval = struct.pack('>i', number)
    return struct.unpack('>HH', byteval)

def parse_linkidandlinkedbehavior(number):
    """
    Returns a link ID index and behavior tuple for the given number.
    """
    number = int(number)
    byteval = struct.pack('>i', number)
    (linkid, junk, behavior) = struct.unpack('>bbH', byteval)
    return (linkid, behavior)

def follow(link, cold_data, behavior_data, seq_idx, cold_followed):
    """
    Follows the given `link` (being a compound number of the sort
    found in BPDs) through the given `behavior_data`, using `cold_data`
    as the glue.  `seq_idx` is our current BPD index.
    """
    to_ret = set()
    (link_index, link_length) = parse_arrayindexandlength(link)
    for (cold_order_idx, cold_index) in enumerate(range(link_index, link_index+link_length)):
        full_cold_index = '{}_{}'.format(seq_idx, cold_index)
        if full_cold_index in cold_followed:
            continue
        else:
            cold_followed.add(full_cold_index)
        try:
            cold = cold_data[cold_index]
        except IndexError:
            return to_ret
        (link_id, bindex) = parse_linkidandlinkedbehavior(cold['LinkIdAndLinkedBehavior'])
        behavior = behavior_data[bindex]
        to_ret.add(Data.get_struct_attr_obj(behavior, 'Behavior'))
        to_ret |= follow(behavior['OutputLinks']['ArrayIndexAndLength'],
            cold_data,
            behavior_data,
            seq_idx,
            cold_followed,
            )
    return to_ret


for game in ['BL2', 'TPS']:
    data = Data(game)
    bpd_names = []
    bpd_names.extend(data.get_all_by_type('BehaviorProviderDefinition'))
    bpd_names.extend(data.get_all_by_type('AIBehaviorProviderDefinition'))
    max_len = 0
    for bpd_name in sorted(bpd_names):

        if len(bpd_name) > 120:
            report_str = '{}...'.format(bpd_name[:117])
        else:
            report_str = bpd_name
        max_len = max(max_len, len(report_str))
        spaces = max_len - len(report_str)
        sys.stdout.write("{} {}{}\r".format(game, report_str, ' '*spaces))

        bpd = data.get_struct_by_full_object(bpd_name)

        process = False
        if len(bpd['BehaviorSequences']) > 1:
            seqs_with_events = 0
            for bs in bpd['BehaviorSequences']:
                if len(bs['EventData2']) > 0:
                    seqs_with_events += 1
            if seqs_with_events > 1:
                process = True

        if process:
            behaviors_used = {}
            cold_followed = set()
            for bs_idx, bs in enumerate(bpd['BehaviorSequences']):

                event_data = bs['EventData2']
                behavior_data = bs['BehaviorData2']
                cold_data = bs['ConsolidatedOutputLinkData']

                bpds_seen = set()

                for event_idx, event in enumerate(event_data):
                    bpds_seen |= follow(event['OutputLinks']['ArrayIndexAndLength'],
                        cold_data,
                        behavior_data,
                        bs_idx,
                        cold_followed,
                        )

                for bpd_name in bpds_seen:
                    if bpd_name not in behaviors_used:
                        behaviors_used[bpd_name] = 1
                    else:
                        behaviors_used[bpd_name] += 1

                #print('{}, BS {}'.format(bpd_name, bs_idx))
                #print(bpds_seen)

            for behavior, count in behaviors_used.items():
                if count > 1:
                    print('')
                    print('{} used {} times'.format(behavior, count))

print('')
print('Done!')
