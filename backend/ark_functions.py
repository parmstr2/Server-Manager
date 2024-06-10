import socket

def send_query(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    try:
        sock.sendto(message, (ip, port))

        data, _ = sock.recvfrom(4096)
        return data
    except socket.timeout:
        print("Request timed out")
        return None
    finally:
        sock.close()

def parse_string(data):
    """Parse a null-terminated string from data."""
    string_end = data.find(b'\x00')
    if string_end == -1:
        return "", data
    return data[:string_end].decode('utf-8'), data[string_end + 1:]

def parse_info(data):
    """Parse the server response."""
    if data[4] == 0x41:
        return 0
    elif data[4] != 0x49:
        raise ValueError("Not a valid A2S_INFO response")

    result = {}
    data = data[5:]  # Skip header and type

    # Protocol version
    result['protocol'], data = data[0], data[1:]

    # Server name
    result['server_name'], data = parse_string(data)

    # Map name
    result['map_name'], data = parse_string(data)

    # Game directory
    result['game_directory'], data = parse_string(data)

    # Game description
    result['game_description'], data = parse_string(data)

    # Steam Application ID
    result['app_id'] = int.from_bytes(data[:2], byteorder='little')
    data = data[2:]

    # Number of players
    result['players'], data = data[0], data[1:]

    # Maximum players
    result['max_players'], data = data[0], data[1:]

    # Number of bots
    result['bots'], data = data[0], data[1:]

    # Server type
    result['server_type'], data = data[0], data[1:]

    # Environment
    result['environment'], data = data[0], data[1:]

    # Visibility
    result['visibility'], data = data[0], data[1:]

    # VAC
    result['vac'], data = data[0], data[1:]

    # Version
    result['version'], data = parse_string(data)

    return result

def parse_players(data):
    if data[4] == 0x41:
        return 0
    elif data[4] != 0x44:
        raise ValueError("Not a valid A2S_Player response")
    
    result = {}
    data: bytes = data[5:]
    num_players = data[0]
    data = data[1:]
    for i in range(num_players):
        index = data[0]
        data = data[1:]
        result[index] = data.split(b"\x00")[0].decode("utf-8")

    return result

def parse_rules(data):
    if data[4] == 0x41:
        return 0
    elif data[4] != 0x45:
        raise ValueError("Not a valid A2S_Rule response")
    
    result = {}
    data: bytes = data[5:]
    num_rules = data[0]
    data:bytes = data[2:]
    data = data.split(b'\x00')
    
    for i in range(num_rules):
        result[data[0].decode("utf-8")] = data[1].decode("utf-8")
        data = data[2:]

    return result

class arkServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def query_info(self):
        message = b'\xFF\xFF\xFF\xFF\x54Source Engine Query\x00'
        response = send_query(self.ip, self.port, message)
        if response:
            parsed_data = parse_info(response)

            if parsed_data == 0:
                response = send_query(self.ip, self.port, message+response[5:])
                parsed_data = parse_info(response)

            return parsed_data
        
    def query_players(self):
        message = b'\xFF\xFF\xFF\xFF\x55\xFF\xFF\xFF\xFF'
        response = send_query(self.ip, self.port, message)
        if response:
            parsed_data = parse_players(response)

            while parsed_data == 0:
                response = send_query(self.ip, self.port, message[0:5]+response[5:])

                parsed_data = parse_players(response)
            
            return parsed_data
        
    def query_rules(self):
        message = b'\xFF\xFF\xFF\xFF\x56\xFF\xFF\xFF\xFF'
        response = send_query(self.ip, self.port, message)
        if response:
            parsed_data = parse_rules(response)

            while parsed_data == 0:
                response = send_query(self.ip, self.port, message[0:5]+response[5:])

                parsed_data = parse_rules(response)
            
            return parsed_data

    def query_ping(self):
            message = b'\xFF\xFF\xFF\xFF\x69'
            response = send_query(self.ip, self.port, message)
            if response:
                parsed_data = response[4]
                
                return parsed_data

print(arkServer("192.168.2.19", 27015).query_ping())