Software drivers
================


Until now I have been using a modified version of the A20 olimex sample code.
this results in a quite messy set of scripts and tools used to grab input
from the GPIO and display to the user by invoking binaries.

More work is needed to make the hardware follow the linux driver model

LCD as framebuffer driver
-------------------------

TODO:
The mainline kernel as in tree (but staging) support for the Nokia 3310 Display in
the form of fbtft see drivers/staging/fbtft or the `fbtft wiki`_.

.. _fbtft wiki: https://github.com/notro/fbtft/wiki

We need to start using this driver. 

Button as key events
--------------------

TODO:
We need to configure kernel to make the GPIO pins generate key evens (UEVENTS).

