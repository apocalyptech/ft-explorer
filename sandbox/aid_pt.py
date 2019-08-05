#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Trying to find references to D_Attributes.Balance.PlayThroughCount inside
# AttributeInitializationDefinition objects which reference something other
# than 1 and 2.

from ftexplorer.data import Data, Weight

data = Data('BL2')

for aid_name in sorted(data.get_all_by_type('AttributeInitializationDefinition')):
    aid = data.get_struct_by_full_object(aid_name)
    ci = aid['ConditionalInitialization']
    if ci['bEnabled'] == 'True':
        for ce in ci['ConditionalExpressionList']:
            for exp in ce['Expressions']:
                if 'PlayThroughCount' in exp['AttributeOperand1']:
                    numval = float(exp['ConstantOperand2'])
                    if numval != 1 and numval != 2:
                        print('{}: {}'.format(aid_name, numval))
                    elif numval == 2:
                        print('{} - 2'.format(aid_name))
