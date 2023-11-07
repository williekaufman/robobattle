#!/usr/bin/python3

from flask import Flask, jsonify, request, make_response, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS, cross_origin
from secrets import compare_digest, token_hex
from redis_utils import redis, rget_json, rset_json, rset, rget, recurse_to_json
from board import Board
from square import Square, Direction
from state import GameInfo, State
from enemy import get_enemy, all_enemies
import random
import traceback
from functools import wraps

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# decorator that takes in an api endpoint and calls recurse_to_json on its result
def api_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(traceback.print_exc())
            return jsonify({"error": "Unexpected error"}), 500
    return wrapper


def success(data):
    return jsonify({'success': True, **data})


def failure(data):
    return jsonify({'success': False, **data})


def new_game_id():
    return token_hex(16)

@app.route('/new_game', methods=['POST'])
@api_endpoint
def new_game():
    game_id = new_game_id()
    state = State(
        GameInfo(game_id, 1),
        Board(),
    )
    state.write()
    return jsonify({'gameId': game_id})

