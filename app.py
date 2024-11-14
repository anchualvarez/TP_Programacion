from flask import Flask, jsonify, request
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
DATABASE = 'autos.db'

# Función para conectar a la base de datos
def connect_to_database():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as error_conexion:
        print(f"Error al conectar a la base de datos '{DATABASE}': {error_conexion}")
        return None

# id, marca, modelo, año_creacion, precio_usd, condicion

@app.route("/")
def hello():
    return "Hola, bienvenido a la API de autos y clientes."

# Endpoint para ver todos los autos
@app.route("/autos", methods=["GET"])
def get_autos():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM autos")
    autos = cursor.fetchall()
    conn.close()

#    clean_autos = [
#       {"id": auto[0], "marca": auto[1], "modelo": auto[2], "año_creacion": auto[3], "precio_usd": auto[4], "condicion": auto[5]}
#        for auto in autos
#    ]
 
    clean_autos = []
    for auto in autos:
        clean_autos.append({
            "id": auto[0],
            "marca": auto[1],
            "modelo": auto[2],
            "año_creacion": auto[3],
            "precio_usd": auto[4],
            "condicion": auto[5],
        })
    
    return jsonify(clean_autos), 200

# Endpoint para agregar un auto nuevo
@app.route("/add_autos", methods=["POST"])
def add_auto():
    data = request.get_json()
    
    print(data)  # Imprime los datos recibidos
    
    if not data:
        return jsonify ({"Error": "No se recibieron datos"}), 400
    
    id = data.get("id") #?
    marca = data.get("marca")
    modelo = data.get("modelo")
    año_creacion = data.get("año_creacion")
    precio_usd = data.get("precio_usd")
    condicion = data.get("condicion")

    if not (id and marca and modelo and año_creacion and precio_usd and condicion):
        return jsonify({"Error": "Faltan datos necesarios"}), 400

    try:
        precio_usd = float(precio_usd)
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400

    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO autos (id, marca, modelo, año_creacion, precio_usd, condicion) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id, marca, modelo, año_creacion, precio_usd, condicion))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        return jsonify({"message": "Auto agregado con éxito"}), 201
    except sqlite3.Error as e:
        # En caso de error en la consulta
        conn.close()
        return jsonify({"error": f"Error al agregar auto: {e}"}), 500
    
#    cursor.execute("INSERT INTO autos (id, marca, modelo, año_creacion, precio_usd, condicion) VALUES (?, ?, ?, ?, ?, ?)",
#                   (id, marca, modelo, año_creacion, precio_usd, condicion))
#    conn.commit()
#    conn.close()

#    return jsonify({"message": "Auto agregado con éxito"}), 201

# Endpoint para ver el precio en pesos de un auto específico
@app.route("/precio_pesos/<int:auto_id>", methods=["GET"])
def precio_pesos(auto_id):
    try:
        # Obtener el precio del auto en USD
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT precio_usd FROM autos WHERE id = ?", [auto_id])
        precio_usd = cursor.fetchone()[0]
        conn.close()

        # Obtener tipo de cambio de la API de BlueLytics
        response = requests.get("https://api.bluelytics.com.ar/v2/latest")
        tipo_cambio = response.json()["blue"]["value_avg"]

        # Calcular precio en pesos
        precio_en_pesos = precio_usd * tipo_cambio
        return jsonify({"precio_en_pesos": precio_en_pesos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para actualizar un auto existente
@app.route("/autos/<int:auto_id>", methods=["PUT"])
def update_auto(auto_id):
    data = request.get_json()
    marca = data.get("marca")
    modelo = data.get("modelo")
    año_creacion = data.get("año_creacion")
    precio_usd = data.get("precio_usd")
    condicion = data.get("condicion")

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("UPDATE autos SET marca = ?, modelo = ?, año_creacion = ?, precio_usd = ?, condicion = ? WHERE id = ?",
                   (marca, modelo, año_creacion, precio_usd, condicion, auto_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Auto actualizado con éxito"}), 200

# Endpoint para eliminar un auto
@app.route("/autos/<int:auto_id>", methods=["DELETE"])
def delete_auto(auto_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM autos WHERE id = ?", (auto_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Auto eliminado con éxito"}), 200

# Endpoints para clientes

# Registrar un nuevo cliente
@app.route("/clientes", methods=["POST"])
def add_cliente():
    data = request.get_json()
    nombre = data.get("nombre")
    edad = data.get("edad")

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conn.commit()
    conn.close()
    return jsonify({"message": "Cliente registrado con éxito"}), 201

# Obtener información de un cliente específico
@app.route("/clientes/<int:cliente_id>", methods=["GET"])
def get_cliente(cliente_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        cliente_data = {"id": cliente[0], "nombre": cliente[1], "edad": cliente[2]}
        return jsonify(cliente_data), 200
    else:
        return jsonify({"error": "Cliente no encontrado"}), 404


@app.route("/clientes/ultimos_autos", methods=["GET"])
def get_ultimos_autos_vistos(): # cliente_id 
    conn = connect_to_database()
    cursor = conn.cursor()

    # Consulta para obtener los últimos 5 autos añadidos a la base de datos
    cursor.execute("SELECT * FROM autos ORDER BY id DESC LIMIT 5") # WHERE id = ?", (cliente_id,)
    autos = cursor.fetchall()
    conn.close()

    # Formateamos los resultados en un diccionario
    ultimos_autos = [
        {
            "id": auto[0], 
            "marca": auto[1], 
            "modelo": auto[2], 
            "año_creacion": auto[3], 
            "precio_usd": auto[4], 
            "condicion": auto[5]
        }
        for auto in autos
    ]
    
    # Devolvemos los últimos autos vistos como respuesta JSON
    return jsonify({"ultimos_autos_ingresados": ultimos_autos}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)


