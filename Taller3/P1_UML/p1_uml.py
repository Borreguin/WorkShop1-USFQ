import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# Carga de datos
url = "https://raw.githubusercontent.com/Borreguin/WorkShop1-USFQ/main/Taller3/P1_UML/data/data.csv"
df = pd.read_csv(url, delimiter=';')
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d.%m.%Y %H:%M')
df['dia'] = df['timestamp'].dt.day
df['nombre_dia'] = df['timestamp'].dt.day_name()

# Función modificada para mostrar heatmap
def mostrar_heatmap(dia, columna):
    if dia != "Todos":
        df_filtrado = df[df['nombre_dia'] == dia]
    else:
        df_filtrado = df
    pivot_table = df_filtrado.pivot_table(values=columna, index=df_filtrado.timestamp.dt.hour, columns='dia', aggfunc='mean')
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_table, cmap='coolwarm', annot=False, fmt=".1f")
    plt.title(f'Heatmap de {columna} {("los " + dia) if dia != "Todos" else "de todos los días"}')
    plt.xlabel('Día del mes')
    plt.ylabel('Hora del día')
    plt.show()
    
    pivot_table2 = df_filtrado.pivot_table(values=columna, index=df_filtrado.timestamp.dt.hour)
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_table2, cmap='coolwarm', annot=True, fmt=".1f")
    plt.title(f'Heatmap de {columna} {("los " + dia) if dia != "Todos" else "de todos los días"}')
    plt.xlabel('Día del mes')
    plt.ylabel('Hora del día')
    plt.show()

# Menú modificado para seleccionar el día de la semana
dias = {
    '1': 'Monday',
    '2': 'Tuesday',
    '3': 'Wednesday',
    '4': 'Thursday',
    '5': 'Friday',
    '6': 'Saturday',
    '7': 'Sunday',
    '8': 'Todos'
}

print("Selecciona el día de la semana o 'Todos' los días:")
print("1: Lunes\n 2: Martes\n 3: Miércoles\n 4: Jueves\n 5: Viernes\n 6: Sábado\n 7: Domingo\n 8: Todos")
opcion = input("Introduce el número de tu opción: ")

dia_seleccionado = dias.get(opcion, 'Todos')  # Default a 'Todos' si la entrada no es válida

# Solicitar al usuario qué variable desea visualizar
opcion = input("Introduce el número correspondiente a la variable que deseas visualizar:\n"
               "1: V005_vent01_CO2\n"
               "2: V022_vent02_CO2\n"
               "3: V006_vent01_temp_out\n"
               "4: V023_vent02_temp_out\n"
               "5: V005_vent01_CO2', 'V022_vent02_CO2\n"
               "6: V006_vent01_temp_out', 'V023_vent02_temp_out\n")


# Asignar la columna según la opción elegida
if opcion == '1':
    columna = 'V005_vent01_CO2'
elif opcion == '2':
    columna = 'V022_vent02_CO2'
elif opcion == '3':
    columna = 'V006_vent01_temp_out'
elif opcion == '4':
    columna = 'V023_vent02_temp_out'
elif opcion == '5':
    columna = ['V005_vent01_CO2', 'V022_vent02_CO2']
elif opcion == '6':
    columna = ['V006_vent01_temp_out', 'V023_vent02_temp_out']
else:
    print("Opción no válida. Mostrando V005_vent01_CO2 por defecto.")
    columna = 'V005_vent01_CO2'

# Mostrar heatmap para la columna seleccionada
mostrar_heatmap(dia_seleccionado, columna)

#--------------------------------------------------------------------------------------------
# Función para plotear gráficos de caja para las variables seleccionadas
def plotear_boxplots_diarios():
    # Filtrar las horas del día para incluir solo de 00:00 a 23:00
    df['hora'] = df['timestamp'].dt.hour
    
    # Lista de las variables a plotear
    variables = ['V005_vent01_CO2', 'V022_vent02_CO2', 'V006_vent01_temp_out', 'V023_vent02_temp_out']
    
    # Configuración del tamaño de la figura
    plt.figure(figsize=(12, 6))
    
    # Loop para plotear cada variable
    for i, var in enumerate(variables, 1):
        plt.subplot(2, 2, i)  # 2 filas, 2 columnas, posición i
        sns.boxplot(x='hora', y=var, data=df)
        plt.title(f'Distribución diaria de {var}')
        plt.ylabel('Valor')
        plt.xlabel('Hora del día')
    
    plt.tight_layout()
    plt.show()

# Llamada a la función para plotear los boxplots
plotear_boxplots_diarios()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Asegúrate de especificar el delimitador correcto
data = df
data = pd.read_csv(url, delimiter=';')

# Imprime los nombres de las columnas para verificarlos
print("Columnas en el dataframe: ", data.columns)

# Asegúrate de que tus datos estén indexados por fecha
data.index = pd.to_datetime(data['timestamp'])
data = data.drop(columns=['timestamp'])

# Reemplaza los valores faltantes con la media de la columna
imputer = SimpleImputer(strategy='mean')
data_imputed = imputer.fit_transform(data)
data = pd.DataFrame(data_imputed, columns=data.columns, index=data.index)

variables = ['V005_vent01_CO2', 'V022_vent02_CO2', 'V006_vent01_temp_out', 'V023_vent02_temp_out']

for var in variables:
    # Verifica si la variable está en el dataframe antes de trazarla
    if var in data.columns:
        plt.figure(figsize=(12,6))
        for day in data.index.day.unique():
            # Filtra los datos para cada día y traza la variable
            data_day = data[data.index.day == day]
            plt.plot(data_day.index.hour, data_day[var])

        plt.title(f'Valores diarios superpuestos para {var}')
        plt.xlabel('Hora del día')
        plt.ylabel('Valor')
        plt.show()
    else:
        print(f"La variable {var} no se encuentra en el dataframe.")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Normaliza los datos antes del clustering
scaler = StandardScaler()
data_scaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

# Método del codo para determinar el número óptimo de clusters
def metodo_del_codo(data_scaled):
    distortions = []
    K = range(1, 10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k, random_state=0)
        kmeanModel.fit(data_scaled)
        distortions.append(kmeanModel.inertia_)

    plt.figure(figsize=(12,6))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Número de clusters')
    plt.ylabel('Distorsión')
    plt.title('El Método del Codo mostrando el número óptimo de clusters')
    plt.show()

metodo_del_codo(data_scaled[[var for var in variables if var in data.columns]])

# Asignar el número óptimo de clusters basado en la observación del método del codo
num_clusters_optimo = 3  # Este valor debe ajustarse basado en los resultados del método del codo

# Aplica K-means usando el número óptimo de clusters identificado
for var in variables:
    if var in data.columns:
        kmeans = KMeans(n_clusters=num_clusters_optimo, random_state=0).fit(data_scaled[[var]])
        data[var + '_cluster'] = kmeans.labels_

# Muestra los clusters en un gráfico
plt.figure(figsize=(12,6))
sns.scatterplot(x=data.index.hour, y=data[var], hue=data[var + '_cluster'], palette='viridis')
plt.title(f'Clusters diarios para {var} con {num_clusters_optimo} clusters')
plt.xlabel('Hora del día')
plt.ylabel('Valor')
plt.legend(title='Cluster')
plt.show()

df = data[['V005_vent01_CO2', 'V022_vent02_CO2', 'V006_vent01_temp_out', 'V023_vent02_temp_out']]

# Elimina las filas con valores faltantes o reemplaza con la media
# df = df.dropna()
imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Normaliza los datos
scaler = StandardScaler()
df_normalized = scaler.fit_transform(df_imputed)

# Aplica el algoritmo K-means con 3 clusters
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(df_normalized)
df['cluster'] = clusters  # Añade la asignación de clusters al DataFrame original

# Obtiene los centroides de los clusters
centroids = kmeans.cluster_centers_

# Grafica los datos y los centroides
plt.figure(figsize=(12, 6))

# Grafica los puntos de datos para cada cluster, ajusta las columnas según corresponda
for cluster in np.unique(clusters):
    plt.scatter(df[df['cluster'] == cluster]['V005_vent01_CO2'],
                df[df['cluster'] == cluster]['V006_vent01_temp_out'],
                alpha=0.5,
                label=f'Cluster {cluster}')

# Ajuste necesario para graficar los centroides correctamente
# Escala inversa de los centroides para coincidir con los datos originales
centroids_original = scaler.inverse_transform(centroids)

plt.scatter(centroids_original[:, 0], centroids_original[:, 2], marker='x', color='red', label='Centroides')

plt.xlabel('CO2 Ventilation NE (ppm)')
plt.ylabel('Temp. Vent. NE Out (°C)')
plt.title('Clusters de CO2 y Temperatura')
plt.legend()
plt.show()


