# app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from minecraft_functions import MinecraftQuery, MakeServer, getVersions

MANAGER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))

gamesFile = open("games.txt", "r")

# Skip the headers
gamesFile.readline()
games = []

for game in gamesFile:
    words = game.split()
    games.append({"name": words[0], "steam": words[1], "id": words[2], "servers": []})

    if not os.path.exists(MANAGER_DIR + f"/Servers/{words[0]}"):
        print(f"Missing {words[0]} directory, creating it now")
        os.makedirs(MANAGER_DIR + f"/Servers/{words[0]}")

gamesFile.close()

app = Flask(__name__)
CORS(app)

# Placeholder for server statuses
servers = {}
for game in games:
    servers[game["name"]] = {"status": "offline", "players": 0}

def check_server_status(ip:str, port:int=25565):
    query = MinecraftQuery(ip, port)

    return query.full_stat()

def fetch_server(server_name):
    if not os.path.exists(MANAGER_DIR + f"/Minecraft/{server_name}/manager.txt"):
        print("Server not managed.")
    else:
        print("Server managed.")

##########
# Routes #
##########

@app.route('/status/<server_name>', methods=['GET'])
def status(server_name):
    ip, port = fetch_server(server_name)
    status = check_server_status(ip, port)
    return jsonify(status)

@app.route('/new/minecraft/<server_name>', methods=['POST'])
def newMinecraft(server_name):
    data = request.get_json()
    minecraftCreator = MakeServer(MANAGER_DIR + f"\\Servers\\Minecraft\\{server_name}", data)
    minecraftCreator.make()
    return "Server Made"

@app.route('/games', methods=['GET'])
def gamesGames():
    versions = getVersions().keys()
    versionList = []

    for version in versions:
        versionList.append(version)

    for type in games:
        if(os.path.exists(MANAGER_DIR + "/Servers/" + type["name"])):
            type["servers"] = os.listdir(MANAGER_DIR + "/Servers/" + type["name"])
            if type["name"] == "minecraft":
                type["versions"] = versionList
    return jsonify(games)

if __name__ == '__main__':
    #testing
    # print(check_server_status("192.168.2.19", 25566))
    app.run(debug=True)
