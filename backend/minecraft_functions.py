import struct, socket, variables, os, urllib.request as urllib, subprocess, requests, json

index_url = f"https://files.minecraftforge.net/net/minecraftforge/forge/index_{variables.minecraftVersion}.html"
url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{variables.minecraftVersion}-{variables.forgeVersion}/forge-{variables.minecraftVersion}-{variables.forgeVersion}-installer.jar"
file_name = f"forge-{variables.minecraftVersion}-{variables.forgeVersion}-installer.jar"

class Packet:
    def __init__(self, type, session, payload=b'') -> None:
        self.type = type
        self.sessionID = session
        self.payload = payload

    def pack(self) -> bytes:
        packet = b'\xFE\xFD'
        packet += struct.pack("!B", self.type)
        packet += struct.pack(">l", self.sessionID)
        packet += self.payload

        return packet



class Query:
    def __init__(self, host, port:int=25565, timeout=5) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)

    def handshake(self) -> None:
        self.session = 1
        packet = Packet(9, self.session)

        self.sock.sendto(packet.pack(), (self.host, self.port))
        response = self.receive()
        self.token = struct.pack('>l', int(response[2][:-1]))

    def receive(self) -> tuple[int, bytes, bytes]:
        response = self.sock.recv(4096)
        type = response[0]
        session = response[1:5]
        payload = response[5:]

        return type, session, payload
    
    def request(self) -> dict:
        self.handshake()

        payload = self.token + b'\x00\x00\x00\x00'
        packet =  Packet(0, self.session, payload)
        self.sock.sendto(packet.pack(), (self.host, self.port))
        raw_response = self.receive()
        return self.read(raw_response[2])
    
    def get_status(self):
        response = self.request()
        return response
    
    @staticmethod
    def read(response: bytes) -> dict:
        response = response[11:]

        stats, players = response.split(b'\x00\x00\x01player_\x00\x00')

        stats = stats.split(b'\x00')

        stats = [stat.decode("utf-8") for stat in stats]

        stats[0] = "motd"
        key_field = True
        data = {}
        for x, y in enumerate(stats):
            if key_field:
                data[y] = stats[x+1]
                key_field = False
            else:
                key_field = True

        for key in ["numplayers", "maxplayers", "hostport"]:
            data[key] = int(data[key])
        
        players = players[:-2]
        players = players.split(b'\x00')

        data["players"] = [player.decode("utf-8") for player in players if player != b""]

        return data



class minecraftServer:
    def __init__(self, index):
        self.index = index

    

    def get_all(self):
        query = Query(self.ip, self.port)

        return query.get_status()
    

    
def fetchInstaller(server_num):
    if not os.path.exists(f"./Manager/Minecraft Server {server_num}/libraries"):
        if not os.path.exists(f"./Manager/Minecraft Server {server_num}/{file_name}"):
            if not os.path.exists(f"./Manager/Minecraft Server {server_num}"):
                os.makedirs(f"./Manager/Minecraft Server {server_num}")
                print("Created Directory")
            else:
                print("Directory Exists")
            
            print("Entering directory")
            os.chdir(f"./Manager/Minecraft Server {server_num}")

            opener = urllib.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
            urllib.install_opener(opener)
            urllib.urlretrieve(url, file_name)

            print("Downloaded Installer")
        else:
            print("Installer already downloaded")
        
        subprocess.run(["java", "-jar", file_name, "--installServer"])

        os.remove(file_name)
    else:
        print("Server already installed")



def minecraftChecks():
    eula = """
        #By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
        #Tue Apr 30 15:29:03 ADT 2024
        eula=true
    """

    with open('eula.txt', 'w') as f:
        f.write(eula)

    server_properties = f"""
        #Minecraft server properties
        spawn-protection=0
        max-tick-time=60000
        query.port={variables.minecraftPort}
        generator-settings=
        force-gamemode=false
        allow-nether=true
        gamemode=survival
        broadcast-console-to-ops=true
        enable-query=true
        player-idle-timeout=0
        difficulty={variables.minecraftDifficulty}
        spawn-monsters=true
        op-permission-level=4
        pvp={variables.minecraftPVP}
        snooper-enabled=true
        level-type=default
        hardcore={variables.minecraftHardcore}
        enable-command-block=true
        max-players={variables.minecraftMaxPlayers}
        network-compression-threshold=256
        resource-pack-sha1=
        max-world-size=29999984
        server-port={variables.minecraftPort}
        server-ip=
        spawn-npcs=true
        allow-flight=true
        level-name={variables.minecraftWorldName}
        view-distance=12
        resource-pack=
        spawn-animals=true
        white-list=true
        rcon.port={variables.minecraftRCONPort}
        generate-structures=true
        online-mode=true
        max-build-height=256
        level-seed=
        prevent-proxy-connections=false
        motd={variables.minecraftMOTD}
        enable-rcon=true
    """

    with open('server.properties', 'w') as f:
        f.write(server_properties)

    run = """
        @echo off
        REM Forge requires a configured set of both JVM and program arguments.
        REM Add custom JVM arguments to the user_jvm_args.txt
        REM Add custom program arguments {such as nogui} to this file in the next line before the %* or
        REM  pass them to this script directly
        java @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.20.1-47.2.0/win_args.txt nogui%*
        pause
    """

    with open('run.bat', 'w') as f:
        f.write(run)

    args = """
        # Xmx and Xms set the maximum and minimum RAM usage, respectively.
        # They can take any number, followed by an M or a G.
        # M means Megabyte, G means Gigabyte.
        # For example, to set the maximum to 3GB: -Xmx3G
        # To set the minimum to 2.5GB: -Xms2500M

        # A good default for a modded server is 4GB.
        # Uncomment the next line to set it.
        -Xms4G
        -Xmx8G
    """

    with open('user_jvm_args.txt', 'w') as f:
        f.write(args)
