__author__ = 'Royce'

import logging
from libs.LifxControl import LifxControl

logging.captureWarnings(True)
Control = LifxControl()

try:
    #Control.allOn()
    Control.listLights()
    Control.pulseAll()
    #Control.allOff()
    #Control.listScenes()
    #Control.activateScene()
    #Control.listLights()
except Exception as e:
    print e