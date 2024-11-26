import matplotlib
matplotlib.use('TkAgg')  # Cambiar el backend a uno no interactivo

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# F Histograma
def generar_his():
    # cargar datos
    df = pd.read_csv('autos.csv') 
    
    # crea histo y lo muestra
    plt.figure(figsize=(8, 6))
    sns.histplot(df['precio_usd'], bins=15, kde=True, color="red")
    plt.title('Distribución de Precios de Autos')
    plt.xlabel('Precio en USD')
    plt.ylabel('Frecuencia')
    plt.show()


def generar_bar():
    # Cargar datos
    df = pd.read_csv('autos.csv')
    
    # Crear una nueva columna combinando marca y modelo
    df['marca_modelo'] = df['marca'] + ' ' + df['modelo']
    
    # Ordenar los autos por precio y tomar los 10 más caros
    top_autos = df.sort_values(by='precio_usd', ascending=False).head(10)
    
    # Crear y mostrar el gráfico de barras
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=top_autos, x='marca_modelo', y='precio_usd', palette="pastel")
    
    # Agregar etiquetas encima de las barras (sin decimales)
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
    
    # Mostrar el gráfico
    plt.show()
