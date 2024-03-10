import os
from calendar import calendar

from matplotlib import pyplot as plt

from Taller3.P1_UML.p1_uml_util import *


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



if __name__ == "__main__":
    df = prepare_data()
    #plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    #plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")

df = prepare_data()
# Normalizo los datos para que estén en el rango [0, 1]
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)


# Elimino los NaNs
df_normalized.dropna(inplace=True)

# Hago un KMeans con 2 clusters entre la temperatura y el CO2 de la ventilación NE
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(df_normalized[[lb_V005_vent01_CO2, lb_V006_vent01_temp_out]])
df_normalized['cluster'] = kmeans.labels_



# Hago un KMeans con 2 clusters entre la temperatura y el CO2 de la ventilación SW
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(df_normalized[[lb_V022_vent02_CO2, lb_V023_vent02_temp_out]])
df_normalized['cluster'] = kmeans.labels_



# el index le convierte en columna
df_normalized.reset_index(inplace=True)
# veo el tipo de datos

# La columna timestamp la convierto de object a timestamp
df_normalized[lb_timestamp] = pd.to_datetime(df_normalized[lb_timestamp])

# Creo la columna de día de la semana
import calendar
df_normalized['day_of_week'] = df_normalized[lb_timestamp].dt.dayofweek
# convierto el día de la semana en el nombre del día
df_normalized['day_of_week'] = df_normalized['day_of_week'].apply(lambda x: calendar.day_name[x])


# Creo la columna de hora
df_normalized['hour'] = df_normalized[lb_timestamp].dt.hour
# observo el dataframe


# Creo la columna semana del año

df_normalized['week_of_year'] = df_normalized[lb_timestamp].dt.isocalendar().week

# Creo un grafico de las lineas de tiempo de CO2 y temperatura de la ventilación NE
import seaborn as sns
plt.figure(figsize=(15, 5))
sns.lineplot(data=df_normalized, x=lb_timestamp, y=lb_V005_vent01_CO2, label=alias[lb_V005_vent01_CO2])
sns.lineplot(data=df_normalized, x=lb_timestamp, y=lb_V006_vent01_temp_out, label=alias[lb_V006_vent01_temp_out])
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.title('CO2 and Temperature of Ventilation NE')
plt.show()
