import socket
import fcntl
import struct
import os
import logging

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


ip_published = False

def check_net():
	global ip_published
	for interface in ('eth1','eth0'):
		if not ip_published:
			logging.debug("IP addres not published yet")
			if is_up(interface):
				ip = get_ip_address(interface)
				ret = os.system("ssh lxc-flash-server echo %s \>\> server_list" % ip)
				if ret == 0:
				    logging.info("Ip address %s logged to server" % ip)
				    ip_published = True
				else:
				    logging.info("Error logging ip address")
