import requests
import json

base_url = "http://127.0.0.1:5000"

# Función para registrar un cliente nuevo
def registrar_cliente():
    nombre = input("Ingrese su nombre para registrarse: ")
    edad = input("Ingrese su edad: ")
    data = {"nombre": nombre, "edad": edad}
    
    try:
        response = requests.post(f"{base_url}/clientes", json=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar el cliente: {e}")

# Función para consultar información de un cliente específico
def ver_cliente():
    cliente_id = int(input("Ingrese el ID del cliente que desea consultar: "))
    response = requests.get(f"{base_url}/clientes/{cliente_id}")
    if response.status_code == 200:
        print("Información del cliente:", response.json())
    else:
        print("Error:", response.json().get("error", "Cliente no encontrado"))
        
# Función para ver todos los clientes
def ver_clientes():
    response = requests.get(f"{base_url}/clientes")
    clientes = response.json()
    
    print("\nClientes disponibles:")
    for cliente in clientes:
        print(json.dumps(cliente, indent=4))

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
    precio_usd = int(input("Precio en USD: "))
    condicion = input("Condición (Nuevo/Usado): ")
    
    data = {
        "marca": marca,
        "modelo": modelo,
        "año_creacion": año_creacion,
        "precio_usd": precio_usd,
        "condicion": condicion
    }
    response = requests.post(f"{base_url}/add_autos", json=data)
    print(response.json())


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
        
# Funcion para actualizar un auto segun su id --> ACA HAY ERRORES
def actualizar_auto():
    auto_id = int (input("Ingresa el ID del auto del que deseas actualizar el precio: "))
    
    try:
        nuevo_precio = int (input("Ingresa el nuevo precio del auto: "))

        # Solicitar la actualización del precio del auto a la API
        response = requests.put(f"{base_url}/autos/{auto_id}", json={"precio_usd": nuevo_precio})
        
        if response.status_code == 200:
            # Obtener los datos actualizados del auto
            auto_actualizado = response.json()
            print("Datos del auto actualizado:")
            print(auto_actualizado)  # Esto mostrará todos los datos del auto, incluyendo el nuevo precio
        else:
            print(f"Error al actualizar el precio del auto: {response.json().get('Error', 'No actualizado')}")
    
    except ValueError:
        print("Por favor ingresa un ID y un precio válidos")


# Menú principal de la aplicación
def main():
    while True:
        print("\n--- Menú de Opciones ---")
        print("1: Registrar cliente")
        print("2: Ver información de un cliente")
        print("3: Ver clientes creados")
        print("4: Ver autos disponibles")
        print("5: Agregar un auto nuevo")
        print("6: Ver precio en pesos de un auto")
        print("7: Ver últimos 5 autos ingresados")
        print("8: Eliminar un auto")
        print("9: Actualizar un auto")
        print("10: Salir")

        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            ver_cliente()
        elif opcion == "3":
            ver_clientes()
        elif opcion == "4": 
            ver_autos()  
        elif opcion == "5":
            agregar_auto() 
        elif opcion == "6":
            ver_precio_en_pesos()
        elif opcion == "7":
            ver_ultimos_autos()
        elif opcion == "8":
            eliminar_auto()
        elif opcion == "9":
            actualizar_auto()
        elif opcion == "10":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
