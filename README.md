So you bought one of these remotes on ebay?

![The offending remote](https://tiker.net/news.tiker.net/files/remote.jpeg)

And you plugged it into your Linux box, and it doesn't work? This package can
probably help.

First off, here's a description of the device: It's a remote that comes with a
USB receiver which will report itself to be a HID device with a
VendorId:ProductId of 3351:3715. It can function as a USB keyboard and a USB
mouse--the `toggle` button on the remote switches between the two uses. In
"mouse" mode, the left mouse button supposedly is "back" and the right button
is "ok". The directional controls move the mouse. The device's
[HID](http://www.usb.org/developers/hidpage/) data is scattered over two
interfaces (in the USB sense), each of which carries a HID descriptor and has
one endpoint. Here's one important piece of information: The device will not
talk unless *both* endpoints have been opened. So much for the hardware
description. Now how do you get this thing to work?

Out of the Box
==========

When you plug it into a Linux system (as of 2.6.19.1), it does not work out of
the box. It gets recognized as a mouse and a keyboard. For some reason, Linux
opens only one endpoint, leaving the other as a user HID device
(`/dev/usb/hiddevN`), and as mentioned above, the receiver will thus refuse to
talk.

What to do
========

First, tell the kernel to ignore the device. We'll talk to it via libusb. Go
into `drivers/hid/usbhid/hid-quirks.c` (or `drivers/usb/input/hid-core.c` in
older versions of Linux) and add a line

    { 0x3351, 0x3715, HID_QUIRK_IGNORE },

to the `hid_blacklist`. Recompile the module (or the whole kernel).

Next, get a thread-safe version of the
[libhid](http://libhid.alioth.debian.org/) Python binding. I hacked thread
safety into it, so it might take a while for the change to migrate upstream. I
might update this page as this happens. For the time being, you may download a
suitable set of [Debian
packages](/dl/software/xpc-remote/libhid-python-threads).

Finally, download and install my [custom LIRC
server](https://github.com/inducer/lircd-xpc). For now, the download directory
also contains a file `hidwrap.py` that should be part of libhid-python, but
while it still isn't, install it to `/usr/lib/pyton2.N/site-packages/hid` (with
appropriate permissions). Then run

    su -c python setup.py install

in the package's root. Next, run

    su -c lircd-xpc -n

If you run `irw` or any lircd client, you should see button presses coming in.
Once this works, you may install the init script from the `initscript`
directory and set up a symlink to start `lircd-xpc` automatically.

*NOTE:* You do not need the actual [LIRC daemon](http://www.lirc.org/). You
actually should not have it running. This is a replacement specifically for
this remote. Why? Well, I found it easier to rewrite the relevant parts of
`lircd` in python than to figure out how to interface to its C code. Maybe
someone with more time than me will actually tie this into the LIRC framework.

