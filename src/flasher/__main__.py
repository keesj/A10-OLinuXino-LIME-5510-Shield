#
# Flahser
#
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


import usb_handler
import flash_handler
import ssh_do
import sys

import logging
from os.path import expanduser


filename = expanduser("~/flasher.log")
print "Logging to %s" % filename
logging.basicConfig(filename=filename, level=logging.DEBUG)



class Wrapper():
	def __init__(self,logger):
		self.logger = logger
	def write(self,data):
		self.logger.info(data)
#
# log stdout and stderr
#
sys.stdout = Wrapper(logging.getLogger('STDOUT'))
sys.stderr = Wrapper(logging.getLogger('STDERR'))

usb = LoopingCall(usb_handler.usb_loop)
usb.start(0.5)
n = LoopingCall(ssh_do.check_net)
n.start(10)
reactor.run()
