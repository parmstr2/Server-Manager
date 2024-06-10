import os
import subprocess
from flask import Flask
from flask_cors import CORS
import sqlite3

import minecraft_functions as minecraft
import palworld_functions as palworld
import ark_functions as ark
import steamCMD

MANAGER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if(not os.path.exists("./database/games.db")):
    os.makedirs("./database")
    db = sqlite3.connect("./database/games.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE games(id integer primary key, game varchar(20), serverName(50))")
else:
    db = sqlite3.connect("./database/games.db")
    cursor = db.cursor()

app = Flask(__name__)
CORS(app)

@app.route("/minecraft/<int:index>", methods=["GET"])
def minecraftInfo(index):
    server = minecraft.minecraftServer(index)
    return server.get_all()

@app.route("/palworld", methods=["GET"])
def palworldInfo():
    server = palworld.palworldServer("192.168.2.19:8212")
    return server.getAll()

@app.route("/ark", methods=["GET"])
def arkInfo():
    server = ark.arkServer("192.168.2.19", 27015)
    return server.query_info()

@app.route("/newMinecraftServer", methods=["GET"])
def newMinecraft():
    os.chdir(MANAGER_DIR)
    minecraft.fetchInstaller()
    minecraft.minecraftChecks()
    os.chdir(MANAGER_DIR)

    return "Done"

@app.route("/startMinecraftServer", methods=["GET"])
def startMinecraft():
    os.chdir(MANAGER_DIR + "/Manager/Minecraft Server")
    subprocess.Popen(f"start cmd.exe /k run.bat", shell=True)
    os.chdir(MANAGER_DIR)

    return "Done"

@app.route("/getMinecraftConfigs", methods=["GET"])
def getConfigs():
    os.chdir(MANAGER_DIR + "/Manager/Minecraft Server/config")
    files = os.listdir("./")
    os.chdir(MANAGER_DIR)

    return files

@app.route("/getMinecraftConfig/<string:fileName>", methods=["GET"])
def getConfig(fileName):
    os.chdir(MANAGER_DIR + "/Manager/Minecraft Server/config")
    file = open(fileName)
    contents = file.read()
    os.chdir(MANAGER_DIR)

    return contents

@app.route("/newPalworldServer", methods=["GET"])
def newPalworld():
    steamCMD.fetchSteamCMD()

    return steamCMD.updateServer(2394010)

@app.route("/startPalworldServer", methods=["GET"])
def startPalworld():
    return

@app.route("/newARKServer", methods=["GET"])
def newARK():
    return

@app.route("/startARKServer", methods=["GET"])
def startARK():
    return

if __name__ == '__main__':
    app.run(debug=True)