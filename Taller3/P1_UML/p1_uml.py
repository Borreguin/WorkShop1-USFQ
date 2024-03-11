import os
import seaborn as sns
from Taller3.P1_UML.p1_uml_util import *
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
def prepare_data():
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_path, "data")
    file_path = os.path.join(data_path, "data.csv")

    # Leyendo el archivo CSV
    _df = pd.read_csv(file_path, sep=';')

    # Asegurándonos de que lb_timestamp sea una columna y convertirla a datetime
    if lb_timestamp in _df.columns:
        _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp])
        _df.set_index(lb_timestamp, inplace=True)
    else:
        print(f"La columna {lb_timestamp} no se encuentra en el DataFrame.")

    _df.dropna(inplace=True)

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

# def plot_heatmap(df: pd.DataFrame, variable: str,legend:str):
#
#     # Reshape the dataframe to have hours of the day as columns and days as rows
#     df.index = pd.to_datetime(df.index, dayfirst=True)
#     df['week_of_year'] = df.index.isocalendar().week
#     df['day_of_week'] = df.index.dayofweek
#     df['hour_of_day'] = df.index.hour
#     df['day_hour'] = df['day_of_week']*100 + df['hour_of_day']
#     df_heatmap = df.pivot_table(index='week_of_year', columns='day_hour', values=variable)
#
#     # Set the labels for x-axis and y-axis
#     day_hours = [f"{hour}:00" if hour in [0, 6, 12, 18] else "" for day in range(7) for hour in range(24)]
#     day_labels = [f"Day {day}" if hour == 0 else "" for day in range(7) for hour in range(24)]
#     x_labels = [f"{day}\n{hour}" for day, hour in zip(day_labels, day_hours)]
#     y_labels = [f"{i}" for i in df_heatmap.index]  # Create y-axis labels
#
#     # Create the heatmap
#     plt.figure(figsize=(30, 15))  # Increase the size of the heatmap
#     ax = sns.heatmap(df_heatmap, cmap='YlOrRd', xticklabels=x_labels)  # Change the colormap to 'YlOrRd' for stronger colors
#     ax.set_yticklabels(y_labels, rotation=0)  # Set y-axis labels and make them horizontal
#     plt.xlabel('Day and Hour of the Week')
#     plt.ylabel('Week of the Year')
#     plt.title(f'Heatmap of {legend} over Time')
#     plt.savefig(f'./images/{legend}_heatmap.png')
#     plt.show()
#
#
#
# def create_kmeans(df: pd.DataFrame, field: str, k: int = 2):
#     X = df[[field]].values
#     kmeans = KMeans(n_clusters=k)
#     kmeans.fit(X)
#     df['cluster'] = kmeans.labels_
#     return df
#
#
# def elbow_method(df: pd.DataFrame, field: str, k_max: int = 10):
#
#     # Initialize lists to store the sum of squared distances for each k
#     sse = []
#
#     # Iterate over different values of k
#     for k in range(1, k_max+1):
#         # Create KMeans object and fit the data
#         kmeans = KMeans(n_clusters=k)
#         kmeans.fit(df[[field]].values)
#
#         # Calculate the sum of squared distances for the current k
#         sse.append(kmeans.inertia_)
#
#     # Plot the elbow curve
#     plt.plot(range(1, k_max+1), sse, marker='o')
#     plt.xlabel('Number of Clusters (k)')
#     plt.ylabel('Sum of Squared Distances')
#     plt.title('Elbow Curve')
#     plt.show()
#
# def plot_clusters(df: pd.DataFrame, field: str,legend:str):
#
#     # Get the number of clusters from the dataframe
#     k = df['cluster'].nunique()
#
#     # Reshape the dataframe to have hours of the day as columns and days as rows
#     df.index = pd.to_datetime(df.index, dayfirst=True)
#     df['week_of_year'] = df.index.isocalendar().week
#     df['day_of_week'] = df.index.dayofweek
#     df['hour_of_day'] = df.index.hour
#     df['day_hour'] = df['day_of_week']*100 + df['hour_of_day']
#     df_heatmap = df.pivot_table(index='week_of_year', columns='day_hour', values=field)
#
#     # Set the labels for x-axis and y-axis
#     day_hours = [f"{hour}:00" if hour in [0, 6, 12, 18] else "" for day in range(7) for hour in range(24)]
#     day_labels = [f"Day {day}" if hour == 0 else "" for day in range(7) for hour in range(24)]
#     x_labels = [f"{day}\n{hour}" for day, hour in zip(day_labels, day_hours)]
#     y_labels = [f"{i}" for i in df_heatmap.index]  # Create y-axis labels
#
#     # Create the heatmap
#     plt.figure(figsize=(30, 15))  # Increase the size of the heatmap
#     ax = sns.heatmap(df_heatmap, cmap=['#0000FF', '#00FF00', '#FF0000', '#FFFF00', '#FF00FF'][:k], xticklabels=x_labels)  # Set custom colors for clusters
#     ax.set_yticklabels(y_labels, rotation=0)  # Set y-axis labels and make them horizontal
#     plt.xlabel('Day and Hour of the Week')
#     plt.ylabel('Week of the Year')
#     plt.title(f'Clustered Heatmap of {legend} over Time')
#     plt.savefig(f'./images/{legend}_clustered_heatmap.png')
#     plt.show()
#
#
# def plot_data_by_day(_df: pd.DataFrame, lb1, lb2, legend):
#     df_to_plot = _df.tail(1000)
#     plt.plot(df_to_plot.index, df_to_plot[lb1], label=alias[lb_V005_vent01_CO2])
#     plt.plot(df_to_plot.index, df_to_plot[lb2], label=alias[lb_V022_vent02_CO2])
#     plt.xlabel(lb_timestamp)
#     plt.ylabel(legend)
#     plt.legend()
#     plt.show()
#
#
# #create a funcion that take a dataframe, group the timestamp column by day and hour then iterate the plot for each day in the same graph (one graph per day)
# def plot_data_by_day_and_hour(_df: pd.DataFrame, lb: str, legend: str,line_color: str = 'blue', alpha: float = 0.1):
#
#     # Tomamos las últimas 1000 observaciones para el gráfico
#     df_to_plot = _df
#
#     # Extrayendo la hora del índice
#     df_to_plot['hour'] = df_to_plot.index.hour
#
#     # Agrupando los datos por fecha y hora
#     df_to_plot = df_to_plot.groupby([df_to_plot.index.date, 'hour']).mean()
#     df_to_plot = df_to_plot.reset_index()
#
#     # Calculando el promedio para cada hora a lo largo de todos los días
#     avg_per_hour = df_to_plot.groupby('hour')[lb].mean()
#     # Creando la figura y los ejes para el gráfico
#     fig, ax = plt.subplots(figsize=(12, 6))
#
#     # Iterando sobre cada día único para graficar
#     unique_days = df_to_plot['level_0'].unique()
#     for day in unique_days:
#         daily_data = df_to_plot[df_to_plot['level_0'] == day]
#         ax.plot(daily_data['hour'], daily_data[lb], color=line_color, alpha=alpha)
#
#     ax.plot(avg_per_hour.index, avg_per_hour, color='red', label='Promedio por hora', linewidth=2,linestyle='--')
#     # Configurando la leyenda y los ejes
#
#     # Configurando las marcas del eje X para que muestren todas las horas
#     ax.set_xticks(range(24))  # Establece marcas en cada hora
#     ax.set_xticklabels([f'{hour}:00' for hour in range(24)], rotation=45)
#
#     ax.set_xlabel('Hora')
#     ax.set_ylabel(legend)
#     # No añadimos la leyenda ya que todas las líneas son del mismo color y no hay distinción entre los días
#     plt.savefig(f'./images/{legend}_diario.png')
#     # No añadimos la leyenda ya que todas las líneas son del mismo color y no hay distinción entre los días
#
#     plt.show()
#
# def plot_boxplot_by_hour(_df: pd.DataFrame, lb: str, legend: str):
#
#     # Tomamos las últimas 1000 observaciones para el gráfico
#     df_to_plot = _df.tail(1000)
#
#     # Extrayendo la hora del índice
#     df_to_plot['hour'] = df_to_plot.index.hour
#
#     # Preparando los datos para el gráfico de caja
#     data_to_plot = [df_to_plot[df_to_plot['hour'] == hour][lb] for hour in range(24)]
#
#     # Creando la figura y los ejes para el gráfico
#     fig, ax = plt.subplots(figsize=(12, 6))
#
#     # Creando el gráfico de caja
#     ax.boxplot(data_to_plot, notch=True, patch_artist=True)
#
#     # Configurando los ejes
#     ax.set_xlabel('Hora')
#     ax.set_ylabel(lb)
#     ax.set_xticklabels(range(24))
#     ax.set_title(f'Distribución de {legend} por hora del día')
#
#     plt.grid(True)
#     plt.show()
#
#
# def plot_all_unique_variables(_df,plotfunc,*args,**kwargs):
#     columns_to_plot = {column:name for column,name in alias.items() if column != lb_timestamp}
#     for lb,legend in columns_to_plot.items():
#         plotfunc(_df,lb,legend,*args,**kwargs)
#
# # create a function that scale the data using standarscaler method
# def normalize_z_score(_df: pd.DataFrame) -> pd.DataFrame:
#     # Calculando la media y la desviación estándar para cada columna
#     mean = _df.mean()
#     std = _df.std()
#     # Aplicando la normalización Z-score
#     df_norm = (_df - mean) / std
#
#     return df_norm
#
# def normalize_robust_scaler(_df: pd.DataFrame) -> pd.DataFrame:
#     # Creando el objeto para normalizar con RobustScaler
#     scaler = RobustScaler()
#     # Aplicando la normalización
#     df_norm = scaler.fit_transform(_df)
#     df_norm = pd.DataFrame(df_norm, columns=_df.columns, index=_df.index)
#     return df_norm
#
# def make_kmeans_clustering(_df: pd.DataFrame, n_clusters: int):
#     # Creando el objeto para KMeans
#     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#     # Ajustando el modelo
#     kmeans.fit(_df)
#     # Prediciendo las etiquetas
#     labels = kmeans.predict(_df)
#
#     return labels
#
#
# def group_df_by_day(_df: pd.DataFrame):
#     # Agrupando los datos por día
#     df_by_day = _df.resample('D').mean()
#     return df_by_day
#
# def plot_heatmap_multivariable(_df: pd.DataFrame, lb1: str, lb2: str, legend1: str, legend2: str):
#     # Creando la figura y los ejes para el gráfico
#     fig, ax = plt.subplots(figsize=(12, 6))
#
#     # Creando el gráfico de dispersión
#     h = ax.hist2d(_df[lb1], _df[lb2], bins=(50, 50), cmap='viridis')
#
#     # Configurando los ejes y la barra de colores
#     ax.set_xlabel(legend1)
#     ax.set_ylabel(legend2)
#     plt.colorbar(h[3], ax=ax)
#
#     plt.show()
#
# def plot_multivariable_analisis(_df: pd.DataFrame, lb1: str, lb2: str):
#     # Creando la figura y los ejes para el gráfico
#     fig, ax = plt.subplots(figsize=(12, 6))
#
#     # Graficando los datos
#     ax.scatter(_df[lb1], _df[lb2], c=_df['cluster'], cmap='viridis', s=50, alpha=0.5)
#
#     # Configurando los ejes
#     ax.set_xlabel(alias[lb1])
#     ax.set_ylabel(alias[lb2])
#
#     plt.show()
#
#
# def multivariable_analisis(_df,lb1,lb2):
#     # df = prepare_data()
#     df_norm = normalize_z_score(_df[[lb1,lb2]])
#     _df['cluster'] = make_kmeans_clustering(df_norm, 3)
#     plot_dtw_analysis_cluster(_df, lb1, lb2, 'cluster')
#
# def plot_dtw_analysis_cluster(_df, label1, label2, cluster_col):
#     # Verificar que las etiquetas y la columna de cluster existan en el DataFrame
#
#     # Calculando la distancia DTW entre las series temporales de las etiquetas especificadas
#     distance, path = fastdtw(_df[label1].values, _df[label2].values, dist=euclidean)
#
#     # Imprimir la distancia DTW
#     print(f"DTW distance between {label1} and {label2}: {distance}")
#
#     # Preparar los datos para la visualización del camino DTW
#     x_coords, y_coords = zip(*path)
#
#     # Crear la figura para el gráfico
#     plt.figure(figsize=(12, 6))
#
#     # Obtener los clusters únicos
#     clusters = _df[cluster_col].unique()
#
#     # Graficar una línea por cada cluster
#     for cluster in clusters:
#         cluster_indices = _df[_df[cluster_col] == cluster].index
#         plt.plot(np.array(x_coords)[cluster_indices], np.array(y_coords)[cluster_indices], '-', linewidth=2,
#                  label=f'Cluster {cluster}')
#
#     # Añadir etiquetas y título al gráfico
#     plt.xlabel(label1)
#     plt.ylabel(label2)
#     plt.title(f'DTW Path between {label1} and {label2}')
#     plt.legend()
#     plt.show()
# def plot_dtw_analisis(_df,cluster_col):
#     # Define the time series data
#     time_series_1 = df[['V005_vent01_CO2', 'V006_vent01_temp_out']]
#     time_series_2 = df[['V022_vent02_CO2', 'V023_vent02_temp_out']]
#
#     # Calculate the DTW distance between the time series data
#     distance_1, path_1 = fastdtw(time_series_1.values, time_series_2.values, dist=euclidean)
#     distance_2, path_2 = fastdtw(time_series_2.values, time_series_2.values, dist=euclidean)
#
#     # Print the DTW distances
#     print(f"DTW distance between V005_vent01_CO2 and V006_vent01_temp_out: {distance_1}")
#     print(f"DTW distance between V022_vent02_CO2 and V023_vent02_temp_out: {distance_2}")
#
#     # Separate the x and y coordinates
#     x_coords, y_coords = zip(*path_1)
#
#     # Plot the DTW path
#     plt.figure(figsize=(12, 6))
#     plt.plot(x_coords, y_coords, 'b-', linewidth=2)
#     plt.xlabel('V005_vent01_CO2')
#     plt.ylabel('V006_vent01_temp_out')
#     plt.title('DTW Path between V005_vent01_CO2 and V006_vent01_temp_out')
#     plt.show()

#
# def alternative_main():
#     df = prepare_data()
#     df.fillna(method='ffill', inplace=True) # los valores de NaN se reemplazan por el valor anterior
#     # plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
#     # plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
#
# def univariable_experiment(_df):
#     columns_to_plot= {column:name for column,name in alias.items() if column != lb_timestamp}
#
#     for lb,legend in columns_to_plot.items():
#         plot_data_by_day_and_hour(_df, lb, legend)
#         plot_heatmap(_df,lb,legend)
#         df_kmeans = create_kmeans(_df, lb, 3)
#         plot_clusters(df_kmeans, lb, legend)
#
#
# def plot_data_by_day_2(_df: pd.DataFrame, lb1, lb2, legend1, legend2):
#     # Asumiendo que las últimas 1000 filas son las que quieres graficar
#     df_to_plot = _df.tail(1000)
#
#     # Creando la figura y los ejes
#     fig, ax1 = plt.subplots(figsize=(20, 6))
#
#     # Graficando la primera serie de datos con el eje Y izquierdo
#     color = 'tab:blue'
#     ax1.set_xlabel('Timestamp')
#     ax1.set_ylabel(legend1, color=color)
#     ax1.plot(df_to_plot.index, df_to_plot[lb1], label=lb1, color=color)
#     ax1.tick_params(axis='y', labelcolor=color)
#
#     # Creando un segundo eje Y para la segunda serie de datos
#     ax2 = ax1.twinx()
#     color = 'tab:red'
#     ax2.set_ylabel(legend2, color=color)
#     ax2.plot(df_to_plot.index, df_to_plot[lb2], label=lb2, color=color)
#     ax2.tick_params(axis='y', labelcolor=color)
#
#     # Mostrando las leyendas
#     fig.tight_layout()
#     ax1.legend(loc='upper left')
#     ax2.legend(loc='upper right')
#
#     plt.show()


def multivariable():
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA


    df = prepare_data()
    df.fillna(method='ffill', inplace=True)
    # Convierte el indice en columnas
    df.reset_index(inplace=True)
    # Crea una columna con el día de la semana
    df['dia_semana'] = df[lb_timestamp].dt.dayofweek
    # Crea una columna con la hora del día
    df['hora'] = df[lb_timestamp].dt.hour
    # Al día de la semana le doy nombre
    df['dia_semana'] = df['dia_semana'].map({0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves',
                                                     4: 'Viernes', 5: 'Sabado', 6: 'Domingo'})
    #Creo una columna dia laborable o no con cero y uno
    df['dia_laborable'] = df['dia_semana'].map({'Lunes': 1, 'Martes': 1, 'Miercoles': 1, 'Jueves': 1,
                                                       'Viernes': 1, 'Sabado': 0, 'Domingo': 0})
    # Obtengo el aniomesdia de la fecha
    df['aniomesdia'] = df[lb_timestamp].dt.strftime('%Y-%m-%d')
    # Creo una columna con el número de semana
    df['semana'] = df[lb_timestamp].dt.isocalendar().week



if __name__ == "__main__":
    # multivariable_analisis(df,lb_V005_vent01_CO2,lb_V006_vent01_temp_out)
    df = prepare_data()
    # univariable_experiment(df)
    # multivariable_analisis(df,lb_V005_vent01_CO2,lb_V006_vent01_temp_out)
    multivariable()

