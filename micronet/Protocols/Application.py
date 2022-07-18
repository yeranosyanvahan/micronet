from .base import microinterface, microsocket, randbytes
import struct            
import time

class HTTP:
    pass
class DHCP:
    class Message:
        class Options:
            DISCOVER = 0x01
            OFFER = 0x02
            REQUEST = 0x03
            ACK = 0x05
            
            def __init__(self):
                self.option = {}
            def __setitem__(self, key, value):
                self.option[key] = value
            def __getitem__(self,key):
                return self.option[key]
            def __contains__(self,key):
                return key in self.option
            def pack(self):
                result = []
                for option, value in self.option.items():
                    tmp = struct.pack('!BB', option, len(value))
                    result.append(tmp+value)
                return b''.join(result) + b"\xff"
            
            def unpack(data):
                option = DHCP.Message.Options()
                
                while(len(data) > 2):
                    key = data[0]
                    if(key == 255):
                        return option
                        print('done')
                    else:
                      length = data[1]
                      value = data[2:2+length]
                      data = data[2+length:]
                      option[key] = value
                return option
                
                    
                    
        
        op :      0b1*8= 1
        htype:    0b1*8= 1 # See ARP section "Assigned numbers"
        hlen:     0b1*8= 6
        hops:     0b1*8= 0
        xid:      0x4b*8
        secs:     0x2b*8 = 0
        flags:    0x2b*8 = 0
        ciaddr:   0x4b*8 = 0
        yiaddr:   0x4b*8 = 0
        siaddr:   0x4b*8 = 0
        giaddr:   0x4b*8 = 0
        chaddr:   0x16b*8
        sname:    0x64b*8 = b'\x00' * 64
        file:     0x128b*8= b'\x00' * 128
        mcookie:  0x4b*8 = bytearray([0x63,0x82,0x53,0x63])
        options:  Options 
            
        def __init__(self):
            self.options = DHCP.Message.Options()
            
        def pack(self):
            return struct.pack("!BBBBIHHIIII",
               self.op, 
               self.htype,  
               self.hlen, 
               self.hops, 
               self.xid, 
               self.secs, 
               self.flags, 
               self.ciaddr, 
               self.yiaddr, 
               self.siaddr, 
               self.giaddr) +\
               self.chaddr +\
               self.sname +\
               self.file +\
               self.mcookie +\
               self.options.pack()
        
        def unpack(data):
            message = DHCP.Message()
            (message.op, 
            message.htype,  
            message.hlen, 
            message.hops, 
            message.xid, 
            message.secs, 
            message.flags, 
            message.ciaddr, 
            message.yiaddr, 
            message.siaddr, 
            message.giaddr) = struct.unpack("!BBBBIHHIIII", data[:28])
            message.chaddr = data[28:28+16]
            message.sname = data[44:44+64]
            message.file = data[108:108+128]
            message.mcookie = data[236:236+4]
            message.options =  DHCP.Message.Options.unpack(data[240:])

            return message
        


    @microinterface.protocol_wrapper
    def __init__(self, interface):
        message = DHCP.Message()
        message.chaddr = interface.src.mac +  b'\x00' * 10
        (message.xid,) = struct.unpack('I',randbytes(4))
        self.message = message
        
    def discover(self):
        self.message.options[53] = bytearray([DHCP.Message.Options.DISCOVER])
        self.message.options[55] = bytearray([1,3,6])
#        self.message.options[61] = bytearray([0x01]) + self.src.mac
        self.message.options[12] = self.src.hostname.encode()
        return self.message
    
    def offer(self, message):
        if(self.message.xid == message.xid and message.options[53][0]==DHCP.Message.Options.OFFER):
            self.message.ciaddr = message.yiaddr
            self.message.siaddr = message.siaddr
            if(54 in message.options):
                self.message.options[54] = message.options[54]
            return True
        return False
    
    def request(self):
        self.message.options[53] = bytearray([DHCP.Message.Options.REQUEST])
        self.message.options[50] = struct.pack('!I',self.message.ciaddr)
        return self.message
        
    def acknowledge(self, message):
        if(self.message.xid == message.xid and message.options[53][0]==DHCP.Message.Options.ACK):
            self.message = message
            return True
        return False
    
    def resv(self, parser, timeout = 2):        
        timeouttime = time.time() + timeout
        while(time.time() < timeouttime):                
            for data in self.interface.resv():
                if(parser(DHCP.Message.unpack(data))):
                    return True
        return False
    
    def send(self, message):
        self.interface.send(message.pack())        
    
    def run(self, ntries = 3):
        dropped = True
        for _ in range(ntries):
            self.send(self.discover())
            if(self.resv(self.offer)):
                dropped = False
                break
        if(dropped): raise Exception("DHCP Discover did not get through")
        
            
        dropped = True
        for _ in range(ntries):
            self.send(self.request())
            if(self.resv(self.acknowledge)):
                dropped = False
                break
            
        if(dropped): raise Exception("DHCP Request did not get through") 



