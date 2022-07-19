import struct
from random import getrandbits
import time
def randbytes(n):
    return bytearray([getrandbits(8) for _ in range(n)])

class Timeout:
    def __init__(self, timeout = 1):
        self.timeout = timeout
        self.status = False
        
    def wait(self,generator):
        timeouttime = time.time() + self.timeout
        while(time.time() < timeouttime):
            for data in generator:
                self.status = self.func(data)
                if(self.status): return self.status
        return False
                
    def __call__(self, func):
        self.func = func
        return self
        
class microsocket:
    def __init__(self, mac, IP, port, hostname, crt = None):
        self.crt = crt
        self.hostname = hostname
        self.IP = IP
        self.port = port
        self.mac = mac    


class microinterface:
    def __init__(self,src: microsocket, dst: microsocket, device, ptl = None):
        self.src = src
        self.dst = dst
        self.device = device
        self.ptl = ptl

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
            self.__class__.ptl = property(lambda self: self.interface.ptl)
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
    
