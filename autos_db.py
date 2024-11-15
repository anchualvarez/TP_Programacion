import sqlite3

DATABASE = 'autos.db'

# Función para crear la tabla de autos
def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Crear tabla de autos con las columnas solicitadas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            año_creacion INTEGER NOT NULL,
            precio_usd INTEGER NOT NULL,
            condicion TEXT CHECK(condicion IN ('Nuevo', 'Usado')) NOT NULL
        )
    ''')
    
    # Crear tabla de clientes con columnas para registrar nombre y edad
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')

    conn.commit()
    print("Tablas 'autos' y 'clientes' creadas con éxito en la base de datos.")
    conn.commit()
    conn.close()


# Función para insertar un auto en la base de datos
def insert_car(marca, modelo, año_creacion, precio_usd, condicion):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO autos (marca, modelo, año_creacion, precio_usd, condicion)
    VALUES (?, ?, ?, ?, ?)
    ''', (marca, modelo, año_creacion, precio_usd, condicion))

    conn.commit()
    conn.close()

# Datos de 30 autos con precios realistas y condición (Nuevo / Usado)
cars_data = [
    ('Toyota', 'Corolla', 2024, 25000, 'Nuevo'),
    ('Honda', 'Civic', 2023, 24000, 'Nuevo'),
    ('Ford', 'Focus', 2022, 22000, 'Nuevo'),
    ('Chevrolet', 'Malibu', 2021, 21000, 'Usado'),
    ('BMW', 'X5', 2023, 55000, 'Nuevo'),
    ('Audi', 'A4', 2020, 35000, 'Usado'),
    ('Volkswagen', 'Golf', 2021, 28000, 'Usado'),
    ('Hyundai', 'Elantra', 2022, 19000, 'Nuevo'),
    ('Kia', 'Forte', 2022, 21000, 'Nuevo'),
    ('Mercedes-Benz', 'C-Class', 2023, 45000, 'Nuevo'),
    ('Nissan', 'Altima', 2020, 24000, 'Usado'),
    ('Subaru', 'Outback', 2022, 35000, 'Nuevo'),
    ('Mazda', 'CX-5', 2021, 30000, 'Usado'),
    ('Chevrolet', 'Impala', 2019, 22000, 'Usado'),
    ('Honda', 'Accord', 2023, 27000, 'Nuevo'),
    ('Toyota', 'Camry', 2021, 28000, 'Usado'),
    ('BMW', '3 Series', 2022, 40000, 'Nuevo'),
    ('Audi', 'Q5', 2023, 55000, 'Nuevo'),
    ('Ford', 'Mustang', 2022, 35000, 'Nuevo'),
    ('Chrysler', 'Pacifica', 2020, 37000, 'Usado'),
    ('Ram', '1500', 2023, 45000, 'Nuevo'),
    ('Jeep', 'Grand Cherokee', 2021, 42000, 'Usado'),
    ('GMC', 'Sierra', 2022, 46000, 'Nuevo'),
    ('Lexus', 'RX', 2023, 50000, 'Nuevo'),
    ('Toyota', 'Highlander', 2020, 39000, 'Usado'),
    ('Honda', 'Pilot', 2022, 45000, 'Nuevo'),
    ('Ford', 'Expedition', 2021, 48000, 'Usado'),
    ('BMW', 'X3', 2020, 42000, 'Usado'),
    ('Hyundai', 'Santa Fe', 2021, 33000, 'Usado'),
    ('Kia', 'Sorento', 2023, 35000, 'Nuevo')
]


# Insertar cada auto en la base de datos
def insert_multiple_cars():
    for car in cars_data:
        insert_car(*car)
    print ("Autos ejempos insertados con exito")

# Crear las tablas si no existen
if __name__ == "__main__":
    create_tables()

# Insertar los autos en la base de datos
insert_multiple_cars()

