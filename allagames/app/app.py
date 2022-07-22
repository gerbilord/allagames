import random
import logging
from flask import Flask, render_template, request, json, jsonify
from flask_socketio import SocketIO, send, join_room, leave_room, emit, rooms
from python.gameWrapper import gameWrapper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app) #, logger=True, engineio_logger=True)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

users = ['Ale']
shrinkChessLobbies = []
shrinkChessGames = []

updates = [
    {
        'title': 'Update 0.02',
        'content':'Minor UI improvements',
        'date_posted':'12/30/2019'
    },
    {
        'title': 'Update 0.01',
        'content':'Shrink Chess v0.01 out. Check/checkmate/stalemate not implemented. To win take the enemy king. Person to create lobby is always white.',
        'date_posted':'12/29/2019'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', updates=updates)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/createLobby", methods=['GET','POST'])
def createLobby():
    input = request.get_json()

    gameId = len(shrinkChessGames)
    print("Created lobby with game Id: " + str(gameId))

    shrinkChessLobbies.append({'name':input['lobbyName'], 'type':input['lobbyType'], 'gameId':gameId})
    shrinkChessGames.append(gameWrapper(2, gameId, socketio))

    return jsonify(gameId=gameId)

@app.route("/getLobbies", methods=['GET','POST'])
def getLobbies():
    lobbies = shrinkChessLobbies
    return jsonify(lobbies)


@app.route("/shrinkChess", methods=['GET','POST'])
def shrinkChess():
    return render_template('shrinkChess.html')


@socketio.on('connect')
def connect():
    pass


@socketio.on('join', namespace='/shrinkChess')
def on_join(data):
    print("Player joined room/game: " + str(data['gameId']))
    room = int(data['gameId'])
    join_room(room)
    send('You entered the room: ' + str(room))
    shrinkChessGames[room].addPlayer(request.sid)
    if(shrinkChessGames[room].gameStarted):
        deleteLobby(room)


@socketio.on('gameMove', namespace='/shrinkChess')
def gameMove(data):
    room = int(data['room'])
    move = (data['fromTile'], data['toTile'])
    send('You sent move ' + str(move))
    shrinkChessGames[room].recieveMoves(request.sid, move)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

def deleteLobby(room):
    for x in range(len(shrinkChessLobbies)):
        if(shrinkChessLobbies[x]['gameId']==room):
            del shrinkChessLobbies[x]
            break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
