from machine import Pin, SPI
from Protocols import microsocket, microinterface
from drivers import ENC28J60
#
eth = ENC28J60(spi = SPI(0, baudrate=10000000,
              sck=Pin(18),
              mosi=Pin(19),
              miso=Pin(16)),
              cs = Pin(17))

src = microsocket(
    eth.nic.getMacAddr(),
    '0.0.0.0',
    0,
    'localhost'
    )
dst = microsocket(
    bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]),
    '0.0.0.0',
    0,
    'Bcast'
    )
microinterface(src,dst, device = eth)

