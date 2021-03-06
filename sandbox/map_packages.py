#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# For generating 'level_pkgs' for the DataDumper pythonsdk mod

from ftexplorer.data import Data

data = Data('TPS')
for (english_name, main_package) in data.get_levels():
    print("'{}': [".format(main_package))
    for inner_pkg in data.get_level_package_names(main_package):
        print("        '{}',".format(inner_pkg.split('.')[0]))
    print('    ],')
