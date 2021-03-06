#!/usr/bin/env python

import os,sys,struct,socket,time,multiprocessing

try:
    from netaddr import *
except:
    print 'please install python-netaddr first.'
    sys.exit()

def port_detect(hostname):

    port=443
    # detect hostname's port
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        hostname=socket.gethostbyname(hostname)
        s.connect((hostname, port))
        print hostname
    except:
        pass
    
    s.close()

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print "Usage:", os.path.basename(sys.argv[0]), "host1|host2"
        sys.exit()
    else:
        ip=sys.argv[1].split('|')

        for i in ip:

            dmn_dtct = multiprocessing.Process(name='port_detect',
                                               target=port_detect,
                                               args=(str(i),))
            dmn_dtct.daemon=True
            dmn_dtct.start()

        dmn_dtct.join()
