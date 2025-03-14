#!/usr/bin/env python3

from flask import Flask, jsonify, request
import requests
import xmltodict
from datetime import datetime
import math

app = Flask(__name__)
iss_url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'

def url_to_xml_to_listdict(path: str) -> list[dict[str, float]]:
    '''
    Ingests the ISS data using the requests library and returns it in list of dictionaries format for the rest of the script to use

    Args:
        path (str): The filepath/URL of the ISS trajectory data

    Returns:
        list[dict]: A list of each state vector as a dictionary. Contains the EPOCH, X, Y, Z, X_DOT, Y_DOT, Z_DOT
    '''
    response = requests.get(path)
    response.raise_for_status() # causes an HTTP Error if a bad response is received
    data = response.text
    data = xmltodict.parse(data) # data is now a Python dictionary format of the XML file

    # analyzing the downloaded XML file, we can see the "path" to the state vectors, e.g. our relevant data
    # we'll extract this with the following line
    relevant_data = data['ndm']['oem']['body']['segment']['data']['stateVector']

    # let's make a list with each entry being a dictionary of the values of each state vector
    listDict = []
    for vec in relevant_data:
        listDict.append(
                { # AI Used to Debug "#text" is added because xmltodict automatically creates another dictionary to store the raw string
                    "EPOCH": vec["EPOCH"],
                    "X": float(vec["X"]["#text"]) if isinstance(vec["X"], dict) else float(vec["X"]),
                    "Y": float(vec["Y"]["#text"]) if isinstance(vec["Y"], dict) else float(vec["Y"]),
                    "Z": float(vec["Z"]["#text"]) if isinstance(vec["Z"], dict) else float(vec["Z"]),
                    "X_DOT": float(vec["X_DOT"]["#text"]) if isinstance(vec["X_DOT"], dict) else float(vec["X_DOT"]),
                    "Y_DOT": float(vec["Y_DOT"]["#text"]) if isinstance(vec["Y_DOT"], dict) else float(vec["Y_DOT"]),
                    "Z_DOT": float(vec["Z_DOT"]["#text"]) if isinstance(vec["Z_DOT"], dict) else float(vec["Z_DOT"])
                })
        # makes and appends a dictionary for each state vector
    return listDict

def speed(a: float, b: float, c: float) -> float:
    '''Given three floats for the Cartesian velocity vectors, calculates the resultant magnitude/speed'''
    return math.sqrt(a**2 + b**2 + c**2)

@app.route('/epochs', methods=['GET'])
def epochs():
    '''Returns the entire dataset, also factoring in if a limit and offset are given'''
    data = url_to_xml_to_listdict(iss_url)
    limit = request.args.get('limit', type = int)
    offset = request.args.get('offset', type = int, default = 0) #if a limit is given but no offset, assume still starting at 0
    
    if limit:
        return jsonify(data[offset:offset+limit]) # returns a subset of the dataset
    else:
        return jsonify(data) # no limit specified -> return whole dataset

@app.route('/epochs/<epoch>', methods=['GET'])
def get_epoch(epoch):
    '''Returns the state vectors for a specified epoch'''
    data = url_to_xml_to_listdict(iss_url)
    ep = next((i for i in data if i['EPOCH']==epoch), None)
    if ep: return jsonify(ep)
    else: return jsonify({"Error": "Epoch Not Found"}), 404

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def get_speed(epoch):
    '''Returns the instantaneous speed for a specified epoch'''
    data = url_to_xml_to_listdict(iss_url)
    ep = next((i for i in data if i['EPOCH']==epoch), None)
    if ep: 
        ep_speed = speed(ep['X_DOT'], ep['Y_DOT'], ep['Z_DOT'])
        return jsonify({"EPOCH": epoch, "Instantaneous_Speed": ep_speed})
    else: return jsonify({"Error": "Epoch Not Found"}), 404

@app.route('/epochs/<epoch>/location', methods=['GET'])
def get_loc(epoch):
    '''Returns the lat, lon, altitude, and geoposition for a specified epoch'''

@app.route('/now', methods=['GET'])
def get_now():
    data = url_to_xml_to_listdict(iss_url)
    now = datetime.utcnow() # current time at runtime
    closest = min(data, key=lambda epo: abs (
        now - datetime.strptime(epo["EPOCH"], "%Y-%jT%H:%M:%S.%fZ")
        ))
    
    # need to make new dict to add instantaneous speed
    return jsonify({
        "EPOCH": closest['EPOCH'],
        "X": closest['X'],
        'Y': closest['Y'],
        "Z": closest["Z"],
        "X_DOT": closest["X_DOT"],
        "Y_DOT": closest["Y_DOT"],
        'Z_DOT': closest['Z_DOT'],
        "Instantaenous_Speed": speed(closest['X_DOT'], closest['Y_DOT'], closest['Z_DOT'])
    })

if __name__ == '__main__': # not calling a main method this time, but running our app
    app.run(host='0.0.0.0', port = 5000, debug = True)
