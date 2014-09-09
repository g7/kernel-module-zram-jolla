kernel-module-zram-jolla
========================

This repository contains the source spec file and other bits needed to build
the zram module for the kernel found in our beloved Jolla.

Prerequisites
-------------

**NOTE**: this repository **DOES NOT** contain everything needed to compile zram.

You need:
 - A working mer Platform SDK environment
 - A working Jolla device
 - The Jolla kernel sources
 - Lots of patience

Put a snapshot of the Jolla kernel (the __very__ same version you have on device) in the SOURCES/
directory, using the notation sailfishos_kernel_jolla_msm8930-%{version}.tar.bz2.  
You can obtain a tar.bz2 archive by using (on the kernel_jolla git tree):

	git archive master | bzip2 > sailfishos_kernel_jolla_msm8930-3.4.91.20140612.1.tar.bz2

You also need the kernel configuration, which you can find in /boot/config-%{version} directly
on the phone.

Another needed bit is the Module.symvers file. Jolla doesn't provide kernel headers for its
kernel, so we need to extract it ourselves from the kernel binary.

First of all, we need to extract the kernel from the boot image. To do that,
you can use [unbootimg](http://glandium.org/blog/?p=2214).  
The boot image is located in /boot/boot.img (duh!). Copy it somewhere and run unbootimg on it.

In return, you should get a couple of files. The one you'll need is boot.img-kernel.  
If you ran unbootimg directly on-device, it's better to scp the image on a working and fast machine before
doing the next step.

Download [extract-symvers](https://github.com/glandium/extract-symvers) and put it on the same
directory of the kernel image just extracted.

The [docs](https://github.com/glandium/extract-symvers) say that it's needed to obtain the base
address directly via dmesg on the running device.  
Unfortunately, I had no luck using the found base address, and [I'm not the only one](https://github.com/glandium/extract-symvers/issues/1).

Using the 0xc0008000 as suggested in that bug report I got it working, so:

	python ./extract-symvers.py -B 0xc0008000 boot.img-kernel > Module.symvers
	
Congrats! You now have the Module.symvers file, which you need to put in SOURCES/ using the naming
scheme Module.symvers-%{version}.

I hope to maintain up-to-date those files myself though.

Building
--------

Ensure to adjust the version of the .spec file to match your kernel's version.  
After that, enter in the Platform SDK and run:

	sb2 -t mer-target-armv7hl ./build.sh
	
The build should take a few minutes using a relatively recent machine.  
The result RPMs are available at RPMS/armv7hl.

Enjoy!
