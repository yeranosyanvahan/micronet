from .base import microinterface, microsocket, randbytes
import struct

class HTTP:
    pass
class DHCP:
    class Message:
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
        sname:    0x64b*8= b""
        file:     0x128b*8= b""
        options:  None   = bytearray([0x63,0x82,0x53,0x63])

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
               self.chaddr.rjust(16, b'\x00')  +\
               self.sname.rjust(64, b'\x00')   +\
               self.file.rjust(128, b'\x00')    +\
               self.options 
        
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
            message.options = data[236:]

            return message
        


    @microinterface.protocol_wrapper
    def __init__(self, interface):
        message = DHCP.Message()
        message.chaddr = interface.src.mac
        (message.xid,) = struct.unpack('I',randbytes(4))
        self.message = message
        
    def discover(self):
        return self.message.pack()
    def offer(self):
        pass
    def request(self):
        pass
    def acknowledge(self):        
        pass
    def run(self):
        self.discover()
        self.offer()
        self.request()
        self.acknowledge()

