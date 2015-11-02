__author__ = 'Royce'

import logging
from libs.LifxControl import LifxControl

logging.captureWarnings(True)
Control = LifxControl()

try:
    Control.allOff()
except Exception as e:
    print e