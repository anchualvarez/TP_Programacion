import matplotlib
matplotlib.use('TkAgg')  # Cambiar el backend a uno no interactivo

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Histograma
def generar_his():
    try:
        # Cargar datos
        df = pd.read_csv('autos.csv') 
        
        # Crear histograma y mostrarlo
        plt.figure(figsize=(8, 6))
        sns.histplot(df['precio_usd'], bins=15, kde=True, color="red")
        plt.title('Distribución de Precios de Autos')
        plt.xlabel('Precio en USD')
        plt.ylabel('Frecuencia')
        
        print("Generando gráfico...")
        
        plt.show()
        
    except FileNotFoundError:
        print("Error: El archivo 'autos.csv' no fue encontrado.")
    except pd.errors.EmptyDataError:
        print("Error: El archivo 'autos.csv' está vacío.")
    except Exception as e:
        print(f"Se ha producido un error inesperado: {e}")

def generar_bar():
    try:
        df = pd.read_csv('autos.csv')
        df['marca_modelo'] = df['marca'] + ' ' + df['modelo']
        
        # Ordenar los autos por precio y tomar los 10 más caros
        top_autos = df.sort_values(by='precio_usd', ascending=False).head(10)
        
        plt.figure(figsize=(10, 6))
        palette = sns.color_palette("pastel", n_colors=len(top_autos))
        
        # Usar hue para aplicar los colores pastel a las barras
        ax = sns.barplot(data=top_autos, x='marca_modelo', y='precio_usd', palette=palette, hue='marca_modelo', legend=False)
        
        for p in ax.patches:
            ax.text(p.get_x() + p.get_width() / 2,  # Coordenada x (centro de la barra)
                    p.get_height() + 1000,          # Coordenada y (encima de la barra, ajusta según sea necesario)
                    f'${p.get_height():.0f}',     # Valor precio
                    ha='center', va='bottom', fontsize=10)
        
        # Personalizar el gráfico
        plt.title('Top 10 Autos por Precio')
        plt.xlabel('Marca y Modelo del Auto')
        plt.ylabel('Precio en USD')
        plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mayor legibilidad
        
        print("Generando gráfico...")

        plt.show()
    
    except FileNotFoundError:
        print("Error: El archivo 'autos.csv' no fue encontrado.")
    except pd.errors.EmptyDataError:
        print("Error: El archivo 'autos.csv' está vacío.")
    except Exception as e:
        print(f"Se ha producido un error inesperado: {e}")
