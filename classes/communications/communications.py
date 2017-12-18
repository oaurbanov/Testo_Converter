# coding=utf-8

import datetime
import json

import requests
import logging    # for debbugin requests
import http.client as http_client    # for debbugin requests

from dateutil import parser

# ::::::::::::::::::: GLOBALS :::::: ::::::::::::::::::::::::::::::::::::

# ::::::::::::::::::: Main Class ::::::::::::::::::::::::::::::::::::::::


class Communications:
    """This class contains all the communications atributes and methods"""
    def __init__(self, args):
        self.gt = Gateway(args['Gateway'])
        self.tag = Tag(args['Tag'])
        self.ds = DataSet(args['DataSet'])
        self.url = args['url']
        self.maxSamples = args['maxSamplesToSend']

    def __createPayload(self, jsonPath):
        """ it creates the custom payload for the SmartTags platform"""

        # start by creating json as a dict
        jsonDict = {
            "Gateway": {
                "gatewaySerial": self.gt.gatewaySerial
            },
            "Tag": {
                "TID": self.tag.TID,
                "EPC": self.tag.EPC,
                "timeStamp": "2017-09-22 01:01:01"
            },
            "DataSet": {
                "sensorType": "temperature",
                "logType": "linear",
                "ttLog": 5,
                "timeStamp": "2017-09-22 01:01:01",
                "values": [],
                "timeStamps": []
            }
        }
        # print(json.dumps(jsonDict, indent=2, sort_keys=True))

        # create lists for values and timeStamps
        values = []
        timeStamps = []
        with open(jsonPath, 'r') as jsonfile:
            i = 0
            for line in jsonfile.readlines():
                jsonData = json.loads(line)
                # print(jsonData['ID'])
                timeStamps.append(dateToSend(jsonData['date']))
                temp = (jsonData['temperature']).replace(",", ".")
                values.append(float(temp))
                # print(jsonData['humidity'])
                i += 1
                if (i == self.maxSamples):
                    break

        # building json
        jsonDict["DataSet"]["values"] = values
        jsonDict["DataSet"]["timeStamps"] = timeStamps
        # updating timeStamp of DataSet and Tag to the last timeStamp
        jsonDict["DataSet"]["timeStamp"] = jsonDict["DataSet"]["timeStamps"][-1]
        jsonDict["Tag"]["timeStamp"] = jsonDict["DataSet"]["timeStamps"][-1]
        payload = json.dumps(jsonDict, indent=2, sort_keys=True)
        return payload

    def __verbosingRequestMethod(self):
        http_client.HTTPConnection.debuglevel = 1
        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def __sendHTTP(self, payload):
        '''it sends the json payload in the HTTP post'''
        self.__verbosingRequestMethod()
        headers = {"content-type": "application/json"}
        response = requests.post(self.url, payload,
                                 headers=headers)
        print('\n\n\n------Response-------\n\n' + response.text)

    def sendTestoJSON(self, testoJSON):
        """builds and sends the json file to the web platform"""
        payload = self.__createPayload(testoJSON)
        # print (payload)
        self.__sendHTTP(payload)

# :::::::::::: SubClases and functions ::::::::::::::::


class Gateway:
    def __init__(self, params):
        self.gatewaySerial = params["gatewaySerial"]
        # self.dateGateway = getCurrentTimeStamp()


class Tag:
    def __init__(self, params):
        self.TID = params["TID"]
        self.EPC = params["EPC"]


class DataSet:
    def __init__(self, params):
        self.sensorType = params["sensorType"]
        self.logType = params["logType"]
        self.timeStamp = params["timeStamp"]
        self.values = params["values"]
        self.timeStamps = params["timeStamps"]


def getCurrentTimeStamp(self):
    return datetime.datetime.now().strftime("%Y%m%dT%H%M%S000Z")


def dateToSend(date):
    ''' converts  "6/11/2017 11:16:00 p.m." to "2017-11-06 23:16:00" '''
    rightDate = str(parser.parse(date, dayfirst=True))
    # print(date + ' --> ' + rightDate)
    return rightDate
