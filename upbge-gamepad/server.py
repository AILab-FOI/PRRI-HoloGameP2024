import bge
import flask
from flask import Flask, render_template, send_from_directory, request, abort
from flask_socketio import SocketIO, emit
import json
import threading

ADDR_OUT = '0.0.0.0'
PORT = 5000

app = Flask(__name__)
app.config[ 'SECRET_KEY' ] = 'šekret'
socketio = SocketIO( app, cors_allowed_origins="*" )

# A set to keep track of connected clients
connected_clients = set()

PLAYERS = 0

SCENE = bge.logic.getCurrentScene()
OWN = SCENE.objects['Cube']

@socketio.on( 'connect' )
def connect():
    print( 'Client connected:', request.sid )
    connected_clients.add( request.sid )
    global PLAYERS
    PLAYERS += 1


@socketio.on( 'disconnect' )
def disconnect():
    print( 'Client disconnected:', request.sid )
    connected_clients.remove( request.sid )
    global PLAYERS
    PLAYERS -= 1
    
@socketio.on( 'ctrl' )
def handle_message( message ):
    try:
        msg = json.loads( message[ 'data' ] )
    except Exception as e:
        print( "Error while loading message:", message )
        emit( 'error', { "message": "Your browser sent an unparsable message." }, broadcast=True )
        return
    cmd = msg[ "cmd" ]
    if cmd == "RIGHT":
        OWN.worldPosition.x += 0.1
    if cmd == "LEFT":
        OWN.worldPosition.x -= 0.1
    if cmd == "UP":
        OWN.worldPosition.y += 0.1
    if cmd == "DOWN":
        OWN.worldPosition.y -= 0.1
    
# Route for serving the controller
@app.route( '/' )
def ctrl():
    return render_template( 'ctrl.html', game='abe' )


# Routes for serving static files
@app.route( '/images/<path:path>' )
def serve_images( path ):
    return send_from_directory( 'images', path )

@app.route( '/js/<path:path>' )
def serve_js( path ):
    return send_from_directory( 'js', path )

    
import signal
import os

@app.route('/shutdown')
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'


print( 'Starting server ...' )

def start_server():
    socketio.run( app, host='0.0.0.0', port=5000 )
    
    
thread = threading.Thread( target=start_server )
thread.start()

