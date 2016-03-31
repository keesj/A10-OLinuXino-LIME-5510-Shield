from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import re
import logging

class MyFlasher(protocol.ProcessProtocol):
    def __init__(self, command):
        self.command = command
        self.data = ""
	self.is_done = 0
	self.logger = logging.getLogger(__name__)

    def connectionMade(self):
        self.transport.closeStdin() # tell them we're done

    def outReceived(self, data):
	self.logger.debug(data)

    def errReceived(self, data):
	self.logger.debug(data)

#    def inConnectionLost(self):
#        print "inConnectionLost! stdin is closed! (we probably did it)"

#    def outConnectionLost(self):
#        print "outConnectionLost! The child closed their stdout!"
        # now is the time to examine what they wrote
        #print "I saw them write:", self.data
        #print "I saw %s lines" % lines

#    def errConnectionLost(self):
#        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        self.logger.info("processExited, status %d" % (reason.value.exitCode))
	self.is_done = 1

    def processEnded(self, reason):
        self.logger.info("processEnded, status %d" % (reason.value.exitCode))
	self.is_done = 1
        #reactor.stop()

#pp = MyFlasher("./flash.sh")


#reactor.spawnProcess(pp, "./flash.sh", ["flash"], {})
#reactor.run()
