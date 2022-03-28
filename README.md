# Switcher
The goal is to use a slightly modified cheap external switch for fun and profit.

Since discovering the datasheet for the chipset within the my old Netgear 8 ports GB switch I am wondering if it would be possible to use the in for SPI and DSA (Distributed Switch Architecture) modules to control an external, originally unmanaged, switch.

## Why would you want this?
 * Use off-the-shelf low cost switches for serious traffic management on general purpouse hardware.
 * Create truly legacy free switching solutions:
    - Completely integrated within the Linux networking stack. 
    - Leverage existing kernel code for switch management and control.
    - Use the standard Linux networking tools for configuration.

This work uses a 15 Euro Netgear GS108v3 switch in combination with a 4 Euro ch341a USB to SPI adapter:

see link below for details.

## Models
 - [Netgear GS108-v3 bcm53118 based](/vendor/Netgear/GS108-v3/README.md)

## External References
 - [Hackaday RTL8366SB based](https://hackaday.com/2010/05/26/unlocking-the-crippled-potential-of-an-unmanaged-switch/)
 - [Hackaday IP178CH based](https://hackaday.com/2015/09/07/managing-an-unmanaged-switch/)
 - [Florian bcm53128 based](https://blog.n621.de/2019/04/vlans-on-the-netgear-gs108-switch/)
 - [Linux e hacking IP178CH based](http://linuxehacking.blogspot.com/2015/08/convert-your-unmanaged-to-vlan-capable.html) and [Hackaday](https://hackaday.io/project/7536-2-unmanaged-to-managed-l2-ethernet-switch-hack)
