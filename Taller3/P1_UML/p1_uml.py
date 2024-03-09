import os
from Taller3.P1_UML.p1_uml_util import *
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

def prepare_data():
    # Asumiendo que lb_timestamp es el nombre de la columna de timestamps en tu CSV
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
    df_to_plot = _df.tail(1000)
    plt.plot(df_to_plot.index, df_to_plot[lb1], label=alias[lb_V005_vent01_CO2])
    plt.plot(df_to_plot.index, df_to_plot[lb2], label=alias[lb_V022_vent02_CO2])
    plt.xlabel(lb_timestamp)
    plt.ylabel(legend)
    plt.legend()
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

    plt.show()
    # No añadimos la leyenda ya que todas las líneas son del mismo color y no hay distinción entre los días

    plt.show()

def plot_boxplot_by_hour(_df: pd.DataFrame, lb: str, legend: str):

    # Tomamos las últimas 1000 observaciones para el gráfico
    df_to_plot = _df.tail(1000)

    # Extrayendo la hora del índice
    df_to_plot['hour'] = df_to_plot.index.hour

    # Preparando los datos para el gráfico de caja
    data_to_plot = [df_to_plot[df_to_plot['hour'] == hour][lb] for hour in range(24)]

    # Creando la figura y los ejes para el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    # Creando el gráfico de caja
    ax.boxplot(data_to_plot, notch=True, patch_artist=True)

    # Configurando los ejes
    ax.set_xlabel('Hora')
    ax.set_ylabel(lb)
    ax.set_xticklabels(range(24))
    ax.set_title(f'Distribución de {legend} por hora del día')

    plt.grid(True)
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


def group_df_by_day(_df: pd.DataFrame):
    # Agrupando los datos por día
    df_by_day = _df.resample('D').mean()
    return df_by_day


def plot_multivariable_analisis(_df: pd.DataFrame, lb1: str, lb2: str):
    # Creando la figura y los ejes para el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    # Graficando los datos
    ax.scatter(_df[lb1], _df[lb2], c=_df['cluster'], cmap='viridis', s=50, alpha=0.5)

    # Configurando los ejes
    ax.set_xlabel(alias[lb1])
    ax.set_ylabel(alias[lb2])

    plt.show()


def multivariable_analisis(_df,lb1,lb2):
    # df = prepare_data()
    df_norm = normalize_z_score(_df[[lb1,lb2]])
    _df['cluster'] = make_kmeans_clustering(df_norm, 2)
    plot_multivariable_analisis(_df,)


def alternative_main():
    df = prepare_data()
    plot_all_unique_variables(df,plot_boxplot_by_hour)
    plot_all_unique_variables(df,plot_data_by_day_and_hour,line_color='blue',alpha=0.1)


if __name__ == "__main__":

    # multivariable_analisis(df,lb_V005_vent01_CO2,lb_V006_vent01_temp_out)