"""
Created on Oct 31, 2015

@author: royce
"""

import json
import requests


class LifxControl(object):
    """
    classdocs
    """
    __token = ''
    __header = {"Authorization": "Bearer %s" % __token}

    '''
    Constructor
    '''
    def __init__(self):
        self.__prefix = "https://api.lifx.com/v1/"
        pass

    '''
    Toggle all Lights
    '''
    def allToggle(self):
        try:
            response = requests.post(self.__prefix + 'lights/all/toggle', headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)['results']
        for light in json_data:
            if light['status'] != 'ok':
                raise Exception("Problem with light: {0}".format(light['label']))
        print "All lights toggled"
        return

    '''
    Start the test system
    '''
    def allOn(self):
        try:
            response = requests.get(self.__prefix + 'lights/all', headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        for light in json_data:
            if light['power'] == 'off':
                response = requests.put(self.__prefix + 'lights/all/state', data={"power": "on"}, headers=self.__header)
        return
    '''
    Start the test system
    '''
    def allOff(self):
        try:
            response = requests.get(self.__prefix + 'lights/all', headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        for light in json_data:
            if light['power'] == 'on':
                response = requests.put(self.__prefix + 'lights/all/state', data={"power": "off"}, headers=self.__header)
        return

    '''
    List all lights
    '''
    def listLights(self):
        try:
            response = requests.get(self.__prefix + 'lights/all', headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        for light in json_data:
            print "Label : {0}".format(light['label'])
            print "Id    : {0}".format(light['id'])
            print "Type  : {0}".format(light['product']['name'])
            print "Group : {0}".format(light['group']['name'])
            if light['power'] == 'on':
                print "Power : {0}".format(light['power'])
                print "Hue   : {0}".format(light['color']['hue'])
                print "Sat   : {0}".format(light['color']['saturation'])
                print "Kelvin: {0}\n".format(light['color']['kelvin'])
            else:
                print "Power : {0}\n".format(light['power'])
        return