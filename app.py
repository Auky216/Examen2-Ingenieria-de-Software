from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_path = "C:/Users/adria/OneDrive/Escritorio/Examen2-Ingenieria-de-Software/database.db"

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/mensajeria/contactos', methods=['GET'])
def get_contactos():
    alias = request.args.get('mialias')
    if not alias:
        return jsonify({"error": "Falta el parámetro 'mialias'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.alias, u.nombre FROM Usuario u
        INNER JOIN Contacto c ON u.alias = c.contacto
        WHERE c.usuario = ?
    """, (alias,))
    contactos = cursor.fetchall()
    conn.close()

    result = {contacto['alias']: contacto['nombre'] for contacto in contactos}
    return jsonify(result)

@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def agregar_contacto(alias):
    data = request.get_json()
    if 'contacto' not in data:
        return jsonify({"error": "Falta el parámetro 'contacto'"}), 400
    
    contacto = data['contacto']
    nombre = data.get('nombre')  
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT alias FROM Usuario WHERE alias = ?", (contacto,))
    contacto_exists = cursor.fetchone()
    
    if not contacto_exists:
        if not nombre:
            return jsonify({"error": "Falta el nombre del nuevo usuario"}), 400
        cursor.execute("INSERT INTO Usuario (alias, nombre) VALUES (?, ?)", (contacto, nombre))
        conn.commit()

    cursor.execute("""
        INSERT OR IGNORE INTO Contacto (usuario, contacto, fechaRegistro)
        VALUES (?, ?, ?)
    """, (alias, contacto, datetime.now()))
    cursor.execute("""
        INSERT OR IGNORE INTO Contacto (usuario, contacto, fechaRegistro)
        VALUES (?, ?, ?)
    """, (contacto, alias, datetime.now()))
    conn.commit()
    conn.close()

    return jsonify({"message": "Contacto añadido correctamente"})

@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    if 'usuario' not in data or 'contacto' not in data or 'mensaje' not in data:
        return jsonify({"error": "Faltan parámetros"}), 400

    usuario = data['usuario']
    contacto = data['contacto']
    mensaje = data['mensaje']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT alias FROM Usuario WHERE alias = ?", (usuario,))
    usuario_exists = cursor.fetchone()

    cursor.execute("SELECT alias FROM Usuario WHERE alias = ?", (contacto,))
    contacto_exists = cursor.fetchone()

    if not usuario_exists or not contacto_exists:
        return jsonify({"error": "Uno o ambos usuarios no existen"}), 400

    cursor.execute("""
        INSERT INTO Mensaje (remitente, destinatario, contenido, fechaEnvio)
        VALUES (?, ?, ?, ?)
    """, (usuario, contacto, mensaje, datetime.now()))
    conn.commit()
    conn.close()

    return jsonify({"message": "Mensaje enviado correctamente"})

@app.route('/mensajeria/recibidos', methods=['GET'])
def obtener_mensajes_recibidos():
    alias = request.args.get('mialias')
    if not alias:
        return jsonify({"error": "Falta el parámetro 'mialias'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.remitente, m.contenido, m.fechaEnvio 
        FROM Mensaje m
        WHERE m.destinatario = ?
        ORDER BY m.fechaEnvio DESC
    """, (alias,))
    mensajes = cursor.fetchall()
    conn.close()

    result = [
        {
            "remitente": mensaje['remitente'],
            "mensaje": mensaje['contenido'],
            "fecha": mensaje['fechaEnvio']
        } for mensaje in mensajes
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
