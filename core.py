import os
import socket
import time
import sys

def get_RTT(host,max=4):
    platform = sys.platform
    if platform == 'win32':
        command = 'ping ' + host + ' -n 1'
    elif platform == 'darwin':
        command = 'ping -c 1 ' + host
    for x in range(max):
        result = []
        for x in os.popen(command):
            result.append(x)
        try:
            if platform == 'win32':
                return int(result[-1][result[-1].rfind(' ') + 1:-3])
            elif platform == 'darwin':
                return int(result[-1].split('/')[-3].split('.')[0])
        except Exception:
            pass
    raise TimeoutError('Cannot get RTT! The remote host blocked Ping!')

def get_address(address,AF_INET6=False):
    if AF_INET6:
        return socket.getaddrinfo(address[0], address[1], socket.AF_INET6)[0][4]
    else:
        return socket.getaddrinfo(address[0], address[1], socket.AF_INET)[0][4]

def get_probe(address,AF_INET6=False):
    if AF_INET6:
        probe = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    S = time.time()
    probe.connect(address)
    E = time.time()
    probe.close()
    return E - S

def get_TLR(address,n=10,AF_INET6=False):
    total_packet = 0
    lost_packet = 0
    address = get_address(address,AF_INET6)
    RTT = get_RTT(address[0],4)
    for x in range(n):
        try:
            TCT = get_probe(address,AF_INET6) * 1000
        except Exception:
            total_packet += 1
            lost_packet += 1
        else:
            total_packet += 3
            if (TCT - RTT) > 0:
                total_packet += 0.5 * ((TCT - RTT) // 1000)
                lost_packet += (TCT - RTT) // 1000
    return round((lost_packet/total_packet)*100,2)


if __name__ == '__main__':
    address = ('dc2.bwg.net',443)
    print('DC2丢包率:',get_TLR(address,100),'%')
    address = ('dc3.bwg.net',443)
    print('DC3丢包率:',get_TLR(address,100),'%')
    address = ('dc4.bwg.net',443)
    print('DC4丢包率:',get_TLR(address,100),'%')
    address = ('dc6.bwg.net',443)
    print('DC6丢包率:',get_TLR(address,100),'%')
    address = ('dc8.bwg.net',443)
    print('DC8丢包率:',get_TLR(address,100),'%')
    address = ('dc9.bwg.net',443)
    print('DC9丢包率:',get_TLR(address,100),'%')
    address = ('fmt.bwg.net',443)
    print('FMT丢包率:',get_TLR(address,100),'%')