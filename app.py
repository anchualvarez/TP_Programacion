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
    
#    print(data)  # Imprime los datos recibidos
    
    if not data:
        return jsonify ({"Error": "No se recibieron datos"}), 400
    
#    id = data.get("id") 
    marca = data.get("marca")
    modelo = data.get("modelo")
    año_creacion = data.get("año_creacion")
    precio_usd = data.get("precio_usd")
    condicion = data.get("condicion")

    if not (marca and modelo and año_creacion and precio_usd and condicion):
        return jsonify({"Error": "Faltan datos necesarios"}), 400

    try:
        precio_usd = float(precio_usd)
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400

    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO autos (marca, modelo, año_creacion, precio_usd, condicion) 
            VALUES (?, ?, ?, ?, ?)
        """, (marca, modelo, año_creacion, precio_usd, condicion))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        return jsonify({"message": "Auto agregado con éxito"}), 201
    except sqlite3.Error as e:
        # En caso de error en la consulta
        conn.close()
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
        
        id, marca, modelo, año_creacion, precio_usd, condicion = auto

        # Obtener tipo de cambio de la API de BlueLytics
        response = requests.get("https://api.bluelytics.com.ar/v2/latest")
        tipo_cambio = response.json()["blue"]["value_avg"]

        # Calcular precio en pesos
        precio_en_pesos = precio_usd * tipo_cambio
        
        auto_con_precio = {
            "id": id,
            "marca": marca,
            "modelo": modelo,
            "año_creacion": año_creacion,
            "precio_usd": precio_usd,
            "precio_pesos": round (precio_en_pesos, 2),
            "condicion": condicion
            }
        return jsonify(auto_con_precio), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para actualizar un auto existente --> ERRORES
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
    clientes = cursor.fetchall()
    conn.close()

    clean_clientes = []
    for cliente in clientes:
        clean_clientes.append({
            "id": cliente[0],
            "nombre": cliente[1],
            "edad": cliente[2],
            })
        
    return jsonify(clean_clientes), 200


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

