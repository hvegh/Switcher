# Licence: GPL V3 or higher
#
import time
from pyftdi.ftdi import Ftdi
Ftdi.show_devices()

from pyftdi.spi import SpiController
spi = SpiController()
spi.configure('ftdi://::/1')
slave = spi.get_port(cs=0, freq=250E3, mode=0)

spi_page = -1
def wait_spi(page, cnt = 3):
    while cnt:
        d = slave.exchange([0x60, 0xfe], 1)
        if (d[0] & 0x80) == 0:
            return 0
        print('cnt', cnt)
        cnt = cnt - 1
    slave.exchange([0x61, 0xff, page],0)
    d = slave.exchange([0x60, 0xfe], 1)
    if (d[0] & 0x80) == 0:
        return 0
    return -1

def swrite(page, addr, data, cnt):
    global spi_page
 
    print("%02x:%02x w %x(%d)" % (page, addr, data, cnt))
    if wait_spi(page):
        print("Write software timeout")
        return -1
    if page != spi_page:
        slave.exchange([0x61, 0xff, page],0)
        spi_page = page

    d = [0x61, addr ]
    for i in range(cnt):
        d.append(data & 0xff)
        data >>= 8
    d = slave.exchange(d)
    return d

def sread(page, address, cnt):
    global spi_page

    if wait_spi(page):
        print("Read software timeout")
        return -1
    if page != spi_page:
        slave.exchange([0x61, 0xff, page],0)
        spi_page = page
    d = slave.exchange([0x10, address], cnt+1)
 
    if d[0] & 1:
        ret = 0
        for i in range(cnt, 0, -1):
            ret = ret*256 + d[i]
        return ret
    else:
        print("no rack")
    return d

def sr_print(page, addr, length):
    print("%02x:%02x r %x" % (page, addr, sread(page, addr, length)))
    

################################################################################
# Main
################################################################################

# Device ID
print('Device',   hex(sread(0x02, 0x30, 4)),
      'Revision', hex(sread(0x02, 0x40, 1)))

# Software Reset
page = 0x0
addr = 0x79
sr_print(page, addr, 1)
#swrite(page, addr, 0x88, 1)
#sr_print(page, addr, 1)

for addr in range(8):
    sr_print(page, addr, 1)

page = 0x01
addr = 0x04
sr_print(page, addr, 4)

page = 0x00
addr = 0x0b 
sr_print(page, addr, 1)
swrite(page, addr, 7, 1)
sr_print(page, addr, 1)

page = 0x4
addr = 0
sr_print(page, addr, 1)
addr = 4
sr_print(page, addr, 6)

for addr in range(0x0,0x10, 2):
    page = 0x10
    sr_print(page, addr, 2)

# Jumbo frames:
page = 0x40
addr = 0x01
sr_print(page, addr, 4)
swrite(page, addr, 0xff, 4)
sr_print(page, addr, 4)

addr = 0x05
sr_print(page, addr, 2)
swrite(page, addr, 9720, 2)
sr_print(page, addr, 2)
