from .enc28j60 import ENC28J60

class driver:
    def __init__(self, spi, cs):
        self.nic = ENC28J60(spi, cs)
        self.nic.init()
        
    def resv(self):
        nic = self.nic
        buf = bytearray(enc28j60.ENC28J60_ETH_RX_BUFFER_SIZE)
        while nic.GetRxPacketCnt():
            length = nic.ReceivePacket(buf)
            yield buf[:length]
    
    def send(self, payload):
        self.nic.SendPacket([payload])
