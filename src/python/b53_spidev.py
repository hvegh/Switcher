#!/usr/bin/python

# Licence: GPL V3 or higher
#
import time
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)

spi_page = -1

def wait_spi(page, cnt = 3):
    while cnt:
        d = spi.xfer([0x60, 0xfe, 0x0])
        if (d[2] & 0x80) == 0:
            return 0
        cnt = cnt - 1

    spi.writebytes([0x61, 0xff, page])
    d = spi.xfer([0x60, 0xfe, 0x0])
    if (d[2] & 0x80) == 0:
        return 0
    return -1


def swrite(page, address, data, cnt):
    global spi_page
 
    print("write", hex(page), hex(address), hex(data), cnt)
    if wait_spi(page):
        print("Write software timeout")
        return -1
    if page != spi_page:
        spi.writebytes([0x61, 0xff, page])
        spi_page = page

    d = [0x61, address ]
    for i in range(cnt):
        d.append(data & 0xff)
        data >>= 8
    d = spi.xfer(d)
    return d

def sread(page, address, cnt):
    global spi_page

    if wait_spi(page):
        print("Read software timeout")
        return -1
    if page != spi_page:
        spi.writebytes([0x61, 0xff, page])
        spi_page = page

    d = [0x10, address, 0xff]
    d.extend([0]*cnt)
    d = spi.xfer(d)
#    print("read d",d)
 
    if d[2] & 1:
        ret = 0
        for i in range(cnt, 0, -1):
            ret = ret*256 + d[2+i]
        return ret
    else:
        print("no rack")
    return d

################################################################################
# Main
################################################################################
# Device ID

print("2.30 =", hex(sread(0x2,0x30, 1)))
print('Device',   hex(sread(0x02, 0x30, 4)),
      'Revision', hex(sread(0x02, 0x40, 1)))

#exit(0)
# Software Reset
page = 0x0
addr = 0x79
print(hex(page), hex(addr), hex(sread(page, addr, 1)))
#swrite(page, addr, 0x08, 1)
#swrite(page, addr, 0x88, 1)
#print(hex(page), hex(addr), hex(sread(page, addr, 1)))

for i in range(8):
    d = sread(page, i, 1)
    print(hex(page), hex(i), hex(d))

page = 0x01
addr = 0x04
print(hex(page), hex(addr), hex(sread(page, addr, 4)))

page = 0x00
addr = 0x0b 
print(hex(page), hex(addr), hex(sread(page, addr, 1)))
swrite(page, addr, 7, 1)
print(hex(page), hex(addr), hex(sread(page, addr, 1)))
page = 0x4
addr = 0
print(hex(page), hex(addr), hex(sread(page, addr, 1)))
addr = 4
print(hex(page), hex(addr), hex(sread(page, addr, 6)))

#for i in range(0x0,0x10, 2):
#    page = 0x10
#    print(hex(page), hex(i), hex(sread(page, i, 2)))

# Jumbo frames:
page = 0x40
addr = 0x01
print(hex(page), hex(addr), hex(sread(page, addr, 4)))
swrite(page, addr, 0xff, 4)
print(hex(page), hex(addr), hex(sread(page, addr, 4)))
addr = 0x05
print(hex(page), hex(addr), hex(sread(page, addr, 2)))
swrite(page, addr, 9720, 2)
#swrite(page, addr, 2000, 2)
print(hex(page), hex(addr), hex(sread(page, addr, 2)))

