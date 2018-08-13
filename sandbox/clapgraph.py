#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data

data = Data('BL2')

base = 'Glacial_Dynamic.TheWorld:PersistentLevel.Main_Sequence.ClaptrapIntro'
start = '{}.SeqEvent_Console_0'.format(base)
#base = 'Grass_Cliffs_Combat.TheWorld:PersistentLevel.Main_Sequence.Episode11_Combat'
#start = '{}.WillowSeqEvent_MissionRemoteEvent_0'.format(base)

def go(object_name):
    global data
    global base
    obj = data.get_struct_by_full_object(object_name)
    (first, last) = object_name.rsplit('.', 1)
    print('  {};'.format(last))
    linkcount = 0
    if 'OutputLinks' in obj:
        ol = obj['OutputLinks']
        if ol and ol != '':
            for l in ol:
                if 'Links' in l:
                    links = l['Links']
                    if links and links != '':
                        for link in links:
                            op = Data.get_struct_attr_obj(link, 'LinkedOp')
                            if op.startswith(base):
                                print('  {} -> {} [taillabel={}];'.format(last, op[len(base)+1:], linkcount))
                                go(op)
                            else:
                                print('  {};'.format(op))
                                print('  {} -> {} [taillabel={}];'.format(last, op, linkcount))
                            linkcount += 1

print('digraph clap {')
print('  labelloc = "t";')
print('  fontsize = 25;')
print('  label = <{}>;'.format(start))
go(start)
print('}')
