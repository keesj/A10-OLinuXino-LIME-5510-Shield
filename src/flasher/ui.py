import socket
import fcntl
import struct

def is_up(ifname):
	if get_ip_address(ifname) == None:
		return False
	return True

def get_ip_address(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
			)[20:24])
	except IOError:
        	return None

class UI:
	def __init__(self):
		pygame.init()
		pygame.mouse.set_visible(False)
		self.screen = pygame.display.set_mode((84, 48), 0, 16)
		font_file  = os.path.join(os.path.dirname(__file__), 'assets/atari-small.bdf')
		self.font = pygame.font.Font(font_file,8)

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))
		self.ip_count = 0
		self.ip_status = "Unknown"
		self.status = "initial"

	def write(self, message):
		self.status = message

	def mainUiLoop(self):
		self.screen.blit(self.background, (0, 0))

		#
		# Premature optimization is the root of all evil
		#
		if self.ip_count % 10 == 0:
			if (is_up('eth0')):
				self.ip_status = "ip: %s" % get_ip_address('eth0')
			else:
				self.ip_status = "ip: Not connected"

		self.ip_count = self.ip_count +1
		
		txt = self.font.render(self.ip_status, True, (255,255,255))
		self.screen.blit(txt,(0,0))

		msg = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
		txt = self.font.render(msg, True, (255,255,255))
		self.screen.blit(txt,(0,9))
		status_msg = self.font.render(self.status, True, (255,255,255))
		self.screen.blit(status_msg,(0,18))
		status_msg = self.font.render(self.status, True, (255,255,255))
		pygame.display.flip()


import os
import pygame
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import datetime

from subprocess import call
from pygame.locals import *

	
if os.getuid() == 0:
	print ("Haha n33b you are running as root")
	os.system("echo 1 > /sys/class/backlight/fb_pcd8544/bl_power")

