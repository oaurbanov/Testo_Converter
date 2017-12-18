#!/usr/bin/python3

import csv
import json
from classes.communications import communications
# from classes.logging import myLog

# ::::::::::::::::::: TODO :::::::::::::::::::::::::::::::::::::::::::::::::::
# Exeption handling
# Logging improvement
# Graphical Interfaz (optional)
# Create dependences file

# ::::::::::::::::::: Globals ::::::::::::::::::::::::::::::::::::::::::::::::
configPath = 'configFiles/config.json'


# :::::::::::::::::::::::::::HELPERS::::::::::::::::::::::::::::::::::::::::::::
def getJSONFromTestoCSV(csvfile, jsonfile):
    fieldnames = ("ID", "date", "temperature", "humidity")
    reader = csv.DictReader(csvfile, fieldnames, delimiter=';', quotechar='|')
    for idx, row in enumerate(reader):
        if (idx != 0):
            # print(row)
            json.dump(row, jsonfile)
            jsonfile.write('\n')

# :::::::::::::::::::::MAIN:::::::::::::::::::::::::::::::::::::::::::::::::::::::

with open(configPath) as f:
    configData = json.load(f)
    ĺogsPath = configData['logsPath']
    csvPath = configData['csvPath']
    jsonPath = configData['jsonPath']

# log = myLog.myLogClass({'logsFile': logsPath, 'type': '[H0]', 'verb': 0})
# configData['log'] = log
# log.logInfo('Starting Testo_Converter')

with open(csvPath, 'r') as csvfile:
    with open(jsonPath, 'w') as jsonfile:
        getJSONFromTestoCSV(csvfile, jsonfile)


comms = communications.Communications(configData)
comms.sendTestoJSON(jsonPath)
