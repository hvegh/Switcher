# Why

Step by step guide to control this switch via USB.

# How


![GS108 V3 modification](/vendor/Netgear/GS108-v3/Netgear%20GS108%20modified.jpg)


 1. Remove the resistor on CPU_EEPROM_SEL(pin 18 of SOC) in order to put the device in SPI mode.
 2. Remove the serial configuration EEPROM.
 3. The CS, CLK, DI, DO and GND lines of the configuration EEPROM can now be used to hookup a SPI device.
   FT232H or ch341a, for the latter there is an external kernel module that hooks up 
 4. Optional: remove the resistor on HW_FWDG_EN (pin 9 of SOC) and pull to GND in order to disable forarding in managed mode.

# Notes:
 - Datasheet with documentation on the registers can nowadays be found on the web for quite some Broadcom switch chipsets.
   Last time I checked: BCM53118 datasheet is at https://www.mouser.com/datasheet/2/678/broadcom_limited_avgo-s-a0007199329-1-1747631.pdf
 - Most Broadcom switches are supported in Linux by the in-kernel DSA b53 driver.
   So if we can hook up the shitch via the kernel SPI bus we should be able to use the regular userspace tools like iproute and bridge to do the configuration.
   This makes this sort of hack more mainstream and usable, no legacy configuration tools are needed, all nicely within the linux networking stack.
   At the moment there is no in kernel SPI- support for the widely available USB interface modules, like FT?232H or ch341a chipsets.
   See also https://christian.amsuess.com/idea-incubator/ftdi-kernel-support/ on a deeper discussion.
 - There is an external SPI kernel module for the ch341a here: https://github.com/gschorcht/spi-ch341-usb
   I have ordered a module, in order to see if it works with the DSA driver.
