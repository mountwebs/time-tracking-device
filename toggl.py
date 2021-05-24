import urequests
import ujson

def post_test():
  response = urequests.post("http://jsonplaceholder.typicode.com/posts", data = "some dummy content")
  print(response.json())


def toggl_test():

import ujson
  import urequests
  h = ujson.dumps("{'content-type': 'application/json', 'Authorization': 'Basic '}")
  d = ujson.dumps({'time_entry': {'description': 'Meeting with possible'}})
  response = urequests.post("https://api.track.toggl.com/api/v8/time_entries/start", headers = h, data = d)
  print(response.json())

