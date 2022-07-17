from .base import microinterface, randbytes

import struct

class IP(microinterface):
    class Header:
        MINSIZE = 20
        version: 0x4b = 0x04
        ihl: 0x4b = MINSIZE // 4
        tos: 0x8b = 0
        length: 0x16b
        id: 0x16b
        flags: 0x3b = 0b010 
        offset: 0x13b = 0
        ttl: 0x8b = 128
        protocol: 0x8b = 6 # tcp
        header_checksum: 0x16b = 0
        srcIP: 0x32b
        dstIP: 0x32b
        options: None
        padding: None
        def setprotocol(self,protocol):
            protocolmapper = {
                'TCP':  6,
                'UDP': 17,
                'ICMP': 1
            }
        def pack(self):
         return struct.pack('!BBHHHBBHII',
          (self.version  & 0b00001111) +\
          (self.ihl << 4),
           self.tos,
           self.length,
           self.id,
           self.flags & 0b111 +\
           self.offset << 3,
           self.ttl,
           self.protocol,
           self.header_checksum,
           self.srcIP,
           self.dstIP)
    
        def unpack(packetheader):
           header = IP.Header()
           (first,
           header.tos,
           header.length,
           header.id,
           flags,
           header.ttl,
           header.protocol,
           header.header_checksum,
           header.srcIP,
           header.dstIP)  = struct.unpack('!BBHHHBBHII',packetheader)
            
           header.version = first & 0b00001111
           header.ihl     = first >> 4 
           header.flags   = flags & 0b111
           header.offset = flags >> 3
           return header

    def __init__(self, interface):
        super().__init__(interface.src,interface.dst)
        self.interface=interface
        self.header = IP.Header()
        self.header.srcIP = self.src.IP
        self.header.dstIP = self.dst.IP
        (self.header.id,) = struct.unpack('!H',randbytes(2))

    def encapsulate(self, payload):
        self.header.length = len(payload) + self.header.ihl * 4
        return self.header.pack() + payload
    
    def decapsulate(self, packet):
        header = IP.Header.unpack(packet[:IP.Header.MINSIZE])
        return packet[header.ihl * 4:]
    
    def resv(self):
        for packet in self.interface.resv():
            yield self.decapsulate(packet)
    
    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
        
        
        
