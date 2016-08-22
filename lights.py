#!/usr/bin/python
__author__ = 'Royce'

import logging
import sys
from libs.LifxControl import LifxControl

power = ""
if len(sys.argv) != 2:
    print("  python {} <on/off>\n".format(sys.argv[0]))
else:
    power = sys.argv[1]

logging.captureWarnings(True)
Control = LifxControl()
if power == "off":
    try:
        Control.allOff()
    except Exception as e:
        print e
elif power == "on":
    try:
        Control.allOn()
    except Exception as e:
        print e