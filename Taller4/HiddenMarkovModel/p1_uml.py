import os
import numpy as np
from hmmlearn import hmm
from p1_uml_util import *


def prepare_data():
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_path, "data")
    file_path = os.path.join(data_path, "data.csv")
    _df = read_csv_file(file_path)
    _df.set_index(lb_timestamp, inplace=True)
    print(_df.dtypes)
    return _df

def plot_data(_df: pd.DataFrame, lb1, lb2, legend):
    import matplotlib.pyplot as plt
    df_to_plot = _df.tail(1000)
    plt.plot(df_to_plot.index, df_to_plot[lb1], label=alias[lb_V005_vent01_CO2])
    plt.plot(df_to_plot.index, df_to_plot[lb2], label=alias[lb_V022_vent02_CO2])
    plt.xlabel(lb_timestamp)
    plt.ylabel(legend)
    plt.legend()
    plt.show()

def simple_hmm_example():
    # Define the HMM parameters
    n_components = 2  # Number of hidden states
    # n_features is 24, for each hour of the day
    n_features = 4  # Number of features (dimensionality of the observation space)

    # Generate some example training data
    np.random.seed(42)
    # replace this with real data
    observed_data = np.random.randn(100, n_features)

    # Create a Gaussian HMM model
    model = hmm.GaussianHMM(n_components=n_components, covariance_type="full", n_iter=100)

    # Fit the model to the observed data
    model.fit(observed_data)

    # Print the learned parameters
    print("Transition matrix:\n", model.transmat_)
    print("Means:\n", model.means_)
    print("Covariances:\n", model.covars_)
    print("Start probabilities:\n", model.startprob_)

    # Now let's decode a new sequence of observations
    # use the same observations that were used in the training (line 35)
    new_observations = np.random.randn(10, n_features)

    # Decode the sequence of observations, i.e. find the most likely sequence of hidden states
    # this should help you to group the observations in different states
    decoded_states = model.predict(new_observations)

    # Print the decoded states
    print("Decoded states:", decoded_states)



if __name__ == "__main__":
    df = prepare_data()
    plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
    simple_hmm_example()

    # Ejemplo de cómo visualizar los estados decodificados a lo largo del tiempo
    decoded_states = [0, 1, 0, 1, 1, 1, 1, 0, 0, 1]  # Ejemplo, reemplaza con tu secuencia real   
    # Crear una secuencia de tiempo para el eje x
    time_sequence = range(len(decoded_states))
    import matplotlib.pyplot as plt
    # Crear un gráfico de líneas para visualizar los estados decodificados
    plt.figure(figsize=(10, 6))
    plt.plot(time_sequence, decoded_states, marker='o', linestyle='-')
    plt.xlabel('Tiempo')
    plt.ylabel('Estado Decodificado')
    plt.title('Secuencia de Estados Decodificados a lo largo del tiempo')
    plt.grid(True)
    plt.show()
    
    
    
    
    
    
    # Importa las bibliotecas necesarias
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# URL del archivo CSV en bruto en GitHub
url = "https://raw.githubusercontent.com/Borreguin/WorkShop1-USFQ/main/Taller3/P1_UML/data/data.csv"

# Lee el archivo CSV desde GitHub
# Asegúrate de especificar el delimitador correcto
data = pd.read_csv(url, delimiter=';')

# Imprime los nombres de las columnas para verificarlos
print("Columnas en el dataframe: ", data.columns)

# Asegúrate de que tus datos estén indexados por fecha
data.index = pd.to_datetime(data['timestamp'])
data = data.drop(columns=['timestamp'])

variables = ['V005_vent01_CO2', 'V022_vent02_CO2', 'V006_vent01_temp_out', 'V023_vent02_temp_out']

for var in variables:
    # Verifica si la variable está en el dataframe antes de trazarla
    if var in data.columns:
        plt.figure(figsize=(10,6))
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
        
        
        
        #%pip install hmmlearn
        
        
        
        from hmmlearn import hmm
import numpy as np

# Selecciona las variables
variables = ['V005_vent01_CO2', 'V006_vent01_temp_out']

# Define el rango de valores para n_components
n_min = 2
n_max = 10

# Crea un modelo HMM para cada variable
for var in variables:
    if var in data.columns:

      # Desglosa la variable en observaciones de 24h
        observations = [data[var][i:i+24] for i in range(0, len(data[var]), 24)]

      # Elimina las listas que no tienen exactamente 24 elementos
        observations = [obs for obs in observations if len(obs) == 24]

      # Convierte las observaciones en un array de NumPy
        observations = np.array(observations)

      # Reemplaza los valores NaN con la media de las observaciones
        observations = np.where(np.isnan(observations), np.ma.array(observations, mask=np.isnan(observations)).mean(axis=0), observations)

       # Prueba diferentes valores para n_components
for n_components in range(n_min, n_max+1):
    # Inicializa best_score con un valor por defecto
    best_score = -np.inf

    # Crea y entrena el modelo HMM
    model = hmm.GaussianHMM(n_components=n_components, covariance_type="full")
    model.fit(observations)

    # Calcula la verosimilitud del modelo
    score = model.score(observations)

    # Si la verosimilitud es mejor que la mejor encontrada hasta ahora, actualiza la mejor verosimilitud y el mejor n_components
    if score > best_score:
        best_score = score
        best_n_components = n_components
        
        
        from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Genera algunos datos de muestra
X, y = make_blobs(n_samples=300, centers=4, random_state=0, cluster_std=0.60)

# Ajusta el modelo K-means a los datos
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)

# Predice las etiquetas de los clusters para los datos
y_kmeans = kmeans.predict(X)

# Visualiza los resultados
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm

# Asume que 'model' es tu modelo HMM ya entrenado y 'X' son tus datos
model = hmm.GaussianHMM(n_components=3, covariance_type="full")  # reemplaza esto con tu modelo real
model.fit(X)  # y tus datos reales

# Calcula las probabilidades de los estados ocultos para cada observación
hidden_states = model.predict(X)
hidden_probs = model.predict_proba(X)

# Crea una figura y un conjunto de subgráficos
fig, axs = plt.subplots(model.n_components, sharex=True, sharey=True)

# Para cada estado oculto
for i, (ax, color) in enumerate(zip(axs, plt.cm.viridis(np.linspace(0, 1, model.n_components)))):
    # Encuentra las observaciones que fueron asignadas a este estado
    mask = hidden_states == i

    # Traza las probabilidades para estas observaciones
    ax.plot(hidden_probs[mask, i], ".", c=color)

    # Añade etiquetas, etc.
    ax.set_title(f"Estado oculto {i+1}")
    ax.set_ylabel("Probabilidad")
    ax.set_xlabel("Tiempo")

# Muestra la figura
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt

# Graficar las secuencias de observaciones originales
plt.figure(figsize=(10, 6))
plt.plot(observations[0], label='Observaciones Variable 1', color='b')  # Reemplaza 'observations[0]' con tus observaciones reales
plt.title('Secuencias de Observaciones - Variable 1')
plt.xlabel('Hora del Día')
plt.ylabel('Valor')
plt.legend()
plt.show()

# Graficar los resultados del modelo HMM
hidden_states = model.predict(observations[0].reshape(-1, 1))  # Reformatea las observaciones a una matriz 2D
plt.figure(figsize=(10, 6))
plt.plot(hidden_states, label='Estados Ocultos', color='r', marker='o', linestyle='None')
plt.title('Asignación de Estados Ocultos - Variable 1')
plt.xlabel('Muestra')
plt.ylabel('Estado Oculto')
plt.legend()
plt.show()