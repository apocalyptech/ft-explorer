#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

from ftexplorer.data import Data
from twisted.internet import protocol, reactor, endpoints

class FTExplorer(protocol.Protocol):

    def __init__(self, games):
        self.games = games

    def sendline(self, line):
        return self.transport.write("{}\n".format(line).encode('latin1'))

    def end(self):
        return self.sendline('EOM')

    def dataReceived(self, data):

        data = data.decode('latin1').strip().lower()

        if data == 'exit' or data == 'quit':
            self.transport.loseConnection()

        if data == '':
            for game in self.games.keys():
                self.sendline(game.upper())
            self.sendline('---')
            return self.end()

        if ' ' not in data:
            if data not in self.games:
                return self.end()
            node = self.games[data].top
        else:
            (game, other) = data.split(' ', 1)
            node = self.games[game].get_node_by_full_object(other)

        for child in sorted(node.children.values()):
            self.sendline(child.name)
        self.sendline('---')
        node.load()
        for line in node.data:
            self.sendline(line)
        return self.end()

class FTExplorerFactory(protocol.Factory):

    gamelist = ['BL2', 'TPS']

    def __init__(self):

        print('Initializing...')
        self.games = {}
        for game in self.gamelist:
            self.games[game.lower()] = Data(game)
        print('Done.')

    def buildProtocol(self, addr):
        return FTExplorer(self.games)

endpoints.serverFromString(reactor, "tcp:interface=127.0.0.1:port=21212").listen(FTExplorerFactory())
reactor.run()
