from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'usuarios.json'

def cargar_usuarios():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def guardar_usuarios(usuarios):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(usuarios, file, indent=4, ensure_ascii=False)

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.json
    usuarios = cargar_usuarios()
    if any(u['email'] == datos['email'] for u in usuarios):
        return jsonify({'error': 'Ese correo ya está registrado.'}), 400
    usuarios.append(datos)
    guardar_usuarios(usuarios)
    return jsonify({'mensaje': 'Usuario registrado exitosamente.'}), 201

@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u['email'] == datos['email'] and u['pass'] == datos['pass']), None)
    if usuario:
        return jsonify({'mensaje': 'Login exitoso', 'usuario': usuario}), 200
    return jsonify({'error': 'Correo o contraseña incorrectos.'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)