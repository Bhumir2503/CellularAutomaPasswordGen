from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import random
import string
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, supports_credentials=True)

def generate_password(length, lowercase, uppercase, digits, special):
    charset = ""
    if lowercase:
        charset += string.ascii_lowercase
    if uppercase:
        charset += string.ascii_uppercase
    if digits:
        charset += string.digits
    if special:
        charset += "!@#$%^&*"

    if not charset:
        return ""

    return ''.join(random.choice(charset) for _ in range(length))

def generate_automaton(rule, width, iterations):
    grid = [[0 for _ in range(width)] for _ in range(iterations)]
    grid[0][width // 2] = 1  # Center cell is active

    ruleset = [(rule >> i) & 1 for i in reversed(range(8))]

    for row in range(1, iterations):
        for col in range(width):
            left = grid[row - 1][(col - 1) % width]
            center = grid[row - 1][col]
            right = grid[row - 1][(col + 1) % width]
            idx = (left << 2) | (center << 1) | right
            grid[row][col] = ruleset[idx]

    return grid

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    print("Received data:", data)
    import sys; sys.stdout.flush()

    length = data.get("length", 16)
    lowercase = data.get("lowercase", True)
    uppercase = data.get("uppercase", True)
    digits = data.get("digits", True)
    special = data.get("special", True)
    rule = data.get("rule", 30)
    width = data.get("width", 100)
    iterations = data.get("iterations", 50)
    count = data.get("count", 3)

    passwords = [
        generate_password(length, lowercase, uppercase, digits, special)
        for _ in range(count)
    ]
    grid = generate_automaton(rule, width, iterations)

    response = jsonify({"passwords": passwords, "grid": grid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response

if __name__ == "__main__":
    app.run(debug=True)
