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

from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

def plot_data_ejercicio1b(_df: pd.DataFrame, variable, legend):
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    _df['day'] = _df[lb_timestamp].dt.day

    unique_days = _df['day'].unique()

    for day in unique_days:
        df_to_plot=_df[_df['day'] == day]

        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=24)
        df_to_plot['kmeans_cluster'] = kmeans.fit_predict(df_to_plot[[variable]])

        # Perform Fuzzy C-means clustering
        data_2d = df_to_plot[variable].values.reshape(-1, 1).T  # reshape the data to 2D
        fcm = fuzz.cmeans(data_2d, c=24, m=2, error=0.005, maxiter=1000)
        df_to_plot['fcm_cluster'] = np.argmax(fcm[1], axis=0)

        # Perform anomaly detection with Isolation Forest
        isolation_forest = IsolationForest(contamination='auto')
        df_to_plot['anomaly'] = isolation_forest.fit_predict(df_to_plot[[variable]])

        # Plot clusters
        for i in range(10):
            plt.figure(figsize=(10, 5))
            plt.scatter(range(len(df_to_plot[df_to_plot['kmeans_cluster'] == i])), df_to_plot[df_to_plot['kmeans_cluster'] == i][variable], color='blue')
            plt.scatter(len(df_to_plot[df_to_plot['kmeans_cluster'] == i])//2, kmeans.cluster_centers_[i], color='red')  # plot the KMeans centroid
            plt.scatter(range(len(df_to_plot[df_to_plot['fcm_cluster'] == i])), df_to_plot[df_to_plot['fcm_cluster'] == i][variable], color='green')
            plt.scatter(len(df_to_plot[df_to_plot['fcm_cluster'] == i])//2, fcm[0][i], color='black')  # plot the FCM centroid
            plt.title(f"Cluster {i+1} for {variable} on day {day}")
            plt.tight_layout()
            plt.show()

        # Plot anomalies
        plt.figure(figsize=(10, 5))
        plt.scatter(df_to_plot[df_to_plot['anomaly'] == -1][variable].index, df_to_plot[df_to_plot['anomaly'] == -1][variable], color='orange')  # plot the anomalies
        plt.title(f"Anomalies for {variable} on day {day}")
        plt.tight_layout()
        plt.show()
        
        
def plot_data_ejercicio1_b(_df: pd.DataFrame, variable):
    # Convert timestamp to datetime
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    
    # Extract hour of day and day of week from timestamp
    _df['hour'] = _df[lb_timestamp].dt.hour
    _df['day'] = _df[lb_timestamp].dt.dayofweek

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=24)
    _df['kmeans_cluster'] = kmeans.fit_predict(_df[[variable]])

    # Perform Fuzzy C-means clustering
    fcm = fuzz.cmeans(_df[[variable]].T, c=24, m=2, error=0.005, maxiter=1000)
    _df['fcm_cluster'] = np.argmax(fcm[1], axis=0)

    # Perform anomaly detection with Isolation Forest
    isolation_forest = IsolationForest(contamination='auto')
    _df['anomaly'] = isolation_forest.fit_predict(_df[[variable]])

    # Plot clusters
    for i in range(24):
        plt.figure(figsize=(10, 5))
        plt.scatter(range(len(_df[_df['kmeans_cluster'] == i])), _df[_df['kmeans_cluster'] == i][variable], color='blue')
        plt.scatter(len(_df[_df['kmeans_cluster'] == i])//2, kmeans.cluster_centers_[i], color='red')  # plot the KMeans centroid
        plt.scatter(range(len(_df[_df['fcm_cluster'] == i])), _df[_df['fcm_cluster'] == i][variable], color='green')
        plt.scatter(len(_df[_df['fcm_cluster'] == i])//2, fcm[0][i], color='black')  # plot the FCM centroid
        plt.title(f"Cluster {i+1} for {variable}")
        plt.tight_layout()
        plt.show()

    # Plot anomalies
    plt.figure(figsize=(10, 5))
    plt.scatter(_df[_df['anomaly'] == -1][variable].index, _df[_df['anomaly'] == -1][variable], color='orange')  # plot the anomalies
    plt.title(f"Anomalies for {variable}")
    plt.tight_layout()
    plt.show()

    # Perform time series decomposition
    # _df.set_index(lb_timestamp, inplace=True)
    # result = seasonal_decompose(_df[variable], model='additive', period=24)
    # result.plot()
    # plt.title(f"Time Series Decomposition for {variable}")
    # plt.show()
    
def plot_data_ejercicio1_d(_df: pd.DataFrame, variable1, variable2):
    # Convert timestamp to datetime
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    
    # Extract hour of day and day of week from timestamp
    _df['hour'] = _df[lb_timestamp].dt.hour
    _df['day'] = _df[lb_timestamp].dt.dayofweek

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=1)
    _df['kmeans_cluster'] = kmeans.fit_predict(_df[[variable1, variable2]])

    # Perform Fuzzy C-means clustering
    fcm = fuzz.cmeans(_df[[variable1, variable2]].T, c=1, m=2, error=0.005, maxiter=1000)
    _df['fcm_cluster'] = np.argmax(fcm[1], axis=0)

    # Perform anomaly detection with Isolation Forest
    isolation_forest = IsolationForest(contamination='auto')
    _df['anomaly'] = isolation_forest.fit_predict(_df[[variable1, variable2]])

    # Plot clusters
    for i in range(1):  # change this to match the number of clusters
        plt.figure(figsize=(10, 5))
        plt.scatter(_df[_df['kmeans_cluster'] == i][variable1], _df[_df['kmeans_cluster'] == i][variable2], color='blue')
        plt.scatter(kmeans.cluster_centers_[i, 0], kmeans.cluster_centers_[i, 1], color='red')  # plot the KMeans centroid
        plt.scatter(_df[_df['fcm_cluster'] == i][variable1], _df[_df['fcm_cluster'] == i][variable2], color='green')
        plt.scatter(fcm[0][i, 0], fcm[0][i, 1], color='black')  # plot the FCM centroid
        plt.title(f"Cluster {i+1} for {variable1} and {variable2}")
        plt.tight_layout()
        plt.show()

    # Plot anomalies
    plt.figure(figsize=(10, 5))
    plt.scatter(_df[_df['anomaly'] == -1][variable1], _df[_df['anomaly'] == -1][variable2], color='orange')  # plot the anomalies
    plt.title(f"Anomalies for {variable1} and {variable2}")
    plt.tight_layout()
    plt.show()

    # Perform time series decomposition
    # _df.set_index(lb_timestamp, inplace=True)
    # for variable in [variable1, variable2]:
    #     result = seasonal_decompose(_df[variable], model='additive', period=24)
    #     result.plot()
    #     plt.title(f"Time Series Decomposition for {variable}")
    #     plt.show()
    
if __name__ == "__main__":
    df = prepare_data()
    #plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    #plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
    #plot_data_ejercicio1b(df, lb_V005_vent01_CO2, "CO2")
    # plot_data_ejercicio1_b(df, lb_V005_vent01_CO2)
    plot_data_ejercicio1_d(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2)
    