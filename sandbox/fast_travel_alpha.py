#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

data = Data('TPS')
for ftdef in data.get_all_by_type('FastTravelStationDefinition'):
    ft = data.get_struct_by_full_object(ftdef)
    if ft['StationDisplayName'].startswith('The '):
        print('set {} StationDisplayName {}'.format(
            ftdef,
            ft['StationDisplayName'][4:],
            ))
