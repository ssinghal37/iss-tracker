# Homework 05 - ISS Tracking - Fountains of Flask

## Overview
This directory/homework is an extension of ../homework04 that turns the Python script into a Flask web application. This directory contains Python scripts that take in data about the ISS's trajectory from NASA and display information based on various endpoints the user provides. Everything is containerized and runs via Docker

The data can be downloaded from the [ISS Trajectory Data](https://spotthestation.nasa.gov/trajectory_data.cfm) page, or you can follow the instructions below for using the requests library to import it as a part of the script.

## File Summary
This directory includes a Python script and a tester file
### iss\_tracker.py
- Ingests NASA's ISS data using the requests library, and converts it to a list of dictionaries
    - Each of the dictionaries in this list are one epoch, containing an epoch date and timestamp, a position (X, Y, Z), and velocity in three directions (X_DOT, Y_DOT, Z_DOT)
    - Has a file URL coded in, but that one URL can be replaced with an updated XML from the same ISS trajectory data page
- Includes some helper functions
    - *url\_to\_xml\_to\_listdict* takes in a url (to the xml data) and returns it as a list of Python dictionaries for processing
    - *speed* takes in three floats and outputs their resultant magnitude
- Does not output anything on it's own. See below for instructions on running and testing the different routes/endpoints
    Reading the output should be pretty self explanatory, as it is accompanied with text explaining which numbers are what.

### test\_iss\_tracker.py
- Ensures that all the functions within iss\_tracker.py are working as expected
- Sets up a test client and ensures that all the functions return a status code of 200 (returning and working properly) as well as proper data types


## Running The Scripts

There are two options. First, you can work within this homework05 directory and/or clone it. Otherwise, you can run `docker pull ssinghal37/homework05:1.0` and test the commands wherever you please, as this container has been pushed to Docker. If pulling from Docker, skip to step number 5

1. If applicable, run `git clone https://github.com/ssinghal37/singhal-coe332.git` and navigate to the homework05 directory, most likely done by running `cd singhal-coe322/homework05/`
2. Ensure Docker is installed correctly with `docker --version`. Assuming those testing these are using the TACC Virtual Machine, you should be good to go
3. Once in *homework05/*, use your preferred text editor to create a file called `requirements.txt`. This file should have the following on each line:
    - Flask==3.0.2
    - pytest==8.3.4
    - xmltodict
    - requests
4. Build a Docker image by running `docker build -t ssinghal37/homework05:1.0 ./` This command will use the Dockerfile script to install all the necessary libraries and containerize the scripts within that image
5. Next, run `docker run --name "iss-tracker-app" -d -p 5000:5000 ssinghal37/homework05:1.0`. Beware, if something is already running on port 5000, that will need to be stopped/removed first!
    - The -d tag will detach the container, meaning we can still run commands in the terminal while it runs in the background
    - Do docker ps -a to see all current containers. From here, you can also stop/remove containers by doing `docker stop <id>` or `docker rm <id>`
6. You should automatically be back at the command line. From here, you can test the different endpoints using `curl 'localhost:5000<input>'`
Here is a list of the different routes provided for `<input>`:
- /epochs
    - Returns the entire data set
- /epochs?limit=X
    - Limits the data set to the first X entries
- /epochs?limit=X&offset=Y
    - Limits to the first X entries starting at Y
- /epochs/<epoch>
    - Shows the state vectors for a specified epoch
- /epochs/<epoch>/speed
    - Returns the instantaneous speed for a specified epoch
- /now
    - Shows the state vectors and instantaneous speed for the epoch closest to the execution time
    - Based on UTC time. CST in Austin, TX is UTC -6:00 so think of the epoch timestamp as 6 hours in advance of local time
7. Make sure to run docker stop and docker rm after usage to free up port 5000 for future use

If you wish to incorporate more recent ISS trajectory data, first get the URL to that XML file. Now, you have two options.
1. Go to the *homework05* directory and replace the URL in *iss_tracker.py*, and then rebuild the Docker image (this time as ssinghal37/homework05:2.0) (or whatever version you'd like to name it)
2. Alternatively, run `docker run --rm -it ssinghal37/homework04:1.0` and it will open up an interactive session within the container. From here, you can use an installed text editor (or add your own) to update the link and directly run the script/tester. This option will require opening multiple windows since you will not have detached the container session from your terminal. 
    

## Sources

1. [ISS Trajectory Data Home Page](https://spotthestation.nasa.gov/trajectory_data.cfm)
2. [Trajectory Data XML in use](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS\_OEM/ISS.OEM\_J2K\_EPH.xml)
3. Google Search for debugging questions and how to use pytest with Flask
4. COE 332 ReadTheDocs for reminders on Docker commands

