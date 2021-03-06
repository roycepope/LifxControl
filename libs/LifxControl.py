"""
Created on Oct 31, 2015

@author: royce
"""

import json
import requests
import logging
from prettytable import PrettyTable


class LifxControl(object):
    """
    classdocs
    """
    __token = ''
    __header = {"Authorization": "Bearer %s" % __token}
    __scene = {"Modern": "d1cdcd6b-7e54-4608-a419-ccfac4ee2b9f",
               "Movie": "cb1a2a0c-e2b5-4f3a-9271-aa20ee5034fa",
               "Gaming": "fc7ec00e-c930-48c6-ba87-afb70395508a",
               "Normal": "1db71cee-e17e-46e4-b598-315aa766a5d0",
               "Sunset": "6e1b5236-597c-4e34-b10f-bfa7babb5f8d",
               "Sunrise": "67ecef8c-3af7-4f16-b818-07c16a36b158",
               "Evening": "85b86aa6-35bf-411f-981d-ef6dc01061bd",
               "UnderWater": "485d323f-aad7-403c-b88e-70a5cbb5a89b",
               "Lamp": "088429a1-b17c-4b7a-96c0-205a0027e998",
               "DarkRoom": "8a5b2ec1-f67f-4301-b179-2244b1738cb7",
               "NightLight": "58b36976-21d0-4fe3-8878-4568a73913d7",
               "Night3": "67a083fc-7c62-4896-8c43-618248841b04",
               "Christmas": "e517b462-4a81-4a67-b420-7fcf711d9f97"}
    __light = {"Desk": "d073d527ef8f",
               "Strip": "d073d528d383",
               "Entry": "d073d5384329",
               "Lamp": "d073d5120593",
               "TV Left": "d073d55b449b",
               "TV Right": "d073d536052a",
               "Desk Left": "d073d52be6bf",
               "Desk Right": "d073d527ef8f"
               }
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    log = logging.getLogger(__name__)

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
        self.log.info("All lights toggled")
        return

    '''
    Start the test system
    '''

    def lightOn(self, id, color):
        try:
            response = requests.put(self.__prefix + 'lights/' + id + '/state', data={"power": "on", "brightness": "0.3",
                                                                                     "color": color},
                                    headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        self.log.info(response.status_code)
        if response.status_code != 207:
            raise Exception(json_data['error'])
        else:
            for item in json_data:
                self.log.info(item)
        return

    '''
    Start the test system
    '''

    def lightOff(self, id):
        try:
            response = requests.put(self.__prefix + 'lights/' + id + '/state', data={"power": "off"},
                                    headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        self.log.info(response.status_code)
        if response.status_code != 207:
            raise Exception(json_data['error'])
        else:
            for item in json_data:
                self.log.info(item)
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
        if response.status_code != 200:
            raise Exception(json_data['error'])
        for light in json_data:
            if light['connected']:
                if light['power'] == 'off':
                    response = requests.put(self.__prefix + 'lights/all/state', data={"power": "on"},
                                            headers=self.__header)
                    self.log.info("Light " + light['label'] + " on")
                    # self.log.info(response.status_code)
            else:
                self.log.error("Problem with light: " + light['label'] + " - " + light['id'])
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
        if response.status_code != 200:
            raise Exception(json_data['error'])
        for light in json_data:
            if light['power'] == 'on':
                response = requests.put(self.__prefix + 'lights/all/state', data={"power": "off"},
                                        headers=self.__header)
                self.log.info("All lights off")
        return

    '''
    List my Scenes
    '''

    def activateScene(self):
        try:
            response = requests.put(self.__prefix + 'scenes/scene_uuid:/activate',
                                    headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        if response.status_code != 207:
            raise Exception(json_data['error'])
        print json_data
        for light in json_data:
            self.log.info(light)
        return

    '''
    List my Scenes
    '''

    def listScenes(self):
        try:
            response = requests.get(self.__prefix + 'scenes', headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        if response.status_code != 200:
            raise Exception(json_data['error'])
        for light in json_data:
            self.log.info(light['name'] + " - " + light['uuid'])
        return

    '''
    Puls
    '''

    def pulseAll(self, color):
        if not color:
            color = "green"
        try:
            response = requests.post(self.__prefix + 'lights/all/effects/pulse',
                                     data={"period": .1, "cycles": 5, "color": color},
                                     headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        if response.status_code != 207:
            raise Exception(json_data['error'])
        # self.log.info(json_data)
        return

    '''
    List all lights
    '''

    def listLightsPretty(self):

        table = PrettyTable()
        lights_list = []

        try:
            response = requests.get(self.__prefix + 'lights/all', headers=self.__header)
        except requests.ConnectionError:
            raise Exception("REST Server not found!")
        json_data = json.loads(response.text)
        if response.status_code != 200:
            raise Exception(json_data['error'])
        for light in json_data:
            table.field_names = ["Key", "Value"]
            table.add_row(["Label", light['label']])
            table.add_row(["Id", light['id']])
            table.add_row(["Type", light['product']['name']])
            table.add_row(["Group", light['group']['name']])
            table.add_row(["Connected", light['connected']])
            if light['power'] == 'on':
                table.add_row(["Power", light['power']])
                table.add_row(["Brightness", light['brightness']])
                table.add_row(["Hue", light['color']['hue']])
                table.add_row(["Saturation", light['color']['saturation']])
                table.add_row(["Kelvin", light['color']['kelvin']])
                if light['product']['identifier'] == 'lifx_z':
                    table.add_row(["Zone Count", light['zones']['count']])
            else:
                table.add_row(["Power", light['power']])
            print table
            table.clear()
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
        if response.status_code != 200:
            raise Exception(json_data['error'])
        for light in json_data:
            self.log.info("Label     : {0}".format(light['label']))
            self.log.info("Id        : {0}".format(light['id']))
            self.log.info("Type      : {0}".format(light['product']['name']))
            self.log.info("Group     : {0}".format(light['group']['name']))
            self.log.info("Connected : {0}".format(light['connected']))
            if light['power'] == 'on':
                self.log.info("Power     : {0}".format(light['power']))
                self.log.info("Brightness: {0}".format(light['brightness']))
                self.log.info("Hue       : {0}".format(light['color']['hue']))
                self.log.info("Sat       : {0}".format(light['color']['saturation']))
                self.log.info("Kelvin    : {0}".format(light['color']['kelvin']))
                if light['product']['identifier'] == 'lifx_z':
                    self.log.info("Zone Count: {0}".format(light['zones']['count']))
                self.log.info("\n")
            else:
                self.log.info("Power     : {0}\n".format(light['power']))

        return
