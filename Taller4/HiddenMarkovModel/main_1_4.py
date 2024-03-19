
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
from hmmlearn import hmm
#%pip install hmmlearn

import random

# Set a random seed for the random module
random.seed(43)
# Set a random seed for NumPy
np.random.seed(43)

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
    # Leer el archivo CSV
    df = read_csv_file(file_path)
    
    # Convertir la columna "timestamp" a formato de fecha y hora
    df['timestamp1'] = pd.to_datetime(df['timestamp'])
    
    # Establecer la columna "timestamp" como el índice del DataFrame
    df.set_index('timestamp1', inplace=True)
    
    # Extraer la hora de cada marca de tiempo y usarla como columna adicional
    df['Hour'] = df.index.hour
    
    return df


def train_hmm_and_predict(df):
    # Obtener todas las observaciones
    all_observations = df.values
    
    # Determinar el rango óptimo de número de estados ocultos
    n_min = 4
    n_max = 20
    best_log_likelihood = -10_000_000_000_000
    best_model = None
    for n_components in range(n_min, n_max + 1):
        model = hmm.GaussianHMM(n_components=n_components)
        model.fit(all_observations)
        # log_likelihood = model.score(all_observations)
        log_likelihood = model.bic(all_observations)
        # Calcular la diferencia porcentual entre el logaritmo de probabilidad actual y el mejor
        percent_difference = -1*(log_likelihood - best_log_likelihood) / best_log_likelihood
        print(f'Diferencia porcentual log i - best: {percent_difference}')
        print(f'Log likelihood: {log_likelihood}')
        if percent_difference > 0.01:
            best_log_likelihood = log_likelihood
            best_model = model
            print("Mejor Logaritmo de Probabilidad:")
            print(f'Best log lokelihooh {best_log_likelihood}')
            print(f'n: {model.n_components}')
    
    # Predecir la secuencia de estados ocultos para cada observación
    hidden_state_sequences = best_model.predict(all_observations)
    
    return best_model, hidden_state_sequences

def assign_labels_to_data(df, hidden_state_sequences):
    # Asignar etiquetas a cada fila del DataFrame original según el estado oculto predicho
    df_with_labels = df.copy()
    df_with_labels['Label'] = hidden_state_sequences
    
    return df_with_labels

def plot_boxplots_by_label(df_with_labels, df_name):
    # Count the occurrences of each cluster label
    cluster_counts = df_with_labels['Label'].value_counts()
    
    # Filter clusters with more than 10 observations
    clusters_to_plot = cluster_counts[cluster_counts > 10].index
    
    # Iterate over each cluster label
    for label in clusters_to_plot:
        # Select rows with the current label
        df_label = df_with_labels[df_with_labels['Label'] == label]
        
        # Plot boxplots for each column
        fig, ax = plt.subplots(figsize=(12, 6))
        df_label.boxplot(ax=ax)
        plt.title(f'Boxplots for Cluster {label} - {df_name}')
        plt.xticks(rotation=45)
        plt.xlabel('Hours')
        plt.ylabel('CO2')
        plt.tight_layout()
        plt.show()

def plot_probability_distributions(model, title):
    n_components = model.n_components
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    
    plt.figure(figsize=(12, 6))
    for i in range(n_components):
        # Get the parameters of the Gaussian distribution for the i-th hidden state
        mean = model.means_[i][0]
        cov = model.covars_[i][0][0]  # Assuming diagonal covariance matrix
        
        # Generate 1000 points for the x-axis
        x = np.linspace(mean - 3 * np.sqrt(cov), mean + 3 * np.sqrt(cov), 1000)
        
        # Calculate the probability density function (PDF) for the Gaussian distribution
        pdf = np.exp(-0.5 * ((x - mean) / np.sqrt(cov))**2) / (np.sqrt(2 * np.pi * cov))
        
        # Cycle through colors list to ensure we have enough colors
        color = colors[i % len(colors)]
        
        # Plot the PDF
        plt.plot(x, pdf, color, label=f'Cluster {i}')
    
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
    
def print_cluster_counts(df_with_labels):
    # Count the occurrences of each cluster label
    cluster_counts = df_with_labels['Label'].value_counts()
    
    # Print the counts
    print("Cluster Counts:")
    for cluster, count in cluster_counts.items():
        print(f"Cluster {cluster}: {count} observations")

    print(f'max - cluster: {max(cluster_counts.keys())}')
    print(f'min - cluster: {min(cluster_counts.keys())}')

os.getcwd()

file_path = './Taller4/HiddenMarkovModel/data/data.csv'  
df = prepare_data(file_path)

df.columns

# Crear un diccionario para almacenar los DataFrames resultantes
# Obtener una lista de las variables de interés
variables = ['V005_vent01_CO2', 'V022_vent02_CO2', 'V006_vent01_temp_out', 'V023_vent02_temp_out']

dataframes_por_variable = {}

# Iterar sobre cada variable y generar el DataFrame correspondiente
for variable in variables:
    # Seleccionar la variable actual y las columnas "timestamp" y "Hour"
    df_variable = df[[variable, 'Hour']]
    
    # Pivotar el DataFrame para tener las horas como filas y los días como columnas
    df_pivot = df_variable.pivot(columns='Hour')
    
    # Cambiar el nombre de las columnas para que solo muestren la hora
    df_pivot.columns = df_pivot.columns.droplevel()
    df_pivot.columns.name = None
    
    # Agregar el DataFrame resultante al diccionario
    dataframes_por_variable[variable] = df_pivot

# Mostrar el primer DataFrame como ejemplo
print("Ejemplo de DataFrame para la variable 'V005_vent01_C02':")
print(dataframes_por_variable['V005_vent01_CO2'])

df_vent_01_co2=dataframes_por_variable['V005_vent01_CO2']
df_vent_02_co2=dataframes_por_variable['V022_vent02_CO2']
df_vent_01_temp=dataframes_por_variable["V006_vent01_temp_out"]
df_vent_02_temp=dataframes_por_variable['V023_vent02_temp_out']

# Agrupar por día y reorganizar las horas en columnas
df_vent_01_co2 = df_vent_01_co2.groupby(pd.Grouper(freq='D')).sum()
df_vent_02_co2 = df_vent_02_co2.groupby(pd.Grouper(freq='D')).sum()

# Mostrar Proceso
print(df_vent_01_co2)

# Entrenar el modelo HMM y predecir las secuencias de estados ocultos
model1, hidden_state_sequences1 = train_hmm_and_predict(df_vent_01_co2)
model2, hidden_state_sequences2 = train_hmm_and_predict(df_vent_02_co2)

# Asignar etiquetas a los datos originales según los estados ocultos predichos
df_with_labels1 = assign_labels_to_data(df_vent_01_co2, hidden_state_sequences1)
df_with_labels2 = assign_labels_to_data(df_vent_02_co2, hidden_state_sequences2)

# Ver el DataFrame con las etiquetas asignadas
print(df_with_labels1) #Vent01
print(df_with_labels2) #Vent02

# Call the function to print the cluster counts
print_cluster_counts(df_with_labels1)
print_cluster_counts(df_with_labels2)

# Call the function to plot boxplots for each label
# plot_boxplots_by_label(df_with_labels1,"V005_vent01_CO2") #will only plot cluster with more than 10 observations
# plot_boxplots_by_label(df_with_labels2, "V022_vent02_CO2") #will only plot cluster with more than 10 observations

# plot_probability_distributions(model1, "V005_vent01_CO2")

def plot_cluster_counts(df, year, i_axis, name):
    df_year = df.loc[year]

    df_year['Average'] = df_year.iloc[:, 0:24].mean(axis=1)

    scatter = axs[i_axis].scatter(df_year.index, df_year['Label'], c=df_year['Average'], cmap='viridis')
    fig.colorbar(scatter, ax=axs[i], label='Average of hours 0 to 23')
    axs[i_axis].set_title(name + ' - ' + year)
    axs[i_axis].set_xlabel('Timestamp')
    axs[i_axis].set_ylabel('Label')

years = ['2012', '2013', '2014', '2015']

fig, axs = plt.subplots(2, 2, figsize=(15, 10))
axs = axs.flatten()

for i, year in enumerate(years):
    plot_cluster_counts(df_with_labels1, year, i, 'V005_vent01_CO2')
plt.tight_layout()
plt.show()

fig, axs = plt.subplots(2, 2, figsize=(15, 10))
axs = axs.flatten()

for i, year in enumerate(years):
    plot_cluster_counts(df_with_labels2, year, i, 'V022_vent02_CO2')
plt.tight_layout()
plt.show()
