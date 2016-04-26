Software drivers
================


Until now I have been using a modified version of the A20 olimex sample code.
this results in a quite messy set of scripts and tools used to grab input
from the GPIO and display to the user by invoking binaries.

More work is needed to make the hardware follow the linux driver model

LCD as framebuffer driver
-------------------------

Enable BT_TFT in kernel config (first enable staging)

also enable pcd8544::

  {
                  .name = "nokia3310",
                  .spi = &(struct spi_board_info) {
                          .modalias = "fb_pcd8544",
                          .max_speed_hz = 400000,
                          .mode = SPI_MODE_0,
                          .platform_data = &(struct fbtft_platform_data) {
                                  .display = {
                                          .buswidth = 8,
                                  },
                                  .gpios = (const struct fbtft_gpio []) {
                                          { "reset", 25 },
                                          { "dc", 24 },
                                          { "led", 23 },
                                          {},
                                  },
                          }
                  }
          }

	MODULE_ALIAS("spi:" DRVNAME);
	MODULE_ALIAS("spi:pdc8544");


pretty nice wiki but pretty much targetting rpi
https://github.com/notro/fbtft/wiki

Looking at some examples we need to add a slave node attached to the
spi bus and make it "compatible with "pdc8544". next we need to configure
the data command pin and led pin.

https://github.com/notro/fbtft/blob/master/dts/rpi.dts

Hence we need to configure the reset , dc and led gpio (next to the SPI)

TODO:
The mainline kernel as in tree (but staging) support for the Nokia 3310 Display in
the form of fbtft see drivers/staging/fbtft or the `fbtft wiki`_.

.. _fbtft wiki: https://github.com/notro/fbtft/wiki

We need to start using this driver.

device tree changes::

	&spi2 {
		pinctrl-names = "default";
		pinctrl-0 = <&spi2_pins_a>,
			    <&spi2_cs0_pins_a>;
		status = "okay";
		nokia3310@1 {
			compatible = "philips,pdc8544";
			rotate = <0>;
			reg = <0>;
			spi-max-frequency = <25000000>;
			reset-gpios = <&pio 1 20>; /* PB20 */
			dc-gpios    = <&pio 1 21>; /* PB21 */
			led-gpios    = <&pio 6 10>;/* GP10 */
		};
	};

log output::

	[    0.842047] Freeing initrd memory: 12308K (cf3fb000 - d0000000)
	[    1.744089] fbtft_of_value: rotate = 0
	[    1.747959] fb_pcd8544 spi32765.0: buswidth is not set
	[    1.753129] fb_pcd8544: probe of spi32765.0 failed with error -22

Base on this input::

	&spi2 {
		pinctrl-names = "default";
		pinctrl-0 = <&spi2_pins_a>,
			    <&spi2_cs0_pins_a>;
		status = "okay";
		nokia3310@1 {
			compatible = "philips,pdc8544";

			spi-max-frequency = <25000000>;

			rotate = <0>;
			reg = <0>;
			buswidth = <8>;

			reset-gpios = <&pio 1 20 GPIO_ACTIVE_HIGH>; /* PB20 */
			dc-gpios    = <&pio 1 21 GPIO_ACTIVE_HIGH>; /* PB21 */
			led-gpios    = <&pio 6 10 GPIO_ACTIVE_HIGH>;/* GP10 */
		};
	};


second modification::

	Bubhid: USB HID core driver
	[    1.744115] fbtft_of_value: buswidth = 8
	[    1.748059] fbtft_of_value: rotate = 0
	[    1.873045] fb_pcd8544 spi32765.0: SPI transfer failed: -22
	[    1.878696] spi_master spi32765: failed to transfer one message from queue
	[    1.885565] fb_pcd8544 spi32765.0: write failed and returned: -22
	[    1.891683] fb_pcd8544 spi32765.0: fbtft_update_display: write_vmem failed to update display buffer
	[    1.903614] Console: switching to colour frame buffer device 10x6
	[    1.909892] graphics fb0: fb_pcd8544 frame buffer, 84x48, 7 KiB video memory, 0 KiB DMA buffer memory, fps=20, spi32765.0 at 25 MHz
	[    1.923068] NET: Registered protocol family 17
	[    1.927582] can: controller area network core (rev 20120528 abi 9)
	[    1.933829] NET: Registered protocol family 29
	[    1.938297] can: raw protocol (rev 20120528)
	[    1.942569] can: broadcast manager protocol (rev 20120528 t)
	[    1.948251] can: netlink gateway (rev 20130117) max_hops=1
	[    1.954019] Key type dns_resolver registered
	[    1.958927] cpufreq: cpufreq_online: CPU0: Running at unlisted freq: 1008000 KHz
	[    1.966949] cpufreq: cpufreq_online: CPU0: Unlisted initial frequency changed to: 912000 KHz
	[    1.975659] Registering SWP/SWPB emulation handler
	[    1.980941] fb_pcd8544 spi32765.0: SPI transfer failed: -22
	[    1.986563] spi_master spi32765: failed to transfer one message from queue
	[    1.993433] fb_pcd8544 spi32765.0: write failed and returned: -22
	[    1.999537] fb_pcd8544 spi32765.0: fbtft_update_display: write_vmem failed to update display buffer
	[    2.043104] mmc0: host does not support reading read-only switch, assuming write-enable
	[    2.053370] mmc0: new high speed SDHC card at address 27ac
	[    2.059424] mmcblk0: mmc0:27ac SD04G 3.75 GiB
	[    2.065047]  mmcblk0: p1 p2
	[    2.075809] ahci-sunxi 1c18000.sata: controller can't do PMP, turning off CAP_PMP
	[    2.083325] ahci-sunxi 1c18000.sata: SSS flag set, parallel bus scan disabled
	[    2.090509] ahci-sunxi 1c18000.sata: AHCI 0001.0100 32 slots 1 ports 3 Gbps 0x1 impl platform mode
	[    2.099483] ahci-sunxi 1c18000.sata: flags: ncq sntf stag pm led clo only pio slum part ccc
	[    2.109008] scsi host0: ahci-sunxi
	[    2.112760] ata1: SATA max UDMA/133 mmio [mem 0x01c18000-0x01c18fff] port 0x100 irq 26
	[    2.121086] ehci-platform 1c14000.usb: EHCI Host Controller
	[    2.126722] ehci-platform 1c14000.usb: new USB bus registered, assigned bus number 1
	[    2.134599] ehci-platform 1c14000.usb: irq 22, io mem 0x01c14000
	[    2.155888] fb_pcd8544 spi32765.0: SPI transfer failed: -22
	[    2.161465] spi_master spi32765: failed to transfer one message from queue
	[    2.168357] fb_pcd8544 spi32765.0: write failed and returned: -22
	[    2.174444] fb_pcd8544 spi32765.0: fbtft_update_display: write_vmem failed to update display buffer
	[    2.183534] ehci-platform 1c14000.usb: USB 2.0 started, EHCI 1.00
	[    2.190590] hub 1-0:1.0: USB hub found
	[    2.194381] hub 1-0:1.0: 1 port detected
	[    2.199084] ehci-platform 1c1c000.usb: EHCI Host Controller

Tyring to validate the hint I got from IRC I am hitting the 64 bytes limit::

	diff --git a/drivers/staging/fbtft/fb_pcd8544.c b/drivers/staging/fbtft/fb_pcd8544.c
	index a6b4332..e9b6c2a 100644
	--- a/drivers/staging/fbtft/fb_pcd8544.c
	+++ b/drivers/staging/fbtft/fb_pcd8544.c
	@@ -129,7 +129,8 @@ static int write_vmem(struct fbtft_par *par, size_t offset, size_t len)

		/* Write data */
		gpio_set_value(par->gpio.dc, 1);
	-       ret = par->fbtftops.write(par, par->txbuf.buf, 6 * 84);
	+       //ret = par->fbtftops.write(par, par->txbuf.buf, 6 * 84);
	+       ret = par->fbtftops.write(par, par->txbuf.buf, 60);
		if (ret < 0)
			dev_err(par->info->device, "write failed and returned: %d\n",
				ret);


IRC::

	13:34 -!- mozzwald [~www.mozzw@c-67-176-182-49.hsd1.il.comcast.net] has joined #linux-sunxi
	13:35 < keesj> does: spi_master spi32765: failed to transfer one message from queue  ring a bell?
	13:35 < keesj> I am trying to enable the fbtft (staging) driver on an A10-Lime board
	13:36 < keesj> (full paste here http://paste.ubuntu.com/15827945/ )
	13:37 < keesj> I previously tested the hardware using spidev (also on spi32765.1)
	13:45 < lennyraposo> see you all later folks
	13:45 < lennyraposo> ;)
	13:45 -!- lennyraposo [~administr@CPE84948c5c33d1-CM84948c5c33d0.cpe.net.cable.rogers.com] has quit [Quit: Leaving.]
	13:47 < keesj> can it be that I am finally hitting the 64 bytes limit?
	13:51 < keesj> I think I am
	13:52 < plaes> keesj: yes you are
	13:52 < plaes> I had same issue
	13:53 < plaes> keesj: feel free to steal the patches: https://github.com/plaes/linux/commits/plaes-wip-stuff
	13:55 < keesj> any speofic commit ? like https://github.com/plaes/linux/commit/c39fb6ae72a2f274595f3ad48ed0f02068789834 or is there more
		       stuff I need to fetch?
	13:56 < keesj> there is more good steal stuff there

code::

	git remote add plaes https://github.com/plaes/linux.git
	git fetch plaes
	git diff plaes/plaes-wip-stuff
	

steal::

	keesj@e540:~/projects/olimex/linux-new$ git cherry-pick 0b931d5a8b40725540a3ad23f581cb11cf3a7739
	[master 7eb9f6a] spi: sun4i: add DMA support
	 Author: Emilio López <emilio@elopez.com.ar>
	 Date: Fri May 30 17:27:28 2014 -0300
	 1 file changed, 128 insertions(+), 12 deletions(-)
	keesj@e540:~/projects/olimex/linux-new$ git cherry-pick c39fb6ae72a2f274595f3ad48ed0f02068789834
	[master 5a3cc75] ARM: sunxi: spi: add notice about SPI FIFO limit.
	 Author: Michal Suchanek <hramrach@gmail.com>
	 Date: Mon May 4 12:23:59 2015 +0200
	 1 file changed, 3 insertions(+), 1 deletion(-)


trying some python code to access the framebuffer::

	
	apt-get install python-pygame
	reading :

	export SDL_VIDEODRIVER=directfb
	root@flasher-06:~# python game.py
	commandline read: python
	commandline read: game.py
	   ~~~~~~~~~~~~~~~~~~~~~~~~~~| DirectFB 1.2.10 |~~~~~~~~~~~~~~~~~~~~~~~~~~
		(c) 2001-2008  The world wide DirectFB Open Source Community
		(c) 2000-2004  Convergence (integrated media) GmbH
	      ----------------------------------------------------------------

	(*) DirectFB/Core: Single Application Core. (2014-10-21 10:21)
	(*) Direct/Thread: Started 'VT Switcher' (-1) [CRITICAL OTHER/OTHER 0/0] <8388608>...
	(*) Direct/Thread: Started 'Keyboard Input' (-1) [INPUT OTHER/OTHER 0/0] <8388608>...
	(*) DirectFB/Input: Keyboard 0.9 (directfb.org)
	(*) Direct/Thread: Started 'Linux Input' (-1) [INPUT OTHER/OTHER 0/0] <8388608>...
	(*) DirectFB/Input: gpio_keys (1) 0.1 (directfb.org)
	(*) Direct/Thread: Started 'Linux Input' (-1) [INPUT OTHER/OTHER 0/0] <8388608>...
	(*) DirectFB/Input: axp20x-pek (2) 0.1 (directfb.org)
	(*) DirectFB/Graphics: Generic Software Rasterizer 0.6 (directfb.org)
	(*) DirectFB/Core/WM: Default 0.3 (directfb.org)
	(*) FBDev/Surface: Allocated 84x48 16 bit RGB16 buffer (index 0) at offset 0 and pitch 168.
	ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
	ALSA lib conf.c:4259:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
	ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
	ALSA lib conf.c:4259:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
	ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
	ALSA lib conf.c:4259:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
	ALSA lib conf.c:4738:(snd_config_expand) Evaluate error: No such file or directory
	ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM default
	SDL DirectFB_SetVideoMode: 84x48@16, flags: 0x10000000
	(*) FBDev/Mode: Setting 84x48 RGB16
	(*) FBDev/Mode: Switched to 84x48 (virtual 84x48) at 16 bit (RGB16), pitch 168
	(*) FBDev/Surface: Allocated 84x48 16 bit RGB16 buffer (index 0) at offset 0 and pitch 168.
	(*) FBDev/Surface: Allocated 84x48 16 bit RGB16 buffer (index 0) at offset 0 and pitch 168.
	(!) DirectFB/core/vt: Unable to disallocate VT!
	    --> Device or resource busy

edit::

	root@flasher-06:~# cat .directfbrc 
	no-vt-switch 


viewing key evens::

	root@flasher-06:~# python game.py
	commandline read: python
	commandline read: game.py

	   ~~~~~~~~~~~~~~~~~~~~~~~~~~| DirectFB 1.2.10 |~~~~~~~~~~~~~~~~~~~~~~~~~~
		(c) 2001-2008  The world wide DirectFB Open Source Community
		(c) 2000-2004  Convergence (integrated media) GmbH
	      ----------------------------------------------------------------

	(*) DirectFB/Core: Single Application Core. (2014-10-21 10:21)
	(*) Direct/Thread: Started 'VT Switcher' (-1) [CRITICAL OTHER/OTHER 0/0] <8388608>...
	(*) Direct/Thread: Started 'Keyboard Input' (-1) [INPUT OTHER/OTHER 0/0] <8388608>...
	(*) DirectFB/Input: Keyboard 0.9 (directfb.org)
	(*) Direct/Thread: Started 'Linux Input' (-1) [INPUT OTHER/OTHER 0/0] <8388608>...
	(*) DirectFB/Input: gpio_keys (1) 0.1 (directfb.org)
	(*) Direct/Thread: Started 'Linux Input' (-1) [INPUT OTHER/OTHER 0/0] <8388608>...
	(*) DirectFB/Input: axp20x-pek (2) 0.1 (directfb.org)
	(*) DirectFB/Graphics: Generic Software Rasterizer 0.6 (directfb.org)
	(*) DirectFB/Core/WM: Default 0.3 (directfb.org)
	(*) FBDev/Surface: Allocated 84x48 16 bit RGB16 buffer (index 0) at offset 0 and pitch 168.
	ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
	ALSA lib conf.c:4259:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
	ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
	ALSA lib conf.c:4259:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
	ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
	ALSA lib conf.c:4259:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
	ALSA lib conf.c:4738:(snd_config_expand) Evaluate error: No such file or directory
	ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM default
	SDL DirectFB_SetVideoMode: 84x48@16, flags: 0x10000000
	(*) FBDev/Mode: Setting 84x48 RGB16
	(*) FBDev/Mode: Switched to 84x48 (virtual 84x48) at 16 bit (RGB16), pitch 168
	(*) FBDev/Surface: Allocated 84x48 16 bit RGB16 buffer (index 0) at offset 0 and pitch 168.
	<Event(2-KeyDown {'scancode': 0, 'key': 0, 'unicode': u'', 'mod': 0})>
	<Event(3-KeyUp {'scancode': 0, 'key': 0, 'mod': 0})>
	<Event(2-KeyDown {'scancode': 75, 'key': 278, 'unicode': u'', 'mod': 0})>
	<Event(3-KeyUp {'scancode': 75, 'key': 278, 'mod': 0})>
	<Event(2-KeyDown {'scancode': 0, 'key': 0, 'unicode': u'', 'mod': 0})>
	<Event(3-KeyUp {'scancode': 0, 'key': 0, 'mod': 0})>



Button as key events
--------------------

TODO:
We need to configure kernel to make the GPIO pins generate key evens (UEVENTS).

Enable Even interface and GPIO button in the kernel

device tree first::

	gpio_keys {
		compatible = "gpio-keys";
		pinctrl-names = "default";
		pinctrl-0 = <&key_pins_shield>;
		#address-cells = <1>;
		#size-cells = <0>;

		button@0 {
			label = "Key Back";
			linux,code = <KEY_BACK>;
			gpios = <&pio 6 7 GPIO_ACTIVE_HIGH>;
		};

		button@1 {
			label = "Key Home";
			linux,code = <KEY_HOME>;
			gpios = <&pio 6 8 GPIO_ACTIVE_HIGH>;
		};

		button@2 {
			label = "Key Menu";
			linux,code = <KEY_MENU>;
			gpios = <&pio 6 9 GPIO_ACTIVE_HIGH>;
		};
	};

resulted in::

	root@flasher-06:~# dmesg | grep gpio
	[    2.429051] gpio-keys gpio_keys: Unable to get irq number for GPIO 199, error -22
	[    2.436643] gpio-keys: probe of gpio_keys failed with error -22
	root@flasher-06:~#


result::

	root@flasher-06:/sys/devices/platform/gpio_keys/of_node# ls -l
	total 0
	-r--r--r-- 1 root root  4 Jan  1 01:47 #address-cells
	drwxr-xr-x 2 root root  0 Jan  1 01:47 button@0
	drwxr-xr-x 2 root root  0 Jan  1 01:47 button@1
	drwxr-xr-x 2 root root  0 Jan  1 01:47 button@2
	-r--r--r-- 1 root root 15 Jan  1 01:47 compatible
	-r--r--r-- 1 root root 10 Jan  1 01:47 name
	-r--r--r-- 1 root root  4 Jan  1 01:47 pinctrl-0
	-r--r--r-- 1 root root  8 Jan  1 01:47 pinctrl-names
	-r--r--r-- 1 root root  4 Jan  1 01:47 #size-cells
	root@flasher-06:/sys/devices/platform/gpio_keys/of_node#


enable gpio-keys-polled (in menu config) replace gpio-keys with gpio-keys-polled and
added a poll-interval:

[    1.839445] input: gpio_keys as /devices/platform/gpio_keys/input/input0
[    1.847738] sunxi-rtc 1c20d00.rtc: rtc core: registered rtc-sunxi as rtc0
[

from http://stackoverflow.com/questions/11608454/frame-buffer-module-of-python


lower freq::

		spi-max-frequency = <400000>;

change gamma::

	root@flasher-06:/sys/devices/platform/soc@01c00000/1c17000.spi/spi_master/spi32765/spi32765.1/graphics/fb0# pwd
	/sys/devices/platform/soc@01c00000/1c17000.spi/spi_master/spi32765/spi32765.1/graphics/fb0
	echo 25  > /sys/devices/platform/soc@01c00000/1c17000.spi/spi_master/spi32765/spi32765.1/graphics/fb0/gamma


Backlight::
	
	https://github.com/notro/fbtft/wiki/Backlight
	echo 1 > /sys/class/backlight/*/bl_power


tested using evtest::

	root@flasher-06:~# evtest /dev/input/event0
	Input driver version is 1.0.1
	Input device ID: bus 0x19 vendor 0x1 product 0x1 version 0x100
	Input device name: "gpio_keys"
	Supported events:
	  Event type 0 (EV_SYN)
	  Event type 1 (EV_KEY)
	    Event code 102 (KEY_HOME)
	    Event code 139 (KEY_MENU)
	    Event code 158 (KEY_BACK)
	Properties:
	Testing ... (interrupt to exit)
	Event: time 1262307768.536826, type 1 (EV_KEY), code 139 (KEY_MENU), value 1
	Event: time 1262307768.536826, -------------- EV_SYN ------------
	Event: time 1262307768.836842, type 1 (EV_KEY), code 139 (KEY_MENU), value 0
	Event: time 1262307768.836842, -------------- EV_SYN ------------
	Event: time 1262307770.036866, type 1 (EV_KEY), code 102 (KEY_HOME), value 1
	Event: time 1262307770.036866, -------------- EV_SYN ------------
	Event: time 1262307770.336814, type 1 (EV_KEY), code 102 (KEY_HOME), value 0
	Event: time 1262307770.336814, -------------- EV_SYN ------------
	Event: time 1262307771.836827, type 1 (EV_KEY), code 158 (KEY_BACK), value 1
	Event: time 1262307771.836827, -------------- EV_SYN ------------
	Event: time 1262307772.036816, type 1 (EV_KEY), code 158 (KEY_BACK), value 0
	Event: time 1262307772.036816, -------------- EV_SYN ------------

Modify device tree:

Test changed using evtest
apt-get install evtest

Looking arround::

	 root@flasher-06:~# cat /proc/bus/input/devices
	 I: Bus=0000 Vendor=0000 Product=0000 Version=0000
	 N: Name="axp20x-pek"
	 P: Phys=m1kbd/input2
	 S: Sysfs=/devices/platform/soc@01c00000/1c2ac00.i2c/i2c-0/0-0034/axp20x-pek/input/input0
	 U: Uniq=
	 H: Handlers=kbd event0
	 B: PROP=0
	 B: EV=3
	 B: KEY=100000 0 0 0

	 root@flasher-06:~# evtest /dev/input/event0
	 Input driver version is 1.0.1
	 Input device ID: bus 0x0 vendor 0x0 product 0x0 version 0x0
	 Input device name: "axp20x-pek"
	 Supported events:
	  Event type 0 (EV_SYN)
	  Event type 1 (EV_KEY)
	    Event code 116 (KEY_POWER)
	 Properties:
	 Testing ... (interrupt to exit)




install pyton-edev
