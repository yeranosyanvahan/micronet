import struct
def randbytes(n):
    from random import randbytes
    return randbytes(n)

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

class microbuffer(microinterface):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.buffer = []
                  
    def resv(self,nunits = 1):
        for b in self.buffer:
            yield b
        
    def send(self,payload):
        self.buffer.append(payload)
    
