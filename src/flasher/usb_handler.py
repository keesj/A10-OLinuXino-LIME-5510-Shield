#!/usr/bin/env python
import usb
import time
import datetime
import subprocess
import logging

import flash_handler


from twisted.internet import reactor

def msg(str):
	logging.info("%s:%s" %(datetime.date.today() ,str))

f = None
def setF(ff):
	global f
	f  = ff

def doWrite(message):
	f.write(message)

mf = None

def start_flash(dev):                  
	global mf
	msg("Flashing device")
	doWrite("Flashing %s" % dev.serial)
	mf = flash_handler.MyFlasher("./flash.sh -s %s" % dev.serial)
	reactor.spawnProcess(mf,"./flash.sh",["flash","%s" % dev.serial],{})
#	ret = call(["fastboot","update", "-w" , "/root/FP2-gms36-1.1.7-img.zip"])

def add_device(dev):
		if dev.idVendor == 0x18d1:
			msg("Flashing")
			start_flash(dev)
		if dev.idVendor == 0x2ae5:
			msg("Non fastboot device")

def remove_device(dev):
			msg("Device removed")

class MyDevice():
	def __init__(self,bus,dev):
		self.bus = bus.dirname
		self.devnum = dev.devnum
		self.idVendor = dev.idVendor
		self.idProduct = dev.idProduct
		self.serial = "abcd"
		
		try:
			f = dev.open()
			self.serial = f.getString(dev.iSerialNumber,64)
			del f
		except usb.USBError:
			logging.warning("Failed to get serial number")
			

	def __eq__(self, other): 
		return self.__hash__() == other.__hash__()

	def __ne__(self, other): 
		return not self.__eq__(other)

	def __hash__(self):
		return hash((self.bus, self.devnum , self.idVendor, self.idProduct))
		

def list_devices():
	devset = set()	
	busses = usb.busses()
	for bus in busses:
	    devices = bus.devices
	    for dev in devices:
		#print ("Bus %s Device %s" % (bus.dirname,dev.devnum))
		if dev.idVendor == 0x18d1 and dev.idProduct == 0xd00d:
			devset.add( MyDevice(bus,dev))
		if dev.idVendor == 0x05c6 and dev.idProduct == 0x9026:
			devset.add( MyDevice(bus,dev))
		# Bus 002 Device 010: ID 2ae5:9039  
		if dev.idVendor == 0x2ae5:
			devset.add( MyDevice(bus,dev))
	return devset

# main loop
#msg("Looking...")

devlist = set()

def usb_loop():
	global devlist
	l =  list_devices()
	added = l - devlist
	removed = devlist -l
	if len(added) > 0:
		for a in added:
			add_device(a)
			logging.info ("Device added (serial = %s)" % a.serial)

	if len(removed) > 0:
		logging.info( "Device%s removed" %( ("s","")[len(added) > 1]))
		for r in removed:
			remove_device(r)
	
	devlist = l

#loopd()
