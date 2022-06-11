import os
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse
from dotenv import load_dotenv
import yaml

load_dotenv()
TOGGL_API_KEY = os.getenv('TOGGL_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("project", help="Add the number of the project you want to start",
                    type=int)
args = parser.parse_args()

def getConfig (configPath):
    with open(configPath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            if (not config or not config['projects']): return False
            return config
        except yaml.YAMLError as exc:
            print(exc)
            return false

def getProject (config, projectNum):
    if(projectNum >= len(config['projects'])): 
        raise ValueError("Project number is not valid")
    return config['projects'][projectNum]

def startProject (project):
    dataObject = {"time_entry":{"created_with":"python", "pid": project}}
    try:
        r = requests.post('https://api.track.toggl.com/api/v8/time_entries/start',
            auth=HTTPBasicAuth(TOGGL_API_KEY, 'api_token'), 
            data=json.dumps(dataObject))
        print(r.json())
    except Exception as e: print(e)    

config = getConfig('toggl-projects.yaml')

startProject(getProject(config, args.project))
    









