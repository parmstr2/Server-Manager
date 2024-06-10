import os

MANAGER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if(not os.path.exists(MANAGER_DIR + "/Servers/Minecraft")):
    print("Minecraft directory not found making new directory")
    os.makedirs(MANAGER_DIR + "/Servers/Minecraft")
else:
    print("Minecraft directory already exists")

if(not os.path.exists(MANAGER_DIR + "/Servers/ARK")):
    print("ARK directory not found making new directory")
    os.makedirs(MANAGER_DIR + "/Servers/ARK")
else:
    print("ARK directory already exists")

if(not os.path.exists(MANAGER_DIR + "/Servers/Palworld")):
    print("Palworld directory not found making new directory")
    os.makedirs(MANAGER_DIR + "/Servers/Palworld")
else:
    print("Palworld directory already exists")