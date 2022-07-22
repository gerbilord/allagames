from flask import Flask, render_template, request, json, jsonify
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from python.games.shrinkChess import shrinkChess
class gameWrapper:

    def __init__(self, maxPlayers, gameId, socketio):
        self.playersSocketIds = [] # Make a hashmap in the future
        self.maxPlayers = maxPlayers
        self.gameStarted = False
        self.gameId = gameId
        self.socketio = socketio
        self.curPlayer = 0 # Make random
        self.game = shrinkChess()

    def addPlayer(self, socketId):
        if (self.gameStarted is False and len(self.playersSocketIds) < self.maxPlayers):
            self.playersSocketIds.append(socketId)
            self.socketio.emit('message', 'Player joined game. Total players in game is ' + str(len(self.playersSocketIds)), room=self.gameId, namespace='/shrinkChess')
            self.socketio.emit('playerAssign', len(self.playersSocketIds), room=socketId, namespace='/shrinkChess')
            self.socketio.emit('gameUpdateEvent', self.game.getBoardState(), room=self.gameId, namespace='/shrinkChess')

            if(self.maxPlayers == len(self.playersSocketIds)):
                self.gameStarted = True
                self.socketio.emit('game started', room=self.gameId)
                self.socketio.emit('message', 'Game has started', room=self.gameId, namespace='/shrinkChess')
                self.socketio.emit('turnUpdate', self.curPlayer+1, room=self.gameId, namespace='/shrinkChess')

    def sendMoves(self, playerId, move):
        self.socketio.emit('gameUpdateEvent', self.game.getBoardState() , room=self.gameId, namespace='/shrinkChess')
        self.socketio.emit('turnUpdate', self.curPlayer+1, room=self.gameId, namespace='/shrinkChess')

    def recieveMoves(self, socketId, move):
        playerId = self.getPlayerIndex(socketId)
        if(self.gameStarted and playerId == self.curPlayer):
            if(self.game.playMove(move[0], move[1])):
                self.curPlayer = (self.curPlayer + 1) % self.maxPlayers
                self.sendMoves(playerId, move)

    def getPlayerIndex(self, socketId):
        index = -1

        try:
            index = self.playersSocketIds.index(socketId)
        except(ValueError):
            pass

        return index
