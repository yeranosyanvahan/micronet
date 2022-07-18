from .Protocols import microsocket, microinterface
from .Protocols import TCP, UDP, ETH, ARP, DHCP, IP


        
class mnet:
   def __init__(self, hostname, device):
       self.hostname = hostname
       self.eth = device
       
   def dhcp(self):
        eth = self.eth
        src = microsocket(    
            eth.getMacAddr(),
            bytearray([0,0,0,0]),
            68,
            self.hostname
            )
        dst = microsocket(
            bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]),
            bytearray([255,255,255,255]),
            67,
            'Bcast'
            )
        dhcp = DHCP(UDP(IP(ETH(microinterface(src,dst, device = eth)))))
        return dhcp
        

class inet:
    def __init__(self, hostname, eth):
        self.hostname = hostname
        self.eth = eth
    def dhcp(self):
        src = microsocket(    
            eth.getMacAddr(),
            bytearray([0,0,0,0]),
            68,
            self.hostname
            )
        dst = microsocket(
            bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]),
            bytearray([255,255,255,255]),
            67,
            'Bcast'
            )
        
        interface = microinterface(src,dst, device = self.eth)
        dhcp = DHCP(UDP(IP(ETH)))
        dhcp.run()
#        self.network = 

        
class network:
    def __init__(self, netmask, gateway, dns):
        self.netmask = netmask
        self.gateway = gateway
        self.dns = dns
        self.arptable = {}
        self.dnscache = {}
        

        