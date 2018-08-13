#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

# Attempts to find some cases where we might have a BPD -> Seq -> BPD link.
# *shudder*

data = Data('BL2')

# First gather our BPD EventName mappings
print('Gathering BPD EventName mappings')
bpd_events = {}
events_bpd = {}
for bpd_name in sorted(data.get_all_by_type('BehaviorProviderDefinition')):
    bpd_events[bpd_name.lower()] = set()
    bpd_struct = data.get_struct_by_full_object(bpd_name)
    if 'BehaviorSequences' in bpd_struct and bpd_struct['BehaviorSequences'] != '':
        for seq in bpd_struct['BehaviorSequences']:
            if 'EventData2' in seq and seq['EventData2'] != '':
                for event in seq['EventData2']:
                    event_name = event['UserData']['EventName'].replace('"', '')
                    if event_name.lower() not in events_bpd:
                        events_bpd[event_name.lower()] = set()
                    events_bpd[event_name.lower()].add(bpd_name.lower())
                    bpd_events[bpd_name.lower()].add(event_name.lower())

# Now gather our Kismet EventName mappings
print('Gathering Kismet EventName mappings')
kismet_events = {}
events_kismet = {}
for kismet_name in sorted(data.get_all_by_type('SeqEvent_RemoteEvent')):
    (first, junk) = kismet_name.rsplit('.', 1)
    first = first.lower()
    if first not in kismet_events:
        kismet_events[first] = set()
    kismet_struct = data.get_struct_by_full_object(kismet_name)
    event_name = kismet_struct['EventName'].lower()
    kismet_events[first].add(event_name)
    if event_name not in events_kismet:
        events_kismet[event_name] = set()
    events_kismet[event_name].add(first)

# Now gather BPD->EventName and Kismet->EventName links
print('Gathering BPD->EventName and Kismet->EventName links')
bpd_to_events = {}
kismet_to_events = {}
objects = []
objects.extend(data.get_all_by_type('Behavior_RemoteEvent'))
objects.extend(data.get_all_by_type('Behavior_CustomEvent'))
objects.extend(data.get_all_by_type('Behavior_RemoteCustomEvent'))
for obj_name in sorted(objects):
    obj_struct = data.get_struct_by_full_object(obj_name)
    if 'Behavior_RemoteEvent' in obj_name:
        varname = 'EventName'
    else:
        varname = 'CustomEventName'
    if varname in obj_struct:
        event_name = obj_struct[varname].lower()
        if 'BehaviorProviderDefinition' in obj_name:
            # Ignore remotecustomevents, since they only ever point back to
            # ourselves.
            if 'Behavior_RemoteCustomEvent' in obj_name:
                continue
            to_dict = bpd_to_events
            (base_obj, rest) = obj_name.lower().rsplit('.', 1)
        elif ':PersistentLevel' in obj_name:
            # At the moment, I'm looking at these per type
            #if 'Behavior_RemoteCustomEvent' not in obj_name:
            #if 'Behavior_CustomEvent' not in obj_name:
            if 'Behavior_RemoteEvent' not in obj_name:
                continue
            to_dict = kismet_to_events
            (base_obj, rest1, rest2) = obj_name.lower().rsplit('.', 2)
        else:
            # This is probably a mission behavior or something, we haven't
            # looked into that yet.
            continue
        if base_obj not in to_dict:
            to_dict[base_obj] = set()
        to_dict[base_obj].add(event_name)

# Grab SeqAct_ActivateRemoteEvent objects, make sure these are good.
print('Gathering SeqAct remote event activations') 
seqact_to_events = {}
events_to_seqact = {}
for seqact_name in sorted(data.get_all_by_type('SeqAct_ActivateRemoteEvent')):
    seqact_name_lower = seqact_name.lower()
    (first, junk) = seqact_name_lower.rsplit('.', 1)
    seqact = data.get_struct_by_full_object(seqact_name)
    event_name = seqact['EventName'].lower()
    if first not in seqact_to_events:
        seqact_to_events[first] = set()
    seqact_to_events[first].add(event_name)
    if event_name not in events_to_seqact:
        events_to_seqact[event_name] = set()
    events_to_seqact[event_name].add(first)

# And now we should be able to try and find some possibilities.
print('Looking for matches...')

# Original - looking for BPD -> Kismet -> BPD links
if False:
    for bpd in sorted(bpd_to_events.keys()):
        for bpd_event in sorted(bpd_to_events[bpd]):
            if bpd_event in events_kismet:
                for kismet in sorted(events_kismet[bpd_event]):
                    if kismet in kismet_to_events:
                        for kismet_event in sorted(kismet_to_events[kismet]):
                            if kismet_event in events_bpd:
                                for return_bpd in sorted(events_bpd[kismet_event]):
                                    if return_bpd == bpd:
                                        print('{} ({}) -> {} ({}) -> {}'.format(
                                            bpd, bpd_event,
                                            kismet, kismet_event,
                                            return_bpd,
                                            ))

# Looking for Kismets which link to themselves with CustomEvents
if False:
    for kismet in sorted(kismet_to_events.keys()):
        for kismet_event in sorted(kismet_to_events[kismet]):
            if kismet_event in events_kismet:
                for dest_kismet in events_kismet[kismet_event]:
                    print('{} ({}) -> {}'.format(kismet, kismet_event, dest_kismet))

# Looking for seqact links from BPD -> Kismet -> BPD
if False:
    for bpd in sorted(bpd_to_events.keys()):
        for bpd_event in sorted(bpd_to_events[bpd]):
            if bpd_event in events_kismet:
                for kismet in sorted(events_kismet[bpd_event]):
                    if kismet in seqact_to_events:
                        for kismet_event in sorted(seqact_to_events[kismet]):
                            if kismet_event in events_bpd:
                                for return_bpd in sorted(events_bpd[kismet_event]):
                                    if return_bpd == bpd:
                                        print('{} ({}) -> {} ({}) -> {}'.format(
                                            bpd, bpd_event,
                                            kismet, kismet_event,
                                            return_bpd,
                                            ))

# Looking for seqacts which link to their own kismet
if True:
    for kismet in sorted(seqact_to_events.keys()):
        for kismet_event in sorted(seqact_to_events[kismet]):
            if kismet_event in events_kismet:
                for dest_kismet in events_kismet[kismet_event]:
                    print('{} ({}) -> {}'.format(kismet, kismet_event, dest_kismet))
