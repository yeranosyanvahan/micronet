from .Protocols import microsocket, microinterface
from .Protocols import TCP, UDP, ETH, ARP, DHCP, IP
import struct

class inet:
    def interface(device):
        src = microsocket(    
            device.getMacAddr(),
            bytearray([0,0,0,0]),
            68,
            "RPI PICO"
            )
        dst = microsocket(
            bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]),
            bytearray([255,255,255,255]),
            67,
            'Bcast'
            )
        return microinterface(src,dst, device = device)
    def dhcp(hostname, device):
        src = microsocket(    
            device.getMacAddr(),
            bytearray([0,0,0,0]),
            68,
            hostname
            )
        dst = microsocket(
            bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]),
            bytearray([255,255,255,255]),
            67,
            'Bcast'
            )
        interface = microinterface(src,dst, device = device, ptl = "UDP")
        dhcp = DHCP(UDP(IP(ETH(interface))))
        dhcp.run()
        
        message = dhcp.message
        interface.src.IP  = message.yiaddr
        netmask = message.options[1]
        gateway = message.options[3]
        dns = message.options[6]

        (leasetime,) = struct.unpack('!I',message.options[51])

        return interface

        
class network:
    def __init__(self, netmask, gateway, dns):
        self.netmask = netmask
        self.gateway = gateway
        self.dns = dns
        self.arptable = {}
        self.dnscache = {}
    def __str__(self):
        return f"""
            netmask: {self.netmask}
            gateway: {self.gateway}
            dns:    {self.dns}
            """
        

        