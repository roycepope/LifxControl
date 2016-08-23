#!/usr/bin/python
__author__ = 'Royce'

import os
import logging
from time import sleep
from libs.LifxControl import LifxControl

#logging.captureWarnings(True)
Control = LifxControl()

auth_log = '/var/log/auth.log'

def tail(f, n):
    stdin, stdout = os.popen2("tail -n " + str(n) + " " + f + "|grep closed")
    stdin.close()
    lines = stdout.readlines()
    stdout.close()
    return lines

monitoring = True
ip = []

while monitoring:
    sleep(5)
    auth_tail = tail(auth_log, 1)
    print auth_tail
    if auth_tail:
        if ip:
            if ip[-1] == auth_tail[-1]:
                print "No change"
        else:
            ip.append(auth_tail[0])
            print "Pulse Lights!"
            Control.pulseAll("red")

    else:
        ip = []

