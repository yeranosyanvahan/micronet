from .base import microinterface, randbytes
import struct

class ARP(microinterface):
    class Message:
        # Hardware address format
        ETH = 1  # ethernet hardware
        IEEE802 = 6  # IEEE 802 hardware

        # Protocol address format
        IP = 0x0800  # IP protocol
        ARP = 0x0806

        # ARP operation
        REQUEST     = 1# request to resolve ha given pa
        REPLY       = 2# response giving hardware address
        
        HT: 0x2b*8 = ETH
        PT: 0x2b*8 = IP
        HAL:0x1b*8 = 6
        PAL:0x1b*8 = 4
        OP: 0x2b*8 = REQUEST
        S_HA: 0x6b*8
        S_L32:0x4b*8
        T_HA: 0x6b*8
        T_L32:0x4b*8
        def pack(self):
         return struct.pack('!HHBBH',
            self.HT,
            self.PT,
            self.HAL,
            self.PAL,
            self.OP) +\
            self.S_HA + struct.pack('!I',
            self.S_L32) +\
            self.T_HA + struct.pack('!I',
            self.T_L32)
            
        def unpack(message):
            arp = ARP.Message()
            (arp.HT,
            arp.PT,
            arp.HAL,
            arp.PAL,
            arp.OP,
            *_,
            arp.T_L32) = struct.unpack('!HHBBHQQI',message)
            arp.S_HA = message[8:8+6]
            (arp.S_L32,) = struct.unpack('!I',message[14:14+4])
            arp.T_HA = message[18:18+6]
            return arp
        
    def resv(self):
        for data in self.interface.resv():
            yield ARP.Message.unpack(data)
    
    def send(self, message):
        self.interface.send(message.pack())        
        
    def request(self):
        self.OP = ARP.Message.REQUEST
        self.message.T_L32 = self.dst.IP
        self.message.T_HA  = self.dst.mac
        self.send(self.message)
                

    def parse(self, message):
        if(message.T_L32 == self.message.S_L32 and
           message.T_HA == b'\x00'*6):
            self.message.T_L32 = message.S_L32
            self.message.T_HA  = message.S_HA
        self.send()
            
        
        
    @microinterface.protocol_wrapper
    def __init__(self,interface):
        self.message = ARP.Message()
        self.message.S_L32 = self.src.IP
        self.message.S_HA  = self.src.mac
        

class ETH:
    class Header:
        # Ethertype
        IP  = 0x0800  
        ARP = 0x0806  

        dstmac:    0x6b*8
        srcmac:    0x6b*8
        ethertype: 0x2b*8 = IP
        
        def pack(self):
         return self.dstmac +\
                self.srcmac +\
                struct.pack('!H',self.ethertype)
    
        def unpack(frameheader):
           header = ETH.Header()
           header.dstmac = frameheader[:6]
           header.srcmac = frameheader[6:6+6]
           header.ethertype = struct.unpack('!H',frameheader[12:12+2])
           return header
        
     
    @microinterface.protocol_wrapper
    def __init__(self, interface : microinterface ):
        self.header = ETH.Header()
        self.header.dstmac = interface.dst.mac
        self.header.srcmac = interface.src.mac


    def encapsulate(self, payload):
        return self.header.pack() + payload


    def decapsulate(self, frame):        
        return ETH.Header.unpack(frame[:14]), frame[14:]

    def resv(self):
        for (_, frame) in self.interface.resv():
         yield self.decapsulate(frame)

    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
            