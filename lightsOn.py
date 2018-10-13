__author__ = 'Royce'

import logging
from libs.LifxControl import LifxControl

logging.captureWarnings(True)
Control = LifxControl()

__light = {"Desk": "d073d527ef8f",
           "Strip": "d073d528d383",
           "Entry": "d073d5384329",
           "Lamp": "d073d5120593"}

try:
    #Control.allOn()
    Control.listLights()
    Control.lightOn(__light["Desk"], "yellow")
    #Control.pulseAll()
    #Control.allOff()
    #Control.listScenes()
    #Control.activateScene()
    #Control.listLights()
except Exception as e:
    print e

