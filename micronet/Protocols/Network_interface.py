from .base import microinterface, randbytes

class ARP(microinterface):
    class Message:
        # Hardware address format
        ETH = 1  # ethernet hardware
        IEEE802 = 6  # IEEE 802 hardware

        # Protocol address format
        IP = 0x0800  # IP protocol

        # ARP operation
        REQUEST     = 1# request to resolve ha given pa
        REPLY       = 2# response giving hardware address
        REVREQUEST  = 3# request to resolve pa given ha
        REVREPLY    = 4# response giving protocol address
        
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
        
    def __init__(self,interface):
        super().__init__(interface.src,interface.dst)
        self.interface=interface
        self.message = ARP.Message()
        self.message.S_L32 = self.src.IP
        self.message.S_HA  = self.src.mac
        self.message.T_L32 = self.dst.IP
        self.message.T_HA  = self.dst.mac
        

class ETH:
    # Ethertype
    IP  = 0x0800  
    ARP = 0x0806  

    dstmac:    0x6b*8
    srcmac:    0x6b*8
    ethertype: 0x2b*8 = IP
    payload:   bin
    fcs:       0x4b*8 
            
    def __init__(self, interface : microinterface ):
        self.interface = interface
        self.dstmac = interface.dst.mac
        self.srcmac = interface.src.mac

    def crc(self, payload):
        return b'\x00\x00\x00\x00'
    
    def encapsulate(self, payload):
        self.fcs = self.crc(payload)
        
        return self.dstmac +\
               self.srcmac +\
               payload     +\
               self.fcs

    def decapsulate(self, frame):
        return frame[14:-4]

    def resv(self):
        for segment in self.interface.resv():
         yield self.decapsulate(segment)

    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
            