import os, urllib.request as urllib, subprocess
from zipfile import ZipFile

url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
file_name = "steamcmd.zip"

def fetchSteamCMD():
    if not os.path.exists(f"../Manager/SteamCMD/steamcmd.exe"):
        if not os.path.exists("../Manager/SteamCMD"):
            os.makedirs("../Manager/SteamCMD")
            print("Created Directory")
        else:
            print("Directory Exists")
        
        print("Entering directory")
        os.chdir("../Manager/SteamCMD")

        print("Downloaded zip")
        
        with ZipFile("steamcmd.zip", 'r') as zipObject:
            zipObject.extractall()

        os.remove(file_name)
    else:
        os.chdir("../Manager/SteamCMD")
        print("SteamCMD already installed")

def updateServer(id: int):
    if id == 2394010:
        game_name = "Palworld Server"
    elif id == 376030:
        game_name = "Ark Server"
    else:
        return "Game not supported"
    
    subprocess.call(["steamcmd.exe", f"+force_install_dir ../{game_name}", "+login anonymous", "+app_update " + str(id), "validate", "+quit"])

    return "Game server installed"