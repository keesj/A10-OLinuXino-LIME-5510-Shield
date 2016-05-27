#
# Flasher
#
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


import usb_handler
import flash_handler
import ssh_do
import sys
import os
import ui

import logging
from os.path import expanduser


filename = expanduser("~/flasher.log")
print "Logging to %s" % filename
logging.basicConfig(filename=filename, level=logging.DEBUG)



#os.system("echo 202 > /sys/class/gpio/export")
#os.system("echo out > /sys/class/gpio/gpio202/direction")
#os.system("echo 1 > /sys/class/gpio/gpio202/value")

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


i = ui.UI()
tick = LoopingCall(i.mainUiLoop)
tick.start(1.0 / 5)


usb_handler.setF(i)
flash_handler.setF(i)

usb = LoopingCall(usb_handler.usb_loop)
usb.start(0.5)
n = LoopingCall(ssh_do.check_net)
n.start(10)
i.write("Flasher ready")
reactor.run()

