import flask
from flask import Flask, render_template, send_from_directory, request, abort, redirect
from flask_socketio import SocketIO, emit
import json
import threading
import os
import time

import pygetwindow as gw
from screeninfo import get_monitors
import pyautogui
pyautogui.FAILSAFE = False
all_monitors = get_monitors()
primary_monitor = all_monitors[0]
monitor_center_x = primary_monitor.x + primary_monitor.width // 2
monitor_center_y = primary_monitor.y + primary_monitor.height // 2
active_window = gw.getActiveWindow()
print("ACT: ",active_window)

from config import GAMES

GAME = GAMES['covjece']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'šekret'
socketio = SocketIO(app, cors_allowed_origins="*")

PLAYERS = {}
MAX_PLAYERS = 4
GAME_STARTED = False
READY_PLAYERS = 0
COLORS = ['zelena', 'zuta', 'crvena', 'plava']

@socketio.on('connect')
def connect():
    global GAME_STARTED
    if not GAME_STARTED and len(PLAYERS) < MAX_PLAYERS:
        print('Client connected:', request.sid)
        PLAYERS[request.sid] = {"name": "", "ready": False, "color": None}
        assign_color(request.sid)
        emit('update_lobby', PLAYERS, broadcast=True)
    else:
        emit('error', {"message": "Lobby is full or game has already started!"})

@socketio.on('disconnect')
def disconnect():
    global READY_PLAYERS, GAME_STARTED
    if request.sid in PLAYERS:
        print('Client disconnected:', request.sid)
        if PLAYERS[request.sid]['ready']:
            READY_PLAYERS -= 1
        del PLAYERS[request.sid]
        emit('update_lobby', PLAYERS, broadcast=True)

@socketio.on('ctrl')
def handle_message(message):
    global PLAYERS, GAME_STARTED, GAMES

    try:
        msg = json.loads(message['data'])
        #print('Received message data:', msg)
    except Exception as e:
        print("Error while loading message:", message)
        emit('error', {"message": "Your browser sent an unparsable message."}, broadcast=True)
        return

    cmd = msg["cmd"]
    context = msg["context"]
    #print("PLAYERS: ", PLAYERS)
    player = PLAYERS.get(request.sid)
    #print("player: ",player)

    # Set player's name and color in the message
    #msg['playerName'] = player['name']
    playerColor = player['color']
    print('Player', playerColor, 'pressed', cmd)
    emit('assign_color', {"color":playerColor}, broadcast=False)

    active_window = gw.getActiveWindow()
    active_window.activate()
    print("ACT: ",active_window)

    pyautogui.click(monitor_center_x, monitor_center_y)

    active_window = gw.getActiveWindow()
    active_window.activate()
    print("ACT: ",active_window)

    time.sleep(2)

    active_window = gw.getActiveWindow()
    active_window.activate()
    print("ACT: ",active_window)
    
    if cmd=="KOCKA":
        pyautogui.click(monitor_center_x, monitor_center_y)
        active_window.activate()
        pyautogui.keyDown('space')
        print("PRESSED: space")
        active_window = gw.getActiveWindow()
        print("ACT: ",active_window)
        pyautogui.keyUp('space')
        
    elif cmd=="PIJUN1":
        pyautogui.click(monitor_center_x, monitor_center_y)
        active_window.activate()
        pyautogui.keyDown('1')
        print("PRESSED: 1")
        active_window = gw.getActiveWindow()
        print("ACT: ",active_window)
        pyautogui.keyUp('1')

    elif cmd=="PIJUN2":
        pyautogui.click(monitor_center_x, monitor_center_y)
        active_window.activate()
        pyautogui.keyDown('2')
        print("PRESSED: 2")
        active_window = gw.getActiveWindow()
        print("ACT: ",active_window)
        pyautogui.keyUp('2')

    elif cmd=="PIJUN3":
        pyautogui.click(monitor_center_x, monitor_center_y)
        active_window.activate()
        pyautogui.keyDown('3')
        print("PRESSED: 3")
        active_window = gw.getActiveWindow()
        print("ACT: ",active_window)
        pyautogui.keyUp('3')

    elif cmd=="PIJUN4":
        pyautogui.click(monitor_center_x, monitor_center_y)
        active_window.activate()
        pyautogui.keyDown('4')
        print("PRESSED: 4")
        active_window = gw.getActiveWindow()
        print("ACT: ",active_window)
        pyautogui.keyUp('4')

"""
    if cmd in GAME['taps']:
        if context == "start":
            print(f"Player {player['name']} ({player['color']}) tapped {cmd}")

    if cmd in GAME['toggles']:
        if context == "start":
            print(f"Player {player['name']} ({player['color']}) started toggling {cmd}")
        else:
            print(f"Player {player['name']} ({player['color']}) stopped toggling {cmd}")
"""

@socketio.on('set_name')
def set_name(data):
    #print("data: ", data)
    global READY_PLAYERS
    if request.sid in PLAYERS:
        PLAYERS[request.sid]['name'] = data['name']
        #print("PLAYERS: ", PLAYERS)
        assign_color(request.sid)
        emit('update_lobby', PLAYERS, broadcast=True)
        emit('hide_name_input', broadcast=True)

@socketio.on('set_ready')
def set_ready():
    global READY_PLAYERS, GAME_STARTED
    if request.sid in PLAYERS and not PLAYERS[request.sid]['ready']:
        PLAYERS[request.sid]['ready'] = True
        READY_PLAYERS += 1
        emit('update_lobby', PLAYERS, broadcast=True)
        if READY_PLAYERS == MAX_PLAYERS:
            start_game_countdown()

def assign_color(sid):
    global PLAYERS, COLORS
    available_colors = [color for color in COLORS if color not in [player['color'] for player in PLAYERS.values()]]
    if available_colors:
        PLAYERS[sid]['color'] = available_colors[0]

def start_game_countdown():
    global GAME_STARTED
    GAME_STARTED = True
    countdown = 10
    while countdown > 0:
        socketio.emit('countdown', {'seconds': countdown})
        time.sleep(1)
        countdown -= 1
        if countdown == 1:
            socketio.emit('countdown', {'seconds': 1})  # Emit 1 second countdown
    print('Game started!')
    socketio.emit('start_game', namespace='/', include_self=True) # Emit to all connected clients
    READY_PLAYERS = 0

@app.route('/')
def index():
    if GAME_STARTED:
        return redirect('/game')
    else:
        return render_template('index.html', game='covjece')

@app.route('/game')
def game():
    return render_template('ctrl.html', game='covjece')

@app.route('/images/<path:path>')
def serve_images(path):
    return send_from_directory('static/images', path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('static/js', path)

if __name__ == '__main__':
    print('Starting server ...')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
