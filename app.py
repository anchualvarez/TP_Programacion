from flask import Flask, jsonify, request
import sqlite3
import requests

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

class Cliente:
    def __init__(self, id, nombre, edad):
        self.id = id
        self.nombre = nombre
        self.edad = edad

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}', edad={self.edad})"


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
    
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    
    marca = data.get("marca")
    modelo = data.get("modelo")
    año_creacion = data.get("año_creacion")
    precio_usd = data.get("precio_usd")
    condicion = data.get("condicion")

    # Validar que todos los campos necesarios estén presentes
    if not all([marca, modelo, año_creacion, precio_usd, condicion]):
        return jsonify({"error": "Faltan datos necesarios"}), 400

    # Validar tipos de datos
    try:
        año_creacion = int(año_creacion)
    except ValueError:
        return jsonify({"error": "El año de creación debe ser un número entero válido"}), 400

    try:
        precio_usd = float(precio_usd)
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400

    try:
        with connect_to_database() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO autos (marca, modelo, año_creacion, precio_usd, condicion) 
                VALUES (?, ?, ?, ?, ?)
            """, (marca, modelo, año_creacion, precio_usd, condicion))
            conn.commit()
            auto_id = cursor.lastrowid

        return jsonify({"message": f"El auto ({marca}, {modelo}) fue agregado con éxito", "id": auto_id}), 201

    except sqlite3.Error as e:
        return jsonify({"error": f"Error al agregar auto: {e}"}), 500


# Endpoint para ver el precio en pesos de un auto específico
@app.route("/precio_pesos/<int:auto_id>", methods=["GET"])
def precio_pesos(auto_id):
    try:
        # Obtener el precio del auto en USD
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM autos WHERE id = ?", [auto_id])
        auto = cursor.fetchone()
        conn.close()
        
        if auto is None:
            return jsonify ({"error": "Auto no encontrado"})
        
        marca, modelo, precio_usd = auto [1],auto [2],auto [4]

        # Obtener tipo de cambio de la API de BlueLytics
        response = requests.get("https://api.bluelytics.com.ar/v2/latest")
        tipo_cambio = response.json()["blue"]["value_avg"]

        # Calcular precio en pesos
        precio_en_pesos = precio_usd * tipo_cambio
        
        return jsonify ({
            "marca": marca,
            "modelo": modelo,
            "precio_usd": precio_usd,
            "precio_pesos": round(precio_en_pesos, 2)
        }), 200            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para actualizar un auto existente 
@app.route("/autos/<int:auto_id>", methods=["PUT"])
def update_auto(auto_id):
    data = request.get_json()
    precio_usd = data.get("precio_usd")

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("UPDATE autos SET precio_usd = ? WHERE id = ?",
                   (precio_usd, auto_id))
    conn.commit()
    cursor.execute("SELECT * FROM autos WHERE id = ?", (auto_id,))
    auto_actualizado = cursor.fetchone()
    conn.close()
    
    if auto_actualizado is None:
        return jsonify ({"error": "Auto no encontrado"}), 404

    auto_data = {
        "id": auto_actualizado[0],
        "marca": auto_actualizado[1],
        "modelo": auto_actualizado[2],
        "año_creacion": auto_actualizado[3],
        "precio_usd": auto_actualizado[4],
        "condicion": auto_actualizado[5],
    }
    
    return jsonify(auto_data), 200

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

# Endpoint para ver todos los clientes

@app.route("/clientes", methods=["GET"])
def get_clientes():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes_data = cursor.fetchall()
    conn.close()

    # Crear una lista de instancias de Cliente
    clientes = [Cliente(cliente[0], cliente[1], cliente[2]) for cliente in clientes_data]
    
    # Devolver la lista de clientes
    return jsonify([{"id": cliente.id, "nombre": cliente.nombre, "edad": cliente.edad} for cliente in clientes]), 200


# Registrar un nuevo cliente
@app.route("/clientes", methods=["POST"])
def add_cliente():
    data = request.get_json()
    nombre = data.get("nombre")
    edad = data.get("edad")
    
    if not nombre or not edad:
        return jsonify ({"error": "Faltan dtos necesarios"}), 400

    try:
        edad = int(edad)  # Asegúrate de convertir la edad a un entero
    except ValueError:
        return jsonify({"error": "La edad debe ser un número válido"}), 400

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conn.commit()
    cliente_id = cursor.lastrowid
    conn.close()
    
    nuevo_cliente = Cliente (cliente_id, nombre, edad)  # Crear una instancia de Cliente
    return jsonify({"id": nuevo_cliente.id, "nombre": nuevo_cliente.nombre, "edad": nuevo_cliente.edad}), 201

    #return jsonify({"message": "Cliente registrado con éxito"}), 201

# Obtener información de un cliente específico
@app.route("/clientes/<int:cliente_id>", methods=["GET"])
def get_cliente(cliente_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente_data = cursor.fetchone()
    conn.close()

    if cliente_data:
        cliente = Cliente(cliente_data[0], cliente_data[1], cliente_data[2])  # Crear una instancia de Cliente
        return jsonify({"id": cliente.id, "nombre": cliente.nombre, "edad": cliente.edad}), 200
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
