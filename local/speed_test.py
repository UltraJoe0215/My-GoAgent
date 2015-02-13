#!/usr/bin/env python

import os,sys,struct,socket,time,multiprocessing

ip=[]
time_swap=[]

def port_detect(host):
    cmd='ping -c5 '+host
    out=os.popen(cmd).read()
    out=[x for x in out.split('\n') if x]
    try:
        print host, out[-1], out[-2]
    except:
        pass

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print "Usage:", os.path.basename(sys.argv[0]), "host1|host2"
        sys.exit()
    else:
        ip.extend(sys.argv[1].split('|'))
        ip=[x for x in ip if x]

        for i in ip:
            dmn_dtct = multiprocessing.Process(name='port_detect',
                                               target=port_detect,
                                               args=(str(i),))
            dmn_dtct.daemon=True
            dmn_dtct.start()

        dmn_dtct.join()
