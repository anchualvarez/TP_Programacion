import requests
import json

base_url = "http://127.0.0.1:5000"

# Función para registrar un cliente nuevo
def registrar_cliente():
    nombre = input("Ingrese su nombre para registrarse: ")
    data = {"nombre": nombre}
    response = requests.post(f"{base_url}/clientes", json=data)
    print(response.json())

# Función para consultar información de un cliente específico
def ver_cliente():
    cliente_id = int(input("Ingrese el ID del cliente que desea consultar: "))
    response = requests.get(f"{base_url}/clientes/{cliente_id}")
    if response.status_code == 200:
        print("Información del cliente:", response.json())
    else:
        print("Error:", response.json().get("error", "Cliente no encontrado"))

# Función para ver todos los autos disponibles
def ver_autos():
    response = requests.get(f"{base_url}/autos")
    autos = response.json()
    """print("\nAutos disponibles:")
    for auto in autos:
        print(auto)
     """

    print("\nAutos disponibles:")
    for auto in autos:
        print(json.dumps(auto, indent=4))

# Función para agregar un auto nuevo
def agregar_auto():
    marca = input("Marca del auto: ")
    modelo = input("Modelo del auto: ")
    año_creacion = int(input("Año de creación: "))
    precio_usd = float(input("Precio en USD (con decimal): "))
    condicion = input("Condición (Nuevo/Usado): ")
    
    data = {
        "marca": marca,
        "modelo": modelo,
        "año_creacion": año_creacion,
        "precio_usd": precio_usd,
        "condicion": condicion
    }
    response = requests.post(f"{base_url}/add_autos", json=data)
#    print(response.json())

    # Verificar el código de estado de la respuesta
    print(f"Código de estado: {response.status_code}")
    
    # Si la respuesta no es 200, mostramos el contenido de la respuesta
    if response.status_code == 200:
        try:
            print(response.json())  # Intentamos leer el JSON
        except ValueError:
            print("La respuesta no es un JSON válido:", response.text)
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")


# Función para ver el precio en pesos de un auto específico PREGUNTAR COMO PONER DOLARES TB
def ver_precio_en_pesos():
    auto_id = int(input("Ingrese el ID del auto para ver el precio en pesos: "))
    response = requests.get(f"{base_url}/precio_pesos/{auto_id}")
    if response.status_code == 200:
        print("Precio en pesos:", response.json())
    else:
        print("Error:", response.json().get("error", "Auto no encontrado"))

# Función para ver los últimos 5 autos ingresados
def ver_ultimos_autos():
    response = requests.get(f"{base_url}/clientes/ultimos_autos")
    if response.status_code == 200:
        print("Últimos 5 autos ingresados:", response.json()["ultimos_autos_ingresados"])
    else:
        print("Error:", response.json().get("error", "No encontrados"))
    
# Funcion para eliminar un auto segun su id
def eliminar_auto():
    auto_id = input("Ingresa el ID del auto que deseas eliminar: ")
    
    try:
        auto_id = int(auto_id)  # Convertir el ID a un entero
        # Solicitar la eliminación del auto a la API
        response = requests.delete(f"{base_url}/autos/{auto_id}")
        
        if response.status_code == 200:
            print(f"Auto con ID {auto_id} eliminado con éxito.")
        else:
            print(f"Error al eliminar el auto: {response.json().get('Error', 'No eliminado')}")
    
    except ValueError:
        print("Por favor ingresa un ID válido.")

# Menú principal de la aplicación
def main():
    while True:
        print("\n--- Menú de Opciones ---")
        print("1: Registrar cliente")
        print("2: Ver información de un cliente")
        print("3: Ver autos disponibles")
        print("4: Agregar un auto nuevo")
        print("5: Ver precio en pesos de un auto")
        print("6: Ver últimos autos ingresados")
        print("7: Eliminar un auto")
        print("8: Salir")

        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            ver_cliente()
        elif opcion == "3":
            ver_autos()
        elif opcion == "4":
            agregar_auto()
        elif opcion == "5":
            ver_precio_en_pesos()
        elif opcion == "6":
            ver_ultimos_autos()
        elif opcion == "7":
            eliminar_auto()
        elif opcion == "8":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()