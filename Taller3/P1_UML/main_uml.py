
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:23:01 2024

@author: victorviteri
"""
import os

#from Taller3.P1_UML.p1_uml_util import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

lb_timestamp = "timestamp"
lb_V005_vent01_CO2 = "V005_vent01_CO2"
lb_V022_vent02_CO2 = "V022_vent02_CO2"
lb_V006_vent01_temp_out = "V006_vent01_temp_out"
lb_V023_vent02_temp_out = "V023_vent02_temp_out"

columns = [lb_timestamp, lb_V005_vent01_CO2, lb_V022_vent02_CO2, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out]
alias = {
    lb_timestamp: "timestamp",
    lb_V005_vent01_CO2: "CO2 Ventilation NE",
    lb_V022_vent02_CO2: "CO2 Ventilation SW",
    lb_V006_vent01_temp_out: "Temp. Vent. NE Out",
    lb_V023_vent02_temp_out: "Temp. Vent. SW Out"
}

def read_csv_file(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, sep=';')
    except Exception as e:
        print(f"Error reading file: {file_path}")
        print(e)
        return pd.DataFrame()


def prepare_data(file_path: str):
    script_path = os.path.dirname(os.path.abspath(file_path))
    data_path = os.path.join(script_path, "data")
    file_path = os.path.join(data_path, "data.csv")
    _df = read_csv_file(file_path)
    #_df.set_index(lb_timestamp, inplace=True)
    print(_df.dtypes)
    return _df

def plot_data(df: pd.DataFrame, column: str, legend: str):
    # Extract hour from timestamp
    df.index = pd.to_datetime(df.index)  # Ensure the index is in datetime format
    df['Hour'] = df.index.hour
    
    # Create a boxplot for each hour
    plt.figure(figsize=(12, 6))  # Set figure size
    sns.boxplot(x='Hour', y=column, data=df)
    
    plt.xlabel('Hour of the Day')
    plt.ylabel(legend)
    plt.title('Boxplot of ' + legend + ' by Hour')
    plt.show()

def elbow_method(dataframe, max_clusters):
    # Convertir los nombres de las columnas a tipo string si es necesario
    if not all(isinstance(col, str) for col in dataframe.columns):
        dataframe.columns = dataframe.columns.astype(str)
    
    # Lista para almacenar las inercias
    inertias = []
    
    # Iterar sobre el rango de valores de k
    for k in range(1, max_clusters + 1):
        # Inicializar y ajustar el modelo KMeans
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(dataframe)
        
        # Calcular la inercia y añadirla a la lista
        inertias.append(kmeans.inertia_)
    
    # Graficar la curva de codo
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), inertias, marker='o', linestyle='--')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.xticks(range(1, max_clusters + 1))
    plt.grid(True)
    plt.show()
  
def elbow_method_subplot(row,col,dataframe_list, names_list, max_clusters):
    # Convertir los nombres de las columnas a tipo string si es necesario
    plt.figure(figsize=(8, 6))
    for i, dataframe in enumerate(dataframe_list):
        if not all(isinstance(col, str) for col in dataframe.columns):
            dataframe.columns = dataframe.columns.astype(str)
        
        # Lista para almacenar las inercias
        inertias = []
        
        # Iterar sobre el rango de valores de k
        for k in range(1, max_clusters + 1):
            # Inicializar y ajustar el modelo KMeans
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(dataframe)
            
            # Calcular la inercia y añadirla a la lista
            inertias.append(kmeans.inertia_)
        
        # Graficar la curva de codo
        plt.subplot(row,col, i+1)
        plt.plot(range(1, max_clusters + 1), inertias, marker='o', linestyle='--')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.title(names_list[i])
        plt.xticks(range(1, max_clusters + 1))
        plt.grid(True)
    
    plt.suptitle('Elbow Method for optimal - K', fontsize=16)    
    plt.tight_layout()
    plt.show()

def visualize_kmeans(df, n_clusters):
    # Inicializar el modelo KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=1000)
    
    # Ajustar el modelo a los datos
    kmeans.fit(df)
    
    # Predecir las etiquetas de cluster para cada muestra
    labels = kmeans.predict(df)
    
    # Visualizar los resultados en un gráfico
    plt.figure(figsize=(8, 6))
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=labels, cmap='viridis')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='x', s=100, c='red', label='Centroids')
    
    # Agregar etiquetas a los puntos
    for i, label in enumerate(labels):
        plt.text(df.iloc[i, 0], df.iloc[i, 1], f'{i}', fontsize=8)
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(f'K-Means Clustering (k={n_clusters})')
    plt.legend()
    plt.show()
    
def visualize_kmeans_subplot(row, col, df_list, names_list, n_clusters):
    # Inicializar el modelo KMeans
    plt.figure(figsize=(8, 6))
    for i, df in enumerate(df_list):
        kmeans = KMeans(n_clusters=n_clusters[i], random_state=1000)
        
        # Ajustar el modelo a los datos
        kmeans.fit(df)
        
        # Predecir las etiquetas de cluster para cada muestra
        labels = kmeans.predict(df)
        
        # Visualizar los resultados en un gráfico
        plt.subplot(row,col, i+1)
        plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=labels, cmap='viridis')
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='x', s=100, c='red', label='Centroids')
        
        # Agregar etiquetas a los puntos
        for j, label in enumerate(labels):
            plt.text(df.iloc[j, 0], df.iloc[j, 1], f'{j}', fontsize=8)
        
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.title(f'{names_list[i]} (k={n_clusters[i]})')
        plt.legend()
        
    plt.suptitle('K-Means Clustering', fontsize=16)    
    plt.tight_layout()
    plt.show()



os.getcwd()

file_path = 'C:\\Users\\User\\Documents\\Maestria AI\\03 Inteligencia Artificial\\Semana3\\WorkShop1-USFQ-main\\Taller3\\P1_UML\\data'  # Reemplaza 'ruta_de_tu_archivo' con la ruta real de tu archivo
df = prepare_data(file_path)

# Convertir la columna "timestamp" a formato de fecha y hora
df['timestamp1'] = pd.to_datetime(df['timestamp'], dayfirst = True)

# Establecer la columna "timestamp" como el índice del DataFrame
df.set_index('timestamp1', inplace=True)

# Extraer la hora de cada marca de tiempo y usarla como columna adicional
df['Hora'] = df.index.hour
df.columns
# Obtener una lista de las variables de interés
variables = ['V005_vent01_CO2', 'V022_vent02_CO2', 'V006_vent01_temp_out',
       'V023_vent02_temp_out']

# Crear un diccionario para almacenar los DataFrames resultantes
dataframes_por_variable = {}

# Iterar sobre cada variable y generar el DataFrame correspondiente
for variable in variables:
    # Seleccionar la variable actual y la columna "timestamp"
    df_variable = df[['timestamp',"Hora" ,variable]].copy()
    
    # Convertir la columna "timestamp" a tipo datetime
    df_variable['timestamp'] = pd.to_datetime(df_variable['timestamp'], dayfirst=True)
    
    # Extraer la fecha de la columna "timestamp"
    df_variable['date'] = df_variable['timestamp'].dt.date
    # Pivotar el DataFrame para tener las horas como filas y los días como columnas
    df_pivot = df_variable.pivot(index='Hora', columns='date', values=variable)
    
    # Agregar el DataFrame resultante al diccionario
    dataframes_por_variable[variable] = df_pivot

# Mostrar el primer DataFrame como ejemplo
print("Ejemplo de DataFrame para la variable 'V005_vent01_C02':")
print(dataframes_por_variable['V005_vent01_CO2'])

df_vent_01_co2=dataframes_por_variable['V005_vent01_CO2']
df_vent_02_co2=dataframes_por_variable['V022_vent02_CO2']
df_vent_01_temp=dataframes_por_variable["V006_vent01_temp_out"]
df_vent_02_temp=dataframes_por_variable['V023_vent02_temp_out']

#1. Plot the variables

plot_data(df,'V005_vent01_CO2' ,'V005_vent01_CO2')
plot_data(df,'V022_vent02_CO2' ,'V022_vent02_CO2')
plot_data(df,'V006_vent01_temp_out' ,'V006_vent01_temp_out')
plot_data(df,'V023_vent02_temp_out' ,'V023_vent02_temp_out')

#2. 

#A. K Means:

# Limpiar datos

print(df.isna().sum())

# Aplicar el método del codo para determinar el número óptimo de clusters
max_clusters = 10  # Puedes ajustar este valor según sea necesario

# Crear un imputador que rellene los NaN con la media de la columna
imputer = SimpleImputer(strategy='mean')
# Aplicar la imputación a tus datos


#Vent_01_co2
df_vent_01_co2_imputed = imputer.fit_transform(df_vent_01_co2)
df_vent_01_co2_imputed = pd.DataFrame(df_vent_01_co2_imputed, columns=df_vent_01_co2.columns)

#Vent_02_co2
df_vent_02_co2 = df_vent_02_co2.apply(pd.to_numeric, errors='coerce')
df_vent_02_co2.columns = df_vent_02_co2.columns.astype(str)
df_vent_02_co2_imputed = imputer.fit_transform(df_vent_02_co2)
df_vent_02_co2_imputed = pd.DataFrame(df_vent_02_co2_imputed, columns=df_vent_02_co2.columns)

#Vent_01_temp
df_vent_01_temp = df_vent_01_temp.apply(pd.to_numeric, errors='coerce')
df_vent_01_temp.columns = df_vent_01_temp.columns.astype(str)
df_vent_01_temp_imputed = imputer.fit_transform(df_vent_01_temp)
df_vent_01_temp_imputed = pd.DataFrame(df_vent_01_temp_imputed, columns=df_vent_01_temp.columns)

#Vent_02_temp
df_vent_02_temp = df_vent_02_temp.apply(pd.to_numeric, errors='coerce')
df_vent_02_temp.columns = df_vent_02_temp.columns.astype(str)
df_vent_02_temp_imputed = imputer.fit_transform(df_vent_02_temp)
df_vent_02_temp_imputed = pd.DataFrame(df_vent_02_temp_imputed, columns=df_vent_02_temp.columns)


# Aplicar el método del codo con los datos imputados convertidos de nuevo a DataFrame
elbow_method(df_vent_01_co2_imputed, max_clusters)
elbow_method(df_vent_02_co2_imputed, max_clusters)
elbow_method(df_vent_01_temp_imputed, max_clusters)
elbow_method(df_vent_02_temp_imputed, max_clusters)
elbow_method_subplot(2,2,[df_vent_01_co2_imputed,df_vent_02_co2_imputed,
                          df_vent_01_temp_imputed,df_vent_02_temp_imputed],
                     ['V005_vent01_CO2','V022_vent02_CO2',
                      'V006_vent01_temp_out','V023_vent02_temp_out'],
                     max_clusters)

# Visulizar los resultados:
visualize_kmeans(df_vent_01_co2_imputed, n_clusters=3)
visualize_kmeans(df_vent_02_co2_imputed, n_clusters=2)
visualize_kmeans(df_vent_01_temp_imputed, n_clusters=3)
visualize_kmeans(df_vent_02_temp_imputed, n_clusters=2)
visualize_kmeans_subplot(2,2,[df_vent_01_co2_imputed,df_vent_02_co2_imputed,
                          df_vent_01_temp_imputed,df_vent_02_temp_imputed],
                         ['V005_vent01_CO2','V022_vent02_CO2',
                          'V006_vent01_temp_out','V023_vent02_temp_out'],
                         [3,2,3,2])

#B. Define a function to apply PCA and K-means clustering with the elbow method for choosing K
def apply_pca_and_kmeans(df, max_clusters):
    # Standardize the features
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    
    # Apply PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df_scaled)
    pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
    
    # Calculate the explained variance ratio for the first two principal components
    explained_variance_ratio = pca.explained_variance_ratio_
    variance_explained_pca1 = explained_variance_ratio[0] * 100
    variance_explained_pca2 = explained_variance_ratio[1] * 100
    
    # Apply the elbow method to determine the optimal number of clusters
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(pca_df)
        inertias.append(kmeans.inertia_)
    
    # Plot the elbow method
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), inertias, marker='o', linestyle='--')
    
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.grid(True)
    plt.show()
    
    return pca_df, variance_explained_pca1, variance_explained_pca2, pca

def apply_pca_and_kmeans_subplot(row,col,df_list,names_list, max_clusters):
    
    pca_df_list =[]
    variance_explained_pca1_list = []
    variance_explained_pca2_list = []
    pca_list = []
    plt.figure(figsize=(8, 6))
    for i, df in enumerate(df_list):
        # Standardize the features
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df)
        
        # Apply PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(df_scaled)
        pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
        
        # Calculate the explained variance ratio for the first two principal components
        explained_variance_ratio = pca.explained_variance_ratio_
        variance_explained_pca1 = explained_variance_ratio[0] * 100
        variance_explained_pca2 = explained_variance_ratio[1] * 100
        
        # Apply the elbow method to determine the optimal number of clusters
        inertias = []
        for k in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(pca_df)
            inertias.append(kmeans.inertia_)
            
        pca_df_list.append(pca_df)
        variance_explained_pca1_list.append(variance_explained_pca1)
        variance_explained_pca2_list.append(variance_explained_pca2_list)
        pca_list.append(pca)
        
        # Plot the elbow method
        plt.subplot(row,col,i+1)
        plt.plot(range(1, max_clusters + 1), inertias, marker='o', linestyle='--')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.title(f'{names_list[i]}')
        plt.grid(True)
        
    plt.suptitle('Elbow Method for Optimal K')
    plt.tight_layout()
    plt.show()
    
    return pca_df_list, variance_explained_pca1_list, variance_explained_pca2_list, pca_list


# Define the maximum number of clusters for the elbow method
max_clusters = 10

# B. PCA and K-means clustering with the elbow method for each variable
# Apply PCA and K-means for vent_01_co2 dataset
pca_df_vent_01_co2, variance_explained_pca1_vent_01_co2, variance_explained_pca2_vent_01_co2, pca_vent_01_co2 = apply_pca_and_kmeans(df_vent_01_co2_imputed, max_clusters=10)
print("Variance explained by PCA1 (vent_01_co2):", variance_explained_pca1_vent_01_co2)
print("Variance explained by PCA2 (vent_01_co2):", variance_explained_pca2_vent_01_co2)

# Apply PCA and K-means for vent_02_co2 dataset
pca_df_vent_02_co2, variance_explained_pca1_vent_02_co2, variance_explained_pca2_vent_02_co2, pca_vent_02_co2 = apply_pca_and_kmeans(df_vent_02_co2_imputed, max_clusters=10)
print("Variance explained by PCA1 (vent_02_co2):", variance_explained_pca1_vent_02_co2)
print("Variance explained by PCA2 (vent_02_co2):", variance_explained_pca2_vent_02_co2)

# Apply PCA and K-means for vent_01_temp dataset
pca_df_vent_01_temp, variance_explained_pca1_vent_01_temp, variance_explained_pca2_vent_01_temp, pca_vent_01_temp = apply_pca_and_kmeans(df_vent_01_temp_imputed, max_clusters=10)
print("Variance explained by PCA1 (vent_01_temp):", variance_explained_pca1_vent_01_temp)
print("Variance explained by PCA2 (vent_01_temp):", variance_explained_pca2_vent_01_temp)

# Apply PCA and K-means for vent_02_temp dataset
pca_df_vent_02_temp, variance_explained_pca1_vent_02_temp, variance_explained_pca2_vent_02_temp, pca_vent_02_temp = apply_pca_and_kmeans(df_vent_02_temp_imputed, max_clusters=10)
print("Variance explained by PCA1 (vent_02_temp):", variance_explained_pca1_vent_02_temp)
print("Variance explained by PCA2 (vent_02_temp):", variance_explained_pca2_vent_02_temp)

pca_df, variance_explained_pca1, variance_explained_pca2, pca_list = apply_pca_and_kmeans_subplot(2,2,[df_vent_01_co2_imputed,
                                                                                             df_vent_02_co2_imputed,
                                                                                             df_vent_01_temp_imputed,
                                                                                             df_vent_02_temp_imputed],
                                                                                        ['vent_01_co2','vent_02_co2',
                                                                                         'vent_01_temp','vent_02_temp'],
                                                                                        10)

# Define feature labels for biplot
# Define a function to plot PCA biplot and cluster visualization
def plot_pca_and_clusters(pca_df, clus_k, pca):
    
    # Choose the optimal K based on the elbow method
    # Apply K-means clustering with the optimal K
    kmeans = KMeans(n_clusters=clus_k, random_state=42)
    cluster_labels = kmeans.fit_predict(pca_df)
    
    # Get the principal components (eigenvectors)
    pca_components = pca.components_.T
    
    plt.figure(figsize=(8, 6))
    
    # Plot the PCA biplot
    for i, (pc1, pc2) in enumerate(pca_components):
        plt.arrow(0, 0, pc1, pc2, color='r', alpha=0.5)
        
    # Plot the data points on the PCA space with cluster labels
    # scatter = plt.scatter(pca_df['PC1'], pca_df['PC2'], c=cluster_labels, cmap='viridis', alpha=0.6)
    # plt.scatter(pca_df['PC1'], pca_df['PC2'], c=cluster_labels, cmap='viridis', alpha=0.6)
    
    plt.scatter(pca_df['PC1'], pca_df['PC2'], c=cluster_labels, cmap='viridis', alpha=0.7)
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='x', s=100, c='red', label='Centroids')
    
    # Add labels for each point
    for i, label in enumerate(cluster_labels):
        plt.text(pca_df.iloc[i]['PC1'], pca_df.iloc[i]['PC2'], f'{i}', fontsize=8)
    
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(f'PCA Biplot with Cluster Visualization (k = {clus_k})')
    plt.legend()
    #plt.colorbar(scatter, label='Cluster')
    plt.grid()
    plt.show()
    
    return cluster_labels
    
def plot_pca_and_clusters_subplot(row,col,pca_df_list, names_list, clus_k, pca):
    
    cluster_labels_list = []
    plt.figure(figsize=(8, 6))
    for i, pca_df in enumerate(pca_df_list):
        # Choose the optimal K based on the elbow method
        # Apply K-means clustering with the optimal K
        kmeans = KMeans(n_clusters=clus_k[i], random_state=42)
        cluster_labels = kmeans.fit_predict(pca_df)
        
        # Get the principal components (eigenvectors)
        pca_components = pca[i].components_.T
        
        plt.subplot(row,col,i+1)
        # Plot the PCA biplot
        for j, (pc1, pc2) in enumerate(pca_components):
            plt.arrow(0, 0, pc1, pc2, color='r', alpha=0.5)
            
        # Plot the data points on the PCA space with cluster labels
        # scatter = plt.scatter(pca_df['PC1'], pca_df['PC2'], c=cluster_labels, cmap='viridis', alpha=0.6)
        
        plt.scatter(pca_df['PC1'], pca_df['PC2'], c=cluster_labels, cmap='viridis', alpha=0.7)
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='x', s=100, c='red', label='Centroids')
        
        # Add labels for each point
        for j, label in enumerate(cluster_labels):
            plt.text(pca_df.iloc[j]['PC1'], pca_df.iloc[j]['PC2'], f'{j}', fontsize=8)
        
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.title(f'{names_list[i]} (k = {clus_k[i]})')
        # plt.colorbar(label='Cluster')
        plt.legend()
        plt.grid()
        
        cluster_labels_list.append(cluster_labels)
        
    plt.suptitle('PCA Biplot with Cluster Visualization')
    plt.tight_layout()
    plt.show()
    
    return cluster_labels_list

# Plot PCA biplot and cluster visualization for each variable
cluster_labels_vent_01_co2 = plot_pca_and_clusters(pca_df_vent_01_co2, 3, pca_vent_01_co2)
cluster_labels_vent_02_co2 = plot_pca_and_clusters(pca_df_vent_02_co2, 3, pca_vent_01_co2)
cluster_labels_vent_01_temp = plot_pca_and_clusters(pca_df_vent_01_temp, 3, pca_vent_01_temp)
cluster_labels_vent_02_temp = plot_pca_and_clusters(pca_df_vent_02_temp, 3, pca_vent_02_temp)

cluster_labels_list = plot_pca_and_clusters_subplot(2,2,[pca_df_vent_01_co2,pca_df_vent_02_co2,
                                   pca_df_vent_01_temp,pca_df_vent_02_temp],
                              ['vent_01_co2','vent_02_co2',
                               'vent_01_temp',
                               'vent_02_temp'],
                              [3,3,3,3], [pca_vent_01_co2,pca_vent_01_co2,
                                          pca_vent_01_temp,pca_vent_02_temp])


# 3. 


def detect_anomalies(pca_df, cluster_labels):
    # Calculate the distance of each data point to the centroids
    distances = []
    for i in range(len(pca_df)):
        cluster_id = cluster_labels[i]
        centroid = np.mean(pca_df[cluster_labels == cluster_id], axis=0)
        distance = np.linalg.norm(pca_df.iloc[i] - centroid)
        distances.append(distance)
    
    # Define a threshold for anomaly detection (e.g., based on a certain percentile of distances)
    Q1 = np.percentile(distances, 25)  # Adjust the percentile as needed
    Q3 = np.percentile(distances, 75)
    IQR = Q3 - Q1
    
    # Rango intercartiluco
    LI = Q1 - 1.5* IQR
    LS = Q3 + 1.5* IQR
    
    # Identify anomalies
    anomalies = pca_df[(distances < LI) | (distances > LS)]
    
    return anomalies

# Detect anomalies for each variable
anomalies_vent_01_co2 = detect_anomalies(pca_df_vent_01_co2, cluster_labels_vent_01_co2)
anomalies_vent_01_co2["variable"] = "vent_01_co2"
anomalies_vent_02_co2 = detect_anomalies(pca_df_vent_02_co2, cluster_labels_vent_02_co2)
anomalies_vent_02_co2["variable"] = "vent_02_co2"
anomalies_vent_01_temp = detect_anomalies(pca_df_vent_01_temp, cluster_labels_vent_01_temp)
anomalies_vent_01_temp["variable"] = "vent_01_temp"
anomalies_vent_02_temp = detect_anomalies(pca_df_vent_02_temp, cluster_labels_vent_02_temp)
anomalies_vent_02_temp["variable"] = "vent_02_temp"


# Print or visualize the anomalies
print("Anomalies in Vent 01 CO2:")
print(anomalies_vent_01_co2)
print("Anomalies in Vent 02 CO2:")
print(anomalies_vent_02_co2)
print("Anomalies in Vent 01 Temp:")
print(anomalies_vent_01_temp)
print("Anomalies in Vent 02 Temp:")
print(anomalies_vent_02_temp)

df_anomalias = pd.DataFrame()
for anomalias in [anomalies_vent_01_co2,anomalies_vent_02_co2,anomalies_vent_01_temp,anomalies_vent_02_temp]:
    df_anomalias = pd.concat((df_anomalias, anomalias.reset_index()), axis = 0)
df_anomalias.columns = ["hours","PC1","PC2","variables"]
df_anomalias = df_anomalias.reset_index(drop=True)

"""Utilizando la metodología de análisis de componentes principales (PCA) combinada con técnicas de agrupación (en este caso, K-means), 
se detectaron anomalías en los perfiles diarios de CO2 y temperatura en los sistemas de ventilación Vent 01 y Vent 02. 
Las anomalías se identificaron mediante la distancia de los puntos de datos a los centroides de los clusters obtenidos 
a partir de los datos reducidos por PCA.

En el caso de CO2 en Vent 01, se observaron dos puntos anómalos en las horas 8 y 17, con valores de PC1 y PC2 (las dos componentes principales)
que se desvían significativamente de los patrones típicos. Para CO2 en Vent 02, se detectaron también dos anomalías en las mismas horas, 
con características similares a las observadas en Vent 01. 

Respecto a la temperatura en Vent 01, se identificaron dos puntos anómalos en las horas 18 y 19, mientras que en Vent 02 se encontraron 
dos anomalías en la hora 5 y 19.

Estas anomalías podrían indicar eventos inusuales o problemas en los sistemas de ventilación durante esas horas específicas. 
Este enfoque proporciona una manera sistemática de detectar patrones atípicos en los datos diarios, lo que puede ser crucial 
para el mantenimiento y la detección temprana de posibles problemas en los sistemas de ventilación, permitiendo una respuesta 
rápida y eficiente para garantizar la calidad del aire interior y la eficiencia energética.

"""

# 4.

scaler = StandardScaler()
##ESTANDARIZACION NE
# Normalizar y estandarizar df_vent_01_co2_imputed
df_vent_01_co2_normalized = scaler.fit_transform(df_vent_01_co2_imputed)

# Normalizar y estandarizar df_vent_01_temp_imputed
df_vent_01_temp_normalized = scaler.fit_transform(df_vent_01_temp_imputed)

# Convertir las matrices normalizadas en DataFrames de Pandas
df_vent_01_co2_normalized = pd.DataFrame(df_vent_01_co2_normalized, columns=df_vent_01_co2_imputed.columns)
df_vent_01_temp_normalized = pd.DataFrame(df_vent_01_temp_normalized, columns=df_vent_01_temp_imputed.columns)

# Concatenar las dos matrices normalizadas
df_vent_01_NE = pd.concat([df_vent_01_co2_normalized, df_vent_01_temp_normalized], axis=1)

# Verificar la matriz resultante
print(df_vent_01_NE)

# ESTANDARIZACION SW

# Normalizar y estandarizar df_vent_02_co2_imputed
df_vent_02_co2_normalized = scaler.fit_transform(df_vent_02_co2_imputed)
df_vent_02_co2_normalized = pd.DataFrame(df_vent_02_co2_normalized, columns=df_vent_02_co2_imputed.columns)

# Normalizar y estandarizar df_vent_02_temp_imputed
df_vent_02_temp_normalized = scaler.fit_transform(df_vent_02_temp_imputed)
df_vent_02_temp_normalized = pd.DataFrame(df_vent_02_temp_normalized, columns=df_vent_02_temp_imputed.columns)

# Concatenar las dos matrices normalizadas
df_vent_02_SW = pd.concat([df_vent_02_co2_normalized, df_vent_02_temp_normalized], axis=1)

# Verificar la matriz resultante
print(df_vent_02_SW)

# A. Aplicar el método del codo con los datos
elbow_method(df_vent_01_NE, max_clusters)
elbow_method(df_vent_02_SW, max_clusters)
elbow_method_subplot(2,2,[df_vent_01_NE,df_vent_02_SW],['vent_01_NE','df_vent_02_SW'], max_clusters)

visualize_kmeans(df_vent_01_NE, n_clusters=4)
visualize_kmeans(df_vent_02_SW, n_clusters=4)
visualize_kmeans_subplot(2,2,[df_vent_01_NE,df_vent_02_SW],['vent_01_NE','df_vent_02_SW'], [4,4])

# B. 

# Apply PCA and K-means for df_vent_01_NE dataset
pca_df_vent_01_NE, variance_explained_pca1_vent_01_NE, variance_explained_pca2_vent_01_NE, pca_vent_01_NE = apply_pca_and_kmeans(df_vent_01_NE, max_clusters=10)
print("Variance explained by PCA1 (df_vent_01_NE):", variance_explained_pca1_vent_01_NE)
print("Variance explained by PCA2 (df_vent_01_NE):", variance_explained_pca2_vent_01_NE)


# Apply PCA and K-means for df_vent_02_SW dataset
pca_df_vent_02_SW, variance_explained_pca1_vent_02_SW, variance_explained_pca2_vent_02_SW, pca_vent_02_SW = apply_pca_and_kmeans(df_vent_02_SW, max_clusters=10)
print("Variance explained by PCA1 (df_vent_02_SW):", variance_explained_pca1_vent_02_SW)
print("Variance explained by PCA2 (df_vent_02_S2):", variance_explained_pca2_vent_02_SW)

pca_df_vent_bi, variance_explained_pca1_vent_bi, variance_explained_pca2_vent_bi, pca_bi_list = apply_pca_and_kmeans_subplot(2,2,
                                                                                                                             [df_vent_01_NE,df_vent_02_SW],
                                                                                                                             ['vent_01_NE','vent_02_SW'],
                                                                                                                             10)


# Plot PCA biplot and cluster visualization for df_vent_01_NE
cluster_labels_vent_01_NE = plot_pca_and_clusters(pca_df_vent_01_NE, 4, pca_vent_01_NE)

# Plot PCA biplot and cluster visualization for df_vent_02_SW
cluster_labels_vent_02_SW = plot_pca_and_clusters(pca_df_vent_02_SW, 4, pca_vent_02_SW)

cluster_labels_vent_bi = plot_pca_and_clusters_subplot(2,2,[pca_df_vent_01_NE,pca_df_vent_02_SW],
                              ['vent_01_NE','vent_02_SW'],
                              [4,4],pca_bi_list)

# 5 Anomalias:
# Detect anomalies for each variable
# Detectar anomalías en pca_df_vent_01_NE
anomalies_vent_01_NE = detect_anomalies(pca_df_vent_01_NE, cluster_labels_vent_01_NE)
anomalies_vent_01_NE["variable"] = "vent_01_NE"
# Detectar anomalías en pca_df_vent_02_SW
anomalies_vent_02_SW = detect_anomalies(pca_df_vent_02_SW, cluster_labels_vent_02_SW)
anomalies_vent_02_SW["variable"] = "vent_02_SW"


print("Anomalies in NE")
print(anomalies_vent_01_NE)

print("Anomalies in SW")
print(anomalies_vent_02_SW )

df_anomalias_bi = pd.DataFrame()
for anomalias in [anomalies_vent_01_NE,anomalies_vent_02_SW]:
    df_anomalias_bi = pd.concat((df_anomalias_bi, anomalias.reset_index()), axis = 0)
df_anomalias_bi.columns = ["hours","PC1","PC2","variables"]
df_anomalias_bi = df_anomalias_bi.reset_index(drop=True)


# Graficar los cluster en las series de tiempo originales.

df['timestamp1'] = pd.to_datetime(df['timestamp'], dayfirst = True)

def labels_df(labels, names):
    label_df = pd.DataFrame(labels, columns=[names]).reset_index()
    label_df.columns = ["Hour",names]
    
    return label_df

labels_vent_01_co2 = labels_df(cluster_labels_vent_01_co2, "vent_01_co2")
labels_vent_02_co2 = labels_df(cluster_labels_vent_02_co2, "vent_02_co2")
labels_vent_01_temp = labels_df(cluster_labels_vent_01_temp, "vent_01_temp")
labels_vent_02_temp = labels_df(cluster_labels_vent_02_temp, "vent_02_temp")
label_vent_01_NE = labels_df(cluster_labels_vent_01_NE, "cluster_vent_01_NE")
label_vent_02_SW = labels_df(cluster_labels_vent_02_SW, "cluster_vent_02_SW")

df_left_join = pd.merge(df, label_vent_01_NE, on='Hour', how='left')
df_left_join = pd.merge(df_left_join, label_vent_02_SW, on='Hour', how='left')
df_left_join = pd.merge(df_left_join, labels_vent_01_co2, on='Hour', how='left')
df_left_join = pd.merge(df_left_join, labels_vent_02_co2, on='Hour', how='left')
df_left_join = pd.merge(df_left_join, labels_vent_01_temp, on='Hour', how='left')
df_left_join = pd.merge(df_left_join, labels_vent_02_temp, on='Hour', how='left')

plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V005_vent01_CO2',hue='vent_01_co2', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,2)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V022_vent02_CO2',hue='vent_02_co2', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,3)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V006_vent01_temp_out',hue='vent_01_temp', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,4)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V023_vent02_temp_out',hue='vent_02_temp', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
sns.scatterplot(data=df_left_join, x='Hour', y='V005_vent01_CO2',hue='vent_01_co2', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,2)
sns.scatterplot(data=df_left_join, x='Hour', y='V022_vent02_CO2',hue='vent_02_co2', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,3)
sns.scatterplot(data=df_left_join, x='Hour', y='V006_vent01_temp_out',hue='vent_01_temp', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,4)
sns.scatterplot(data=df_left_join, x='Hour', y='V023_vent02_temp_out',hue='vent_02_temp', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V005_vent01_CO2',hue='cluster_vent_01_NE', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,2)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V022_vent02_CO2',hue='cluster_vent_02_SW', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,3)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V006_vent01_temp_out',hue='cluster_vent_01_NE', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,4)
sns.scatterplot(data=df_left_join, x='timestamp1', y='V023_vent02_temp_out',hue='cluster_vent_02_SW', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
sns.scatterplot(data=df_left_join, x='Hour', y='V005_vent01_CO2',hue='cluster_vent_01_NE', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,2)
sns.scatterplot(data=df_left_join, x='Hour', y='V022_vent02_CO2',hue='cluster_vent_02_SW', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,3)
sns.scatterplot(data=df_left_join, x='Hour', y='V006_vent01_temp_out',hue='cluster_vent_01_NE', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.subplot(2,2,4)
sns.scatterplot(data=df_left_join, x='Hour', y='V023_vent02_temp_out',hue='cluster_vent_02_SW', edgecolor='none', palette='viridis')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()