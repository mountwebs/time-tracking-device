import requests
from requests.auth import HTTPBasicAuth
import json
import pprint

class TogglApi:
    def __init__(self, api_key):
        self.api_key = api_key

    def startProject (self, project): 
        dataObject = {"time_entry":{"created_with":"python", "pid": project}}
        try:
            r = requests.post('https://api.track.toggl.com/api/v8/time_entries/start',
                auth=HTTPBasicAuth(self.api_key, 'api_token'), 
                data=json.dumps(dataObject))
            print(r.json())
        except Exception as e: print(e)

    def getCurrentTimeEntry (self):
        try:
            r = requests.get('https://api.track.toggl.com/api/v8/time_entries/current',
                auth=HTTPBasicAuth(self.api_key, 'api_token'))
            if (not r.json()['data']): return False
            return r.json()['data']['id']
        except Exception as e: print(e)
        return False

    def stop (self):
        if (not self.getCurrentTimeEntry()):
            print("No runing time entry")
            return False
        timeEntry = self.getCurrentTimeEntry()
        try:
            r = requests.put('https://api.track.toggl.com/api/v8/time_entries/' + str(timeEntry) + '/stop',
                auth=HTTPBasicAuth(self.api_key, 'api_token'))
            print(r.json())
        except Exception as e: print(e)

    def getWorkspaces (self):
        try:
            r = requests.get('https://api.track.toggl.com/api/v8/workspaces',
                auth=HTTPBasicAuth(self.api_key, 'api_token'))
            print(r.json())
        except Exception as e: print(e)

    def getProjects (self, workspaceId):
        try:
            r = requests.get('https://api.track.toggl.com/api/v8/workspaces/' + str(workspaceId)  + '/projects',
                auth=HTTPBasicAuth(self.api_key, 'api_token'))
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(r.json())
        except Exception as e: print(e)


