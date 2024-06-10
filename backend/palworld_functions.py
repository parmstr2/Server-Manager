import requests
import json

class palworldServer:
  def __init__(self, ip):
    self.ip = ip
  #Server Info
  def getInfo(self):
    try:
      url = f"http://{self.ip}/v1/api/info"

      payload={}
      headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("GET", url, headers=headers, data=payload, timeout=2)

      return json.loads(response.text)
    except:
      print("Failed to fetch info")



  #Player list
  def getPlayers(self):
    try:
      url = f"http://{self.ip}/v1/api/players"

      payload={}
      headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("GET", url, headers=headers, data=payload, timeout=2)

      return json.loads(response.text)
    except:
      print("Failed to fetch players")


  #Server settings
  def getSettings(self):
    try:
      url = f"http://{self.ip}/v1/api/settings"

      payload={}
      headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("GET", url, headers=headers, data=payload, timeout=2)

      return json.loads(response.text)
    except:
      print("Failed to fetch settings")



  #Server metrics
  def getMetrics(self):
    try:
      url = f"http://{self.ip}/v1/api/metrics"

      payload={}
      headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("GET", url, headers=headers, data=payload, timeout=2)

      return json.loads(response.text)
    except:
      print("Failed to fetch metrics")



  #Anouncement
  def anounce(self, message):
    try:
      url = f"http://{self.ip}/v1/api/announce"

      payload = json.dumps({
        "message": message
      })
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to anounce")



  #Kick player
  def kick(self, id):
    try:
      url = f"http://{self.ip}/v1/api/kick"

      payload = json.dumps({
        "userid": id,
        "message": "You are kicked."
      })
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to kick player")



  #Ban player
  def ban(self, id):
    try:
      url = f"http://{self.ip}/v1/api/ban"

      payload = json.dumps({
        "userid": id,
        "message": "You are banned."
      })
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to ban player")



  #Unban
  def unban(self, id):
    try:
      url = f"http://{self.ip}/v1/api/unban"

      payload = json.dumps({
        "userid": id
      })
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to unban player")



  #Save
  def save(self):
    try:
      url = f"http://{self.ip}/v1/api/save"

      payload={}
      headers = {
          'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to save")



  #Shutdown
  def shutdown(self):
    try:
      url = f"http://{self.ip}/v1/api/shutdown"

      payload = json.dumps({
        "waittime": 10,
        "message": "Server will shutdown in 10 seconds."
      })
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to shutdown the server")



  #Stop
  def stop(self):
    try:
      url = f"http://{self.ip}/v1/api/stop"

      payload={}
      headers = {
          'Authorization': 'Basic YWRtaW46Qml0Y2g='
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=2)

      return response
    except:
      print("Failed to stop the server")
  
  def getAll(self):
    payload = {}

    info = self.getInfo()
    if info:
      for key in info:
        payload[key] = info[key]

    players = self.getPlayers()
    if players:
      for key in players:
        payload[key] = players[key]

    settings = self.getSettings()
    if settings:
      for key in settings:
        payload[key] = settings[key]

    metrics = self.getMetrics()
    if metrics:
      for key in metrics:
        payload[key] = metrics[key]

    return payload