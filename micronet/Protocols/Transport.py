from .base import microinterface, randbytes
import struct
class UDP(microinterface):
    TIMEOUT = 60 
    class PseudoHeader:
        srcIP: 0x32b
        dstIP: 0x32b
        reserved: 0x8b
        protocol: 0x8b
        segmentlength: 0x16b
        
        def pack(self):
            struct.pack('!IIHH',
                        self.srcIP,    
                        self.dstIP,    
                        self.protocol,                
                        self.tcplength)
            
        def unpack(segmentheader):
            header = TCP.Header()
            (self.srcIP,    
             self.dstIP,    
             self.protocol,                
             self.segmentlength) = struct.unpack('!IIHH', segmentheader)
            return header
        
    class Header:
        SIZE = 8
        
        srcport: 0x16b
        dstport: 0x16b
        length: 0x16b
        checksum: 0x16b = 0
        def pack(self):
          return struct.pack("!hhhh", 
            self.srcport, 
            self.dstport,
            self.length,
            self.checksum)
    
        def unpack(segmentheader):
            header = UDP.Header()
            (header.srcport, 
             header.dstport,
             header.length,
             header.checksum) = struct.unpack("!hhhh", segmentheader)
            return header
    
    @microinterface.protocol_wrapper
    def __init__(self, interface : microinterface ):
        self.header = UDP.Header()
        self.header.srcport = interface.src.port
        self.header.dstport = interface.dst.port
                

    def encapsulate(self, payload):
        self.header.length = len(payload) + UDP.Header.SIZE
        return self.header.pack() + payload

    def decapsulate(self, segment):
        header = UDP.Header.unpack(segment[:UDP.Header.SIZE])
        payload = segment[UDP.Header.SIZE:]        
        return payload
    
    def resv(self):
        for segment in self.interface.resv():
         yield self.decapsulate(segment)
    
    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
        
class TCP:
    TIMEOUT = 60 
    PseudoHeader = UDP.PseudoHeader
        
    class Header:
        srcport: 0x16b
        dstport: 0x16b
        seqnumber: 0x32b
        acknumber: 0x32b
        dataoffset: 0x4b
        reserved: 0x3b
        flag: 0x9b = 0
        window: 0x16b
        checksum: 0x16b = 0
        urgent_pointer: 0x16b
        options: None
        padding: None
        

        def setflag(self,flag):
            flagmapper = {
                'NS':  0b100000000,
                'CWR': 0b010000000,
                'ECE': 0b001000000,
                'URG': 0b000100000,
                'ACK': 0b000010000,
                'PSH': 0b000001000,
                'RST': 0b000000100,
                'SYN': 0b000000010,
                'FIN': 0b000000001
            }
            if(flag not in Header.flagmapper):
                self.flag += Header.flagmapper[flag]
    
        def unpack(segmentheader):
            header = TCP.Header()
            (
            header.src_port,  
            header.dst_port,  
            header.seqnumber,            
            header.acknumber,    
            dataoffset,        
            header.flag,    
            header.window,          
            header.checksum,             
            header.urgent_pointer  
            ) = struct.unpack('!HHIIBBHHH',segmentheader)
            header.dataoffset = dataoffset >> 4            
            return header
        
        def pack(self):
         return struct.pack(
                    '!HHIIBBHHH',
                    self.src_port,  
                    self.dst_port,  
                    self.seqnumber,            
                    self.acknumber,    
                    self.dataoffset << 4,        
                    self.flag,    
                    self.window,          
                    self.checksum,             
                    self.urgent_pointer              
                )
                
    @microinterface.protocol_wrapper
    def __init__(self, interface: microinterface):   
        self.header = TCP.Header()
        self.header.srcport = interface.src.port
        self.header.dstport = interface.dst.port
        
    def resv(self):
        for segment in self.interface.resv():
            yield self.decapsulate(packet)
    
    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
        
        
        
