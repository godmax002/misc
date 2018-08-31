from hashlib import sha256
from struct import pack as p
from struct import unpack as up

class MsgHead(object):
    # uint32_t
    magic   =   None
    # char[12]
    command =   None
    # uint32_t
    length  =   None
    # uint32_t
    checksum =  None
    # uchar[]
    payload = None

    def get_payload(self):
        # return payload bytes
        pass

    def get_length_checksum(self):
        # return payload length and checksum
        assert self.payload
        payload = self.payload
        length = len(paylaod)
        checksum = sha256(sha256(payload))[:4]
        return length, checksum

    def ser(self):
        self.get_payload()
        self.length, self.checksum = self.get_length_checksum()
        assert self.magic
        assert self.command
        return p('Q12sQQ', self.magic, self.command, self.length,
                self.checksum) + self.payload

    def deser(self, msg_stream, msg_cls):
        msg_head = msg_stream.read(24)
        m = msg_cls()
        m.magic, m.command, m.length, m.checksum = \
                up('Q12sQQ', msg_head)
        m.payload = msg_stream.read(length)
        return m

    ########## basic utils
    # uint8_t, 16(fd, 2), 32(fe, 4), 64(ff, 8)  
    uint16_max = pow(2, 16)
    uint32_max = pow(2, 32)
    uint64_max = pow(2, 64)

    def var_int_ser(self, mint):
        assert mint > 0 
        assert mint < uint64_max
         
        if mint < 0xff - 2:
            return p('B', mint)
        elif mint < uint16_max:
            return b'\xfd' + p('H', mint)
        elif mint < uint32_max:
            return b'\xfe' + p('I', mint)
        elif mint < uint64_max:
            return b'\xff' + p('L', mint)

    def var_int_deser(self, msg_stream):
        c = msg_stream.read(1)
        if c == b'\xfd':
            c = msg_stream.read(2)
            return up('H', c)
        elif c == b'\xfe':
            c = msg_stream.read(4)
            return up('I', c)
        elif c == b'\xff':
            c = msg_stream.read(8)
            return up('L', c)
        else:
            return up('B', 1)

    def address(self, time, services, services, ip, port):
        """
        time: uint32_t (version > 31402)
        services: uint64_t
            # 1: node_network, full blocks 
            # 2: node_getutxo
            # 4: node_bloom
            # 8: node_witness
            # 1024: node_network_limited
        ip: char[16], ipv4 or ipv6
        port: uint16_t
        """
    


    def var_str_ser(self, str_bytes):
        pass

    def var_str_dser(self, msg_stream):
        pass
            

class Version(MsgHead):
    # int32_t
    version = None
    # uint64_t
    services
    # int64_t
    timestamp
    # net_addr
    addr_recv

    # version >= 106
    # net_addr
    addr_from
    # uint64_t
    nonce
    # var_str
    user_agent
    # int32_t
    start_height

    # version >= 70001
    # bool
    relay = None

class Ping(MsgHead):
    # uint64_t
    nonce = None

    def ser_payload(self):
        return p('Q', nonce)
    
    def deser(self):
        raise NotImplementedError()

class Pong(MsgHead):
    nonce = None

    def ser(self):
        raise NotImplementedError()

    def deser_payload(self, payload):
        return up('Q', payload)

    def deser(self):
        msg = super(Ping, self).deser(msg_stream, self.__class__)
        msg.nonce = self.deser_payload(msg.payload)
        return msg

class NodeConn(asynccore.dispatcher):
    def __init__(self, dstaddr, dstport):
        asynccore.dispatcher.__init__(self)
        self.dstaddr = dstaddr
        self.dstport = dstport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sendbuf = ''
        self.recvbuf = ''
        self.ver_send = 0
        self.ver_recv = 0
        self.last_sent = 0
        self.state = 'connecting'
        print(self.state)
        
        try:
            self.connect((self.dstaddr, self.dstport))
        except:
            self.handle_close()

    def handle_connect(self):

    def handle_close(self):

    def handle_read(self):

    def handle_write(self):


if __name__ == '__main__':
    c = NodeConn('127.0.0.1', 8333)
    asyncore.loop()


        



