class microsocket:
    def __init__(self, mac, IP, port, domain):
        self.domain = domain
        self.IP = struct.pack('!hhhh',*map(int, ('1.1.1.1'.split('.'))))
        self.port = port
        self.mac = mac    
