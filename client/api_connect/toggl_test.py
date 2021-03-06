import os
import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv

load_dotenv()
TOGGL_API_KEY = os.getenv('TOGGL_API_KEY')


dataObject = {"time_entry":{"description":"Meeting with possible clients","created_with":"python", "pid":"171020230"}}
r = requests.post('https://api.track.toggl.com/api/v8/time_entries/start', auth=HTTPBasicAuth(TOGGL_API_KEY, 'api_token'), data=json.dumps(dataObject))
# r = requests.get('https://api.track.toggl.com/api/v8/me', auth=HTTPBasicAuth('TOGGL_API_KEY', 'api_token'))
# Get current time entry: GET https://api.track.toggl.com/api/v8/time_entries/current
#   id: data.id
# r = requests.get('https://api.track.toggl.com/api/v8/time_entries/current', auth=HTTPBasicAuth('TOGGL_API_KEY', 'api_token'))
print(r.json())
