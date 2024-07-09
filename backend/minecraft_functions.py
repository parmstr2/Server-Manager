import socket, struct, random, json, os, requests

class MinecraftQuery:
    def __init__(self, host, port, timeout=5):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.session_id = random.randint(0, 2147483648) & 0x0F0F0F0F

    def handshake(self):
        #It's magic
        packet = b"\xFE\xFD"
        #Type
        packet += struct.pack("!B", 0x09)
        #Session ID
        packet += struct.pack(">l", self.session_id)

        #Handshake response
        response = self.send_packet(packet)

        #If there was a response received
        if response:
            #Try unpacking the response
            try:
                #Decode the challenge token
                token = int(response[5:-1].decode('utf-8'))
                return token
            except Exception as e:
                print(f"Failed to unpack handshake response: {e}")
                return None
        else:
            return None

    #function to send packet to server
    def send_packet(self, packet_data):
        try:
            #send packet to given host:port
            self.sock.sendto(packet_data, (self.host, self.port))

            #retrieve data from the server
            data, _ = self.sock.recvfrom(2048)

            return data
        except socket.timeout:
            print("Request timed out. The server may be down or not support the query protocol.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def full_stat(self):
        #Get challenge token from the server
        token = self.handshake()

        #If we failed to get the token
        if token is None:
            return None

        #Create challenge token bytes
        token_bytes = struct.pack(">l", token)

        #Full stat request
        #Magic
        packet = b"\xFE\xFD"
        #Type
        packet += struct.pack("!B", 0x00)
        #Session id
        packet += struct.pack(">l", self.session_id)
        #Challenge token
        packet += token_bytes
        #Padding
        packet += b"\x00\x00\x00\x00"

        #Stat response
        response = self.send_packet(packet)

        #If we receive a response
        if response:
            try:
                #skip irrelevant data
                data = response[16:]
                #seperate player list from stats
                items = data.split(b'player_')
                #split the stats
                info = items[0].split(b'\x00')
                #split the players
                players = items[1].split(b'\x00')

                #Dict to hold the server stats
                server_info = {}
                #key for the dict
                last_key = ''

                for i in range(len(info)):
                    #if the value is a key
                    if i % 2 == 0:
                        last_key = info[i].decode('utf-8')
                    #else the value is a stat
                    else:
                        server_info[last_key] = info[i].decode('utf-8')

                #player list
                server_info['players'] = [player.decode('utf-8') for player in players if player]

                return server_info
            except Exception as e:
                print(f"Failed to parse full stat response: {e}")
                return None
        else:
            return None

class MakeServer:
    def __init__(self, dir, data):
        self.dir = dir
        self.data = data

    def createDir(self):
        if os.path.exists(self.dir):
            return "Server with that name already exists"
        else:
            os.makedirs(self.dir)

            return "Folder Created"
        
    def createFiles(self):
        eula = open(f"{self.dir}/eula.txt", "w")
        eula.write("eula=true")
        eula.close

        managerFile = open(f"{self.dir}/manager.json", "w")
        json.dump(self.data, managerFile)
        managerFile.close()

    def getVersions(self):
        gameVersions = {}

        response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
        for res in response.json()['versions']:
            gameVersions[res["id"]] = res["url"]
        
        return gameVersions

    def fetchServer(self):
        response = requests.get(self.getVersions()[self.data["version"]])
        serverJar = requests.get(response.json()["downloads"]["server"]["url"])

        path = self.dir + "/minecraft_server.jar"

        with open(path, "wb") as jar:
            jar.write(serverJar.content)

    def make(self):
        self.createDir()
        self.fetchServer()
        self.createFiles()
        

        
if __name__ == "__main__":
    host = "192.168.2.19"
    port = 25566
    
    query = MinecraftQuery(host, port)
    try:
        server_info = query.full_stat()
        if server_info:
            print(json.dumps(server_info, indent=4))
        else:
            print("Failed to retrieve server information.")
    except Exception as e:
        print(f"An error occurred: {e}")
