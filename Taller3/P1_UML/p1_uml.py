import os
from .p1_uml_util import *
import matplotlib.pyplot as plt
from datetime import time
import seaborn as sns
from sklearn.cluster import KMeans
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import skfuzzy as fuzz
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from scipy.cluster import vq

def prepare_data():
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_path, "data")
    file_path = os.path.join(data_path, "data.csv")
    _df = read_csv_file(file_path)
    
    #_df.set_index(lb_timestamp, inplace=True)

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

def plot_data_ejercicio1(_df: pd.DataFrame, variable, legend):
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    y_min = _df[variable].min()
    y_max = _df[variable].max()
    for i in range(24):
        df_to_plot=_df[_df[lb_timestamp].dt.hour == i]
        print(df_to_plot)
        plt.subplot(1, 24, i+1)
        #plt.plot(df_to_plot.index, df_to_plot[variable], label=f"{i}:00 h")
        sns.boxplot(x=df_to_plot[lb_timestamp].dt.time, y=variable, data=df_to_plot, showfliers=False, color=(i/24, 0.5, 1/(i+1)))
        plt.ylim(y_min, y_max) 
        plt.xlabel("")
        
        plt.ylabel("")
        
    plt.title(legend)
    plt.tight_layout()  # Ajusta el diseño de los subplots para evitar superposiciones
    plt.show()  # Mostrar el gráfico

def plot_data_ejercicio1_b(_df: pd.DataFrame, variable):
    # Convert timestamp to datetime
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    
    # Extract hour of day and day of week from timestamp
    _df['hour'] = _df[lb_timestamp].dt.hour
    _df['day'] = _df[lb_timestamp].dt.dayofweek

    # Group by day
    grouped = _df.groupby('day')

    for day, group in grouped:
        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=5)
        group['kmeans_cluster'] = kmeans.fit_predict(group[[variable]])

        # Perform Fuzzy C-means clustering
        fcm = fuzz.cmeans(group[[variable]].T, c=5, m=2, error=0.005, maxiter=1000)
        group['fcm_cluster'] = np.argmax(fcm[1], axis=0)

        # Perform anomaly detection with Isolation Forest
        isolation_forest = IsolationForest(contamination='auto')
        group['anomaly'] = isolation_forest.fit_predict(group[[variable]])

        # Plot clusters
        plt.figure(figsize=(10, 5))
        plt.scatter(range(len(group[group['kmeans_cluster'] == 0])), group[group['kmeans_cluster'] == 0][variable], color='blue')
        plt.scatter(range(len(group[group['kmeans_cluster'] == 1])), group[group['kmeans_cluster'] == 1][variable], color='red')
        plt.scatter(range(len(group[group['kmeans_cluster'] == 2])), group[group['kmeans_cluster'] == 2][variable], color='yellow')
        plt.scatter(range(len(group[group['kmeans_cluster'] == 3])), group[group['kmeans_cluster'] == 3][variable], color='green')
        plt.scatter(range(len(group[group['kmeans_cluster'] == 4])), group[group['kmeans_cluster'] == 4][variable], color='black')
        # Plot anomalies
        plt.scatter(range(len(group[group['anomaly'] == -1])), group[group['anomaly'] == -1][variable], color='orange')
        plt.title(f"Day {day+1} for {variable}")
        plt.tight_layout()
        plt.show()
        
        plt.figure(figsize=(10, 5))
        plt.scatter(range(len(group[group['fcm_cluster'] == 0])), group[group['fcm_cluster'] == 0][variable], color='lightblue')
        plt.scatter(range(len(group[group['fcm_cluster'] == 1])), group[group['fcm_cluster'] == 1][variable], color='red')
        plt.scatter(range(len(group[group['fcm_cluster'] == 2])), group[group['fcm_cluster'] == 2][variable], color='yellow')
        plt.scatter(range(len(group[group['fcm_cluster'] == 3])), group[group['fcm_cluster'] == 3][variable], color='green')
        plt.scatter(range(len(group[group['fcm_cluster'] == 4])), group[group['fcm_cluster'] == 4][variable], color='cyan')
        # Plot anomalies
        plt.scatter(range(len(group[group['anomaly'] == -1])), group[group['anomaly'] == -1][variable], color='orange')
        
        plt.title(f"Day {day+1} for {variable}")
        plt.tight_layout()
        plt.show()
    
def plot_data_ejercicio1_d(_df: pd.DataFrame, variable1, variable2):
    # Convert timestamp to datetime
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    
    # Extract hour of day and day of week from timestamp
    _df['hour'] = _df[lb_timestamp].dt.hour
    _df['day'] = _df[lb_timestamp].dt.dayofweek

    # Group by day
    grouped = _df.groupby('day')

    for day, group in grouped:
        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=5)
        group['kmeans_cluster'] = kmeans.fit_predict(group[[variable1, variable2]])

        # Perform Fuzzy C-means clustering
        fcm = fuzz.cmeans(group[[variable1, variable2]].T, c=5, m=2, error=0.005, maxiter=1000)
        group['fcm_cluster'] = np.argmax(fcm[1], axis=0)

        # Perform anomaly detection with Isolation Forest
        isolation_forest = IsolationForest(contamination='auto')
        group['anomaly'] = isolation_forest.fit_predict(group[[variable1, variable2]])

        # Plot clusters
        plt.figure(figsize=(10, 5))
        plt.scatter(group[variable1][group['kmeans_cluster'] == 0], group[variable2][group['kmeans_cluster'] == 0], color='blue')
        plt.scatter(group[variable1][group['kmeans_cluster'] == 1], group[variable2][group['kmeans_cluster'] == 1], color='red')
        plt.scatter(group[variable1][group['kmeans_cluster'] == 2], group[variable2][group['kmeans_cluster'] == 2], color='yellow')
        plt.scatter(group[variable1][group['kmeans_cluster'] == 3], group[variable2][group['kmeans_cluster'] == 3], color='green')
        plt.scatter(group[variable1][group['kmeans_cluster'] == 4], group[variable2][group['kmeans_cluster'] == 4], color='black')
        # Plot anomalies
        plt.scatter(group[variable1][group['anomaly'] == -1], group[variable2][group['anomaly'] == -1], color='orange')
        plt.title(f"Day {day+1} for {variable1} and {variable2}")
        plt.tight_layout()
        plt.show()
        
        plt.figure(figsize=(10, 5))
        plt.scatter(group[variable1][group['fcm_cluster'] == 0], group[variable2][group['fcm_cluster'] == 0], color='blue')
        plt.scatter(group[variable1][group['fcm_cluster'] == 1], group[variable2][group['fcm_cluster'] == 1], color='red')
        plt.scatter(group[variable1][group['fcm_cluster'] == 2], group[variable2][group['fcm_cluster'] == 2], color='yellow')
        plt.scatter(group[variable1][group['fcm_cluster'] == 3], group[variable2][group['fcm_cluster'] == 3], color='green')
        plt.scatter(group[variable1][group['fcm_cluster'] == 4], group[variable2][group['fcm_cluster'] == 4], color='black')
        # Plot anomalies
        plt.scatter(group[variable1][group['anomaly'] == -1], group[variable2][group['anomaly'] == -1], color='orange')
        plt.title(f"Day {day+1} for {variable1} and {variable2}")
        plt.tight_layout()
        plt.show()
    
if __name__ == "__main__":
    df = prepare_data()
    #plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    #plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
    
    # plot for each variable hourly graph
    # plot_data_ejercicio1(df, lb_V005_vent01_CO2,  "CO2")
    # plot_data_ejercicio1(df, lb_V022_vent02_CO2,  "CO2")
    # plot_data_ejercicio1(df, lb_V006_vent01_temp_out, "Temperature")
    # plot_data_ejercicio1(df, lb_V023_vent02_temp_out, "Temperature")
    
    
    # plots for each variable with clustering and anomaly detection
    # plot_data_ejercicio1_b(df, lb_V005_vent01_CO2)
    # plot_data_ejercicio1_b(df, lb_V022_vent02_CO2)
    # plot_data_ejercicio1_b(df, lb_V006_vent01_temp_out)
    plot_data_ejercicio1_b(df, lb_V023_vent02_temp_out)
    
    #  plot for 2 co2 variables
    # plot_data_ejercicio1_d(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2)
    
    #  plot for 2 temperature variables
    # plot_data_ejercicio1_d(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out)