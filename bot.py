# This script is under GPL License v2
# (c) Jean-Michel LACROIX 2006 (jm-lacroix@savigny.org)
# (c) Moviuro 2015 (moviuro+ircbot@gmail.com)

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import thread, os, time

MyChannel = 'mychannel'			# Channel name without '#'
MyIRCServer = 'myserver'		# Channel server
MyIRCPort = 6697			# Channel server port
MyPipe = '/usr/home/ircbot/pipe'	# The path to the named pipe
MyBotName = 'ircbot'			# Name of the bot

# system imports
import time, sys

def recupere_pipe(bot = None):
    f=open(MyPipe,'r')
    print "RecPipe"
    while 1:
        time.sleep(0.1)
        li = f.read()
        if not li: continue
        bot.msg('#' + MyChannel, li[:-1])
        print li


class LogBot(irc.IRCClient):
    """A logging IRC bot."""

    nickname = MyBotName

    def connectionMade(self):
        self.thread = thread.start_new_thread(recupere_pipe, (self,))
        irc.IRCClient.connectionMade(self)
        

    def connectionLost(self, reason):
        self.thread.exit()
        irc.IRCClient.connectionLost(self, reason)

    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        pass

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        #self.logger.log("<%s> %s" % (user, msg))

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I am a log bot" % user
            self.msg(channel, msg)
            #self.logger.log("<%s> %s" % (self.nickname, msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        #self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        #self.logger.log("%s is now known as %s" % (old_nick, new_nick))


class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = LogBot

    def __init__(self, channel):
        self.channel = channel

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    # create factory protocol and application
    f = LogBotFactory(MyChannel) 

    # connect factory to this host and port
    reactor.connectTCP(MyIRCServer, MyiIRCPort, f)

    # run bot
    reactor.run()

