#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import sys
import subprocess
import re
import json

from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor, task
from twisted.python import log

log.startLogging(sys.stderr)

class TelnetEcho(TelnetProtocol):
    current_readings = None
    total_clients = 0
    password="somethinggoeshere"
    authenticated = False

    def connectionMade(self):
        self.client_id = self.__class__.total_clients
        self.__class__.total_clients += 1
        log.msg("client %r connected" % self.client_id)

    def connectionLost(self, reason):
        log.msg("client %r disconnected. %s" % (self.client_id, reason.getErrorMessage()))

    def enableRemote(self, option):
        log.msg("User tried to enable %r (I rejected it)\r\n" % (option,))
        return False

    def disableRemote(self, option):
        log.msg("User disabled %r\r\n" % (option,))

    def enableLocal(self, option):
        log.msg("User tried to make me enable %r (I rejected it)\r\n" % (option,))
        return False

    def disableLocal(self, option):
        log.msg("User asked me to disable %r\r\n" % (option,))

    def dataReceived(self, data):
        log.msg("Received \"%s\" from client %r" % (data, self.client_id))
        if (data.strip() == self.password):
            self.authenticated = True
            log.msg("Client %r authenticated." % (self.client_id,))
        elif self.authenticated == True:
            log.msg("Client %r tried to send data even after authenticated.\r\n" % (self.client_id,))

    def sendMonitorData(self):
        if self.authenticated == True:
            log.msg("sending some data to client %s" % self.client_id)
            self.transport.write(self.password)
        else:
            log.msg("cannot send date to client %s, not authenticated." % self.client_id)


class TelnetMonitorTransport(TelnetTransport):
    def connectionMade(self):
        TelnetTransport.connectionMade(self)
        self.factory.open_channels.append(self.protocol)

    def connectionLost(self, reason):
        self.factory.open_channels.remove(self.protocol)
        TelnetTransport.connectionLost(self, reason)

class TelnetMonitorFactory(ServerFactory):
    def __init__(self):
        self.open_channels = []
        self.protocol = lambda: TelnetMonitorTransport(TelnetEcho)

    def removeProtocol(self, protocol):
        self.open_channels.remove(protocol)

    def sendDataToAll(self):
        for channel in self.open_channels:
            channel.sendMonitorData()

if __name__ == '__main__':
    # read loop_time and port
    loop_time = 5.0
    port = 9125
    factory = TelnetMonitorFactory()
    l = task.LoopingCall(factory.sendDataToAll)
    l.start(loop_time)
    reactor.listenTCP(port, factory)
    reactor.run()
