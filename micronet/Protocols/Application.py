from .base import microinterface, microsocket, randbytes
import struct            

class HTTP:
    pass
class DHCP:
    class Message:
        class Options:
            def __init__(self):
                self.option = {}
            def __setitem__(self, key, value):
                self.option[key] = value
            def __getitem__(self,key):
                return self.option[key]
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
                if(len(data) and data[0]==255):
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
        options:  DHCP.Message.Options 
            
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
            message.options =  DHCP.Message.Options.unpack(data[236:])

            return message
        


    @microinterface.protocol_wrapper
    def __init__(self, interface):
        message = DHCP.Message()
        message.chaddr = interface.src.mac +  b'\x00' * 10
        (message.xid,) = struct.unpack('I',randbytes(4))
        self.message = message
        
    def discover(self):
        self.message.options[53] = bytearray([1])
        self.message.options[55] = bytearray([1,3,6])
        self.message.options[61] = bytearray([0x01]) + self.src.mac
        self.message.options[12] = self.src.hostname.encode()
        return self.message.pack()
    
    def offer(self, data):
        message = DHCP.Message.unpack(data)
        if(self.message.xid == message.xid):
            return message.pack()
        return False
    
    def request(self):
        pass
    def acknowledge(self):        
        pass
    def run(self):
        self.discover()
        self.offer()
        self.request()
        self.acknowledge()

