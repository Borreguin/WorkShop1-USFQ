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
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

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

def plot_heatmap(df: pd.DataFrame, variable: str,legend:str):

    # Reshape the dataframe to have hours of the day as columns and days as rows
    df.index = pd.to_datetime(df.index, dayfirst=True)
    df['week_of_year'] = df.index.isocalendar().week
    df['day_of_week'] = df.index.dayofweek
    df['hour_of_day'] = df.index.hour
    df['day_hour'] = df['day_of_week']*100 + df['hour_of_day']
    df_heatmap = df.pivot_table(index='week_of_year', columns='day_hour', values=variable)

    # Set the labels for x-axis and y-axis
    day_hours = [f"{hour}:00" if hour in [0, 6, 12, 18] else "" for day in range(7) for hour in range(24)]
    day_labels = [f"Day {day}" if hour == 0 else "" for day in range(7) for hour in range(24)]
    x_labels = [f"{day}\n{hour}" for day, hour in zip(day_labels, day_hours)]
    y_labels = [f"{i}" for i in df_heatmap.index]  # Create y-axis labels

    # Create the heatmap
    plt.figure(figsize=(30, 15))  # Increase the size of the heatmap
    ax = sns.heatmap(df_heatmap, cmap='YlOrRd', xticklabels=x_labels)  # Change the colormap to 'YlOrRd' for stronger colors
    ax.set_yticklabels(y_labels, rotation=0)  # Set y-axis labels and make them horizontal
    plt.xlabel('Day and Hour of the Week')
    plt.ylabel('Week of the Year')
    plt.title(f'Heatmap of {legend} over Time')
    plt.savefig(f'./images/{legend}_heatmap.png')
    plt.show()




def create_kmeans(df: pd.DataFrame, field: str, k: int = 2):
    X = df[[field]].values
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    df['cluster'] = kmeans.labels_
    return df


def elbow_method(df: pd.DataFrame, field: str, k_max: int = 10):

    # Initialize lists to store the sum of squared distances for each k
    sse = []

    # Iterate over different values of k
    for k in range(1, k_max+1):
        # Create KMeans object and fit the data
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(df[[field]].values)

        # Calculate the sum of squared distances for the current k
        sse.append(kmeans.inertia_)

    # Plot the elbow curve
    plt.plot(range(1, k_max+1), sse, marker='o')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Sum of Squared Distances')
    plt.title('Elbow Curve')
    plt.show()

def plot_clusters(df: pd.DataFrame, field: str,legend:str):

    # Get the number of clusters from the dataframe
    k = df['cluster'].nunique()

    # Reshape the dataframe to have hours of the day as columns and days as rows
    df.index = pd.to_datetime(df.index, dayfirst=True)
    df['week_of_year'] = df.index.isocalendar().week
    df['day_of_week'] = df.index.dayofweek
    df['hour_of_day'] = df.index.hour
    df['day_hour'] = df['day_of_week']*100 + df['hour_of_day']
    df_heatmap = df.pivot_table(index='week_of_year', columns='day_hour', values=field)

    # Set the labels for x-axis and y-axis
    day_hours = [f"{hour}:00" if hour in [0, 6, 12, 18] else "" for day in range(7) for hour in range(24)]
    day_labels = [f"Day {day}" if hour == 0 else "" for day in range(7) for hour in range(24)]
    x_labels = [f"{day}\n{hour}" for day, hour in zip(day_labels, day_hours)]
    y_labels = [f"{i}" for i in df_heatmap.index]  # Create y-axis labels

    # Create the heatmap
    fig,ax=plt.subplots(1,1,figsize=(30, 15))  # Increase the size of the heatmap
    ax = sns.heatmap(df_heatmap, cmap=['#0000FF', '#00FF00', '#FF0000', '#FFFF00', '#FF00FF'][:k], xticklabels=x_labels)  # Set custom colors for clusters
    ax.set_yticklabels(y_labels, rotation=0)  # Set y-axis labels and make them horizontal
    plt.xlabel('Day and Hour of the Week')
    plt.ylabel('Week of the Year')
    plt.title(f'Clustered Heatmap of {legend} over Time')

    plt.savefig(f'./images/{legend}_clustered_heatmap.png')
    plt.show()


def plot_data_by_day(_df: pd.DataFrame, lb1, lb2, legend):
    df_to_plot = _df.tail(1000)
    plt.plot(df_to_plot.index, df_to_plot[lb1], label=alias[lb_V005_vent01_CO2])
    plt.plot(df_to_plot.index, df_to_plot[lb2], label=alias[lb_V022_vent02_CO2])
    plt.xlabel(lb_timestamp)
    plt.ylabel(legend)
    plt.legend()
    plt.show()


#create a funcion that take a dataframe, group the timestamp column by day and hour then iterate the plot for each day in the same graph (one graph per day)
def plot_data_by_day_and_hour(_df: pd.DataFrame, lb: str, legend: str,line_color: str = 'blue', alpha: float = 0.1):

    # Tomamos las últimas 1000 observaciones para el gráfico
    df_to_plot = _df

    # Extrayendo la hora del índice
    df_to_plot['hour'] = df_to_plot.index.hour

    # Agrupando los datos por fecha y hora
    df_to_plot = df_to_plot.groupby([df_to_plot.index.date, 'hour']).mean()
    df_to_plot = df_to_plot.reset_index()

    # Calculando el promedio para cada hora a lo largo de todos los días
    avg_per_hour = df_to_plot.groupby('hour')[lb].mean()
    # Creando la figura y los ejes para el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    # Iterando sobre cada día único para graficar
    unique_days = df_to_plot['level_0'].unique()
    for day in unique_days:
        daily_data = df_to_plot[df_to_plot['level_0'] == day]
        ax.plot(daily_data['hour'], daily_data[lb], color=line_color, alpha=alpha)

    ax.plot(avg_per_hour.index, avg_per_hour, color='red', label='Promedio por hora', linewidth=2,linestyle='--')
    # Configurando la leyenda y los ejes

    # Configurando las marcas del eje X para que muestren todas las horas
    ax.set_xticks(range(24))  # Establece marcas en cada hora
    ax.set_xticklabels([f'{hour}:00' for hour in range(24)], rotation=45)

    ax.set_xlabel('Hora')
    ax.set_ylabel(legend)
    # No añadimos la leyenda ya que todas las líneas son del mismo color y no hay distinción entre los días
    plt.savefig(f'./images/{legend}_diario.png')
    # No añadimos la leyenda ya que todas las líneas son del mismo color y no hay distinción entre los días

    plt.show()


def plot_all_unique_variables(_df,plotfunc,*args,**kwargs):
    columns_to_plot = {column:name for column,name in alias.items() if column != lb_timestamp}
    for lb,legend in columns_to_plot.items():
        plotfunc(_df,lb,legend,*args,**kwargs)

# create a function that scale the data using standarscaler method
def normalize_z_score(_df: pd.DataFrame) -> pd.DataFrame:
    # Calculando la media y la desviación estándar para cada columna
    mean = _df.mean()
    std = _df.std()
    # Aplicando la normalización Z-score
    df_norm = (_df - mean) / std

    return df_norm

def normalize_robust_scaler(_df: pd.DataFrame) -> pd.DataFrame:
    # Creando el objeto para normalizar con RobustScaler
    scaler = RobustScaler()
    # Aplicando la normalización
    df_norm = scaler.fit_transform(_df)
    df_norm = pd.DataFrame(df_norm, columns=_df.columns, index=_df.index)
    return df_norm

def make_kmeans_clustering(_df: pd.DataFrame, n_clusters: int):
    # Creando el objeto para KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    # Ajustando el modelo
    kmeans.fit(_df)
    # Prediciendo las etiquetas
    labels = kmeans.predict(_df)

    return labels




def plot_clusters_3d_hour(data, label_x, label_y, title):
    data['hour'] = data.index.hour
    data['cluster'] = data['cluster'].astype('category')

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(data['hour'],  data[label_x], data[label_y], c=data['cluster'] , alpha=0.1)

    ax.set_xlabel('Hour of Day')
    ax.set_ylabel(alias[label_x])
    ax.set_zlabel(alias[label_y])
    ax.set_title(title)

    categories = np.unique(data['cluster'])
    colors = [plt.cm.viridis(data['cluster'].cat.codes.unique()[i] / (len(categories) - 1)) for i in
              range(len(categories))]

    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=category,
                                  markerfacecolor=color, markersize=10) for category, color in zip(categories, colors)]

    ax.legend(handles=legend_elements, title="Cluster")

    # def init():
    #     return fig,
    #
    # def rotate(angle):
    #     ax.view_init(azim=angle)
    #     return fig,
    #
    # rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 360, 10), init_func=init, interval=100,
    #                                         blit=True)
    # # Guardando la animación
    # rot_animation.save(f'./images/Cluster_{label_x}_vs_{label_y}_hour.gif', dpi=60, writer='pillow', fps=5)

    plt.show()



def plot_clusters_3d_weekday(data, label_x, label_y, title):
    # Mapear el día de la semana a un valor numérico (0 = Lunes, 6 = Domingo)
    data['weekday'] = data.index.dayofweek
    data['cluster'] = data['cluster'].astype('category')

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Graficar los puntos
    scatter = ax.scatter(data['weekday'],  data[label_x], data[label_y], c=data['cluster'] , alpha=0.1)

    # Añadir etiquetas y título
    ax.set_xlabel('Day of Week (0=Monday, 6=Sunday)')
    ax.set_ylabel(alias[label_x])
    ax.set_zlabel(alias[label_y])
    ax.set_title(title)

    # Añadir una barra de color para los clusters
    # colorbar = fig.colorbar(scatter, ax=ax)
    # colorbar.set_label('Cluster')

    categories = np.unique(data['cluster'])
    colors = [plt.cm.viridis(data['cluster'].cat.codes.unique()[i] / (len(categories) - 1)) for i in
              range(len(categories))]

    # Crea elementos de leyenda
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=category,
                                  markerfacecolor=color, markersize=10) for category, color in zip(categories, colors)]

    # Añade la leyenda al gráfico
    ax.legend(handles=legend_elements, title="Cluster")

    # def init():
    #     return fig,
    #
    # def rotate(angle):
    #     ax.view_init(azim=angle)
    #     return fig,
    #
    # rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 360, 10), init_func=init, interval=100,
    #                                         blit=True)
    # # Guardando la animación
    # rot_animation.save(f'./images/Cluster_{label_x}_vs_{label_y}_weekday.gif', dpi=60, writer='pillow', fps=5)

    plt.show()



def plot_weekday_cycle(data, label_temp, label_CO2):
    # Asignar día de la semana a cada timestamp
    data['day_of_week'] = data.index.day_name()
    data['hour_of_day'] = data.index.hour
    # Ordenar los días de la semana
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data['day_of_week'] = pd.Categorical(data['day_of_week'], categories=weekdays, ordered=True)

    # Agrupar por día de la semana y hora para calcular el promedio
    weekday_cycle = data.groupby(['day_of_week', 'hour_of_day']).mean().reset_index()

    # Crear la figura
    fig, axes = plt.subplots(7, 1, figsize=(15, 20), sharex=True)

    for i, day in enumerate(weekdays):
        ax1 = axes[i]
        ax2 = ax1.twinx()

        ax1.plot(weekday_cycle[weekday_cycle['day_of_week'] == day]['hour_of_day'],
                 weekday_cycle[weekday_cycle['day_of_week'] == day][label_temp],
                 color='tab:red', label='Temperature')
        ax1.set_ylabel(alias[label_temp], color='tab:red')
        ax1.tick_params(axis='y', labelcolor='tab:red')

        ax2.plot(weekday_cycle[weekday_cycle['day_of_week'] == day]['hour_of_day'],
                 weekday_cycle[weekday_cycle['day_of_week'] == day][label_CO2],
                 color='tab:blue', label='CO2')
        ax2.set_ylabel(alias[label_CO2], color='tab:blue')
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        ax1.set_title(day)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

    plt.xlabel('Hour of Day')
    fig.text(0.04, 0.5, 'Values', va='center', rotation='vertical')
    plt.tight_layout()
    plt.savefig(f'./images/{alias[label_CO2]}_vs_{alias[label_temp]}_weekday_cycle.png')
    plt.show()


def multivariable_analisis(_df,lb1,lb2):
    df_to_use = _df.copy(deep=True)
    plot_weekday_cycle(df_to_use, lb1,lb2)

    df_pair_cols = df_to_use[[lb1,lb2]].copy(deep=True)
    df_norm = normalize_robust_scaler(df_pair_cols)
    pca = PCA(n_components=1)
    df_to_use['PCA'] = pca.fit_transform(df_norm)

    # _df['cluster'] = make_kmeans_clustering(df_norm, 3)
    # plot_clusters_3d_weekday(_df, lb1, lb2, f'KMeans Clustering {alias[lb1]} vs {alias[lb2]}')
    df_to_use['cluster'] = make_kmeans_clustering(np.array(df_to_use['PCA']).reshape(-1, 1), 2)
    plot_clusters_3d_weekday(df_to_use, lb1, lb2, f'KMeans Clustering {alias[lb1]} vs {alias[lb2]}')
    plot_clusters_3d_hour(df_to_use, lb1, lb2, f'KMeans Clustering {alias[lb1]} vs {alias[lb2]}')



def univariable_experiment(_df):
    df_to_use=_df.copy(deep=True)
    columns_to_plot= {column:name for column,name in alias.items() if column != lb_timestamp}

    for lb,legend in columns_to_plot.items():
        plot_data_by_day_and_hour(df_to_use, lb, legend)
        plot_heatmap(df_to_use,lb,legend)
        df_kmeans = create_kmeans(df_to_use, lb, 3)
        plot_clusters(df_kmeans, lb, legend)


if __name__ == "__main__":
    # multivariable_analisis(df,lb_V005_vent01_CO2,lb_V006_vent01_temp_out)
    df = prepare_data()
    df.index = pd.to_datetime(df.index, dayfirst=True)


    # univariable_experiment(df)
    multivariable_analisis(df,lb_V005_vent01_CO2,lb_V006_vent01_temp_out)
    multivariable_analisis(df, lb_V022_vent02_CO2, lb_V023_vent02_temp_out)


