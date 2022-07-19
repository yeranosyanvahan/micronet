from .base import microinterface, randbytes
import struct
class UDP(microinterface):
    TIMEOUT = 60
    def checksum(data):
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
    
    class PseudoHeader:
        srcIP: 0x32b
        dstIP: 0x32b
        reserved: 0x8b = 0
        protocol: 0x8b =  17 #UDP
        segmentlength: 0x16b
        
        def pack(self):
            return self.srcIP +\
                   self.dstIP + struct.pack('!HH', 
                   self.protocol,                
                   self.segmentlength)
            
        def unpack(segmentheader):
            header = UDP.Header()
            self.srcIP = segmentheader[:4]  
            self.dstIP = segmentheader[4:4+4]    
            (self.protocol,                
            self.segmentlength) = struct.unpack('!HH', segmentheader[8:])
            return header
        
    class Header:
        SIZE = 8        
        srcport: 0x16b
        dstport: 0x16b
        segmentlength: 0x16b
        checksum: 0x16b = 0
        def pack(self):
          return struct.pack("!HHHH", 
            self.srcport, 
            self.dstport,
            self.segmentlength,
            self.checksum)
    
        def unpack(segmentheader):
            header = UDP.Header()
            (header.srcport, 
             header.dstport,
             header.segmentlength,
             header.checksum) = struct.unpack("!HHHH", segmentheader)
            return header
    
    @microinterface.protocol_wrapper
    def __init__(self, interface : microinterface ):
        self.header = UDP.Header()
        self.pseudoheader = UDP.PseudoHeader()
        self.header.srcport = interface.src.port
        self.header.dstport = interface.dst.port
        self.pseudoheader.srcIP = interface.src.IP
        self.pseudoheader.dstIP = interface.dst.IP
                

    def encapsulate(self, payload):
        self.header.segmentlength = len(payload) + UDP.Header.SIZE
        self.pseudoheader.segmentlength = len(payload) + UDP.Header.SIZE
        self.header.checksum  = 0
        self.header.checksum = UDP.checksum(self.pseudoheader.pack() + self.header.pack() + payload)
        return self.header.pack() + payload

    def decapsulate(self, segment):
        header = UDP.Header.unpack(segment[:UDP.Header.SIZE])
        return header, segment[UDP.Header.SIZE:]  
    
    def resv(self):
        for (_, segment) in self.interface.resv():
         yield self.decapsulate(segment)
    
    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
        
class TCP:
    TIMEOUT = 2
    MSS  = 500
    checksum = UDP.checksum
    class PseudoHeader(UDP.PseudoHeader):
        protocol = 6 # tcp
        
    class Header:
        SIZE = 20
        
        srcport: 0x16b
        dstport: 0x16b
        seqnumber: 0x32b
        acknumber: 0x32b = 0
        dataoffset: 0x4b = SIZE//4
        reserved: 0x3b = 0
        flag: 0x9b = 0
        window: 0x16b = 500 #TCP.MSS
        checksum: 0x16b = 0
        urgent_pointer: 0x16b = 0
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
            header.srcport,  
            header.dstport,  
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
                    self.srcport,  
                    self.dstport,  
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
        self.pseudoheader = TCP.PseudoHeader()
        (self.header.seqnumber, ) = struct.unpack("I",randbytes(4))
        self.header.srcport = interface.src.port
        self.header.dstport = interface.dst.port
        self.pseudoheader.srcIP = interface.src.IP
        self.pseudoheader.dstIP = interface.dst.IP
    
    def encapsulate(self, payload):
        self.header.segmentlength = len(payload) + TCP.Header.SIZE
        self.pseudoheader.segmentlength = len(payload) + TCP.Header.SIZE
        self.header.checksum  = 0
        self.header.checksum = TCP.checksum(self.pseudoheader.pack() + self.header.pack() + payload)
        return self.header.pack() + payload

    def decapsulate(self, segment):
        header = UDP.Header.unpack(segment[:UDP.Header.SIZE])
        return header, segment[UDP.Header.SIZE:]
    
        
    def resv(self):
        for segment in self.interface.resv():
            yield self.decapsulate(packet)
    
    def send(self, payload):
        self.interface.send(self.encapsulate(payload))
        
        
        
