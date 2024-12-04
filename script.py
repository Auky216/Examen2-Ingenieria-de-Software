import sqlite3
import os
from datetime import datetime

db_path = "C:/Users/adria/OneDrive/Escritorio/Examen2-Ingenieria-de-Software/database.db"

if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

try:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    schema = """
    CREATE TABLE IF NOT EXISTS Usuario (
        alias TEXT PRIMARY KEY,
        nombre TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Contacto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        contacto TEXT NOT NULL,
        fechaRegistro DATETIME NOT NULL,
        FOREIGN KEY (usuario) REFERENCES Usuario(alias) ON DELETE CASCADE,
        FOREIGN KEY (contacto) REFERENCES Usuario(alias) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Mensaje (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remitente TEXT NOT NULL,
        destinatario TEXT NOT NULL,
        contenido TEXT NOT NULL,
        fechaEnvio DATETIME NOT NULL,
        FOREIGN KEY (remitente) REFERENCES Usuario(alias) ON DELETE CASCADE,
        FOREIGN KEY (destinatario) REFERENCES Usuario(alias) ON DELETE CASCADE
    );
    """
    cursor.executescript(schema)

    users = [
        ("cpaz", "Christian"),
        ("lmunoz", "Luisa"),
        ("mgrau", "Miguel")
    ]
    contacts = [
        ("cpaz", "lmunoz"),
        ("cpaz", "mgrau"),
        ("lmunoz", "mgrau"),
        ("mgrau", "cpaz")
    ]

    cursor.executemany("INSERT OR IGNORE INTO Usuario (alias, nombre) VALUES (?, ?)", users)

    for usuario, contacto in contacts:
        cursor.execute(
            "INSERT OR IGNORE INTO Contacto (usuario, contacto, fechaRegistro) VALUES (?, ?, ?)",
            (usuario, contacto, datetime.now())
        )

    connection.commit()
    connection.close()

    print("Base de datos inicializada con datos predeterminados.")
except sqlite3.Error as e:
    print(f"Error al inicializar la base de datos: {e}")
