#!/bin/sh

(
COUNT=15
while [  !  `cat /sys/class/net/eth0/operstate | grep up` -a $COUNT -gt 0 ]
do
        echo $COUNT
        COUNT=$(($COUNT -1))
        sleep 1
done
ifconfig
if cat /sys/class/net/eth0/operstate | grep up
then
        echo Network is up doing a sync
        date
        ntpdate ntp0.nl.net
        date
        cd /root
        rsync -av --copy-links --delete lxc-flash-server:`hostname`/ flasher/
else
        echo not syncing
fi
systemctl status network-online.target
) 2>&1 | tee -a /root/sync.log

