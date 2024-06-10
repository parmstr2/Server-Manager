import os
from flask import Flask, jsonify

MANAGER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))

gamesFile = open("games.txt", "r")

#skip the headers
gamesFile.readline()
games = []

for game in gamesFile:
    words = game.split()
    games.append(words)

    if(not os.path.exists(MANAGER_DIR + f"/Servers/{words[0]}")):
        print(f"Missing {words[0]} directory creating it now")
        os.makedirs(MANAGER_DIR + f"/Servers/{words[0]}")

gamesFile.close()

app = Flask(__name__)

@app.route("/home", methods=["GET"])
def home():
    return jsonify(games)

if __name__ == '__main__':
    app.run(debug=True)