from .base import microinterface, randbytes

import struct

class IP(microinterface):    
    class Header:
        class Protocol:
                TCP = 6
                UDP = 17
                ICMP = 1
        MINSIZE = 20
        version: 0x4b = 0x04
        ihl: 0x4b = MINSIZE // 4
        tos: 0x8b = 0
        length: 0x16b
        id: 0x16b
        flags: 0x3b = 0b010 
        offset: 0x13b = 0
        ttl: 0x8b = 128
        protocol: 0x8b = Protocol.TCP
        header_checksum: 0x16b = 0
        srcIP: 0x32b
        dstIP: 0x32b
        options: None
        padding: None

        def pack(self):
         return struct.pack('!BBHHHBBH',
          (self.version << 4) +\
          (self.ihl & 0b00001111),
           self.tos,
           self.length,
           self.id,
           self.flags & 0b111 +\
           self.offset << 3,
           self.ttl,
           self.protocol,
           self.header_checksum) + \
           self.srcIP +\
           self.dstIP
        
        def checksum(header):
            header.header_checksum = 0
            data = header.pack()
            checksum = 0
            data_len = len(data)
            if (data_len % 2):
                data_len += 1
                data += struct.pack('!B', 0)
            
            for i in range(0, data_len, 2):
                w = (data[i] << 8) + (data[i + 1])
                checksum += w

            checksum = (checksum >> 16) + (checksum & 0xFFFF)
            checksum = ~checksum & 0xFFFF
            return checksum

    
        def unpack(packetheader):
           header = IP.Header()
           (first,
           header.tos,
           header.length,
           header.id,
           flags,
           header.ttl,
           header.protocol,
           header.header_checksum) = struct.unpack('!BBHHHBBH',packetheader[:-8])
           header.srcIP = packetheader[-8:-8+4]
           header.dstIP = packetheader[-4:-4+4]
            
           header.version = first & 0b00001111
           header.ihl     = first >> 4 
           header.flags   = flags & 0b111
           header.offset = flags >> 3
           return header
    
    @microinterface.protocol_wrapper
    def __init__(self, interface):
        self.header = IP.Header()
        self.header.srcIP = self.src.IP
        self.header.dstIP = self.dst.IP
        (self.header.id,) = struct.unpack('!H',randbytes(2))
        if(interface.ptl == 'UDP'): self.header.protocol = IP.Header.Protocol.UDP

    def encapsulate(self, payload):
        self.header.length = len(payload) + self.header.ihl * 4
        self.header.header_checksum = IP.Header.checksum(self.header)
        Result = self.header.pack() + payload
        self.header.header_checksum = 0
        return Result
    
    def decapsulate(self, packet):
        header = IP.Header.unpack(packet[:IP.Header.MINSIZE])
        return (header, packet[IP.Header.MINSIZE:])
    
    def resv(self):
        for (_, packet) in self.interface.resv():
            yield self.decapsulate(packet)
    
    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
        
        
        
