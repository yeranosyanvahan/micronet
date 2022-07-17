import struct
from random import getrandbits
def randbytes(n):
    return bytearray([getrandbits(8) for _ in range(n)])

class microsocket:
    def __init__(self, mac, IP, port, domain, crt = None):
        self.crt = crt
        self.domain = domain
        (self.IP,) = struct.unpack('!I', struct.pack('!BBBB', 
        *map(int, (IP.split('.')))))
        self.port = port
        self.mac = mac    


class microinterface:
    def __init__(self,src: microsocket, dst: microsocket, device):
        self.src = src
        self.dst = dst
        self.device = device
    def resv(self):
        for unit in self.device.resv():
            yield unit
    def send(self, payload):
        self.device.send(payload)
    def protocol_wrapper(func):
        def new_func(self, interface):
            self.interface = interface
            self.__class__.src = property(lambda self: self.interface.src)
            self.__class__.dst = property(lambda self: self.interface.dst)
            return func(self,interface)
        return new_func

        
class microbuffer(microinterface):
    def __init__(self):
        self.buffer = []
                  
    def resv(self,nunits = 1):
        for _ in range(len(self.buffer)):
            yield self.buffer.pop()

        
    def send(self,payload):
        self.buffer.append(payload)
    
