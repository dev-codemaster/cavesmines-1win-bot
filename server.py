import os
import sys
import time
import hashlib
import threading
from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO, emit
import eventlet
import numpy as np
from predictor import predict_stars

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cavesmines-1win-public')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Game state global
game_state = {
    'balance': 1000.50, 'current_bet': 10.00, 'game_id': '', 
    'grid': [[False]*5 for _ in range(5)], 'history': [], 
    'confidence': 0.0, 'status': 'waiting'
}

def game_monitor():
    while True:
        try:
            new_game_id = f"1win_{int(time.time()*1000)}"
            if new_game_id != game_state['game_id']:
                game_state['game_id'] = new_game_id
                stars, conf = predict_stars(new_game_id)
                game_state.update({'grid': stars, 'confidence': conf, 'status': 'ready'})
                socketio.emit('new_game', game_state)
            time.sleep(3)
        except: time.sleep(10)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/bet', methods=['POST'])
def place_bet():
    data = request.get_json()
    game_state['current_bet'] = float(data.get('amount', 10))
    socketio.emit('bet_placed', {'amount': game_state['current_bet']})
    return jsonify({'success': True})

@app.route('/api/cashout')
def cashout():
    profit = game_state['current_bet'] * 2.1
    game_state['balance'] += profit
    game_state['history'].append({'id': game_state['game_id'], 'profit': profit})
    socketio.emit('cashout', game_state)
    return jsonify(game_state)

@socketio.on('connect')
def connect(): emit('init', game_state)

@socketio.on('click_cell')
def click_cell(data):
    r, c = data['row'], data['col']
    if game_state['grid'][r][c]:
        emit('cell_safe', {'row': r, 'col': c})
    else:
        emit('game_over', {'row': r, 'col': c})
        game_state['status'] = 'game_over'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    threading.Thread(target=game_monitor, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=port)
