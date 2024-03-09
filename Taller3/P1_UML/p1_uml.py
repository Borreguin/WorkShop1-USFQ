import os
import seaborn as sns
import matplotlib.pyplot as plt
from p1_uml_util import *
from sklearn.cluster import KMeans

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

def plot_heatmap(df: pd.DataFrame, variable: str):
   
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
    plt.title(f'Heatmap of {variable} over Time')
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

def plot_clusters(df: pd.DataFrame, field: str):
       
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
    plt.figure(figsize=(30, 15))  # Increase the size of the heatmap
    ax = sns.heatmap(df_heatmap, cmap=['#0000FF', '#00FF00', '#FF0000', '#FFFF00', '#FF00FF'][:k], xticklabels=x_labels)  # Set custom colors for clusters
    ax.set_yticklabels(y_labels, rotation=0)  # Set y-axis labels and make them horizontal
    plt.xlabel('Day and Hour of the Week')
    plt.ylabel('Week of the Year')
    plt.title(f'Clustered Heatmap of {field} over Time')
    plt.show()


if __name__ == "__main__":
    df = prepare_data()
    df.fillna(method='ffill', inplace=True) # los valores de NaN se reemplazan por el valor anterior
    # plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    # plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")

    '''V005_vent01_CO2'''
    # Se realiza un plot para un a;o y observar el comportamiento general
    plot_heatmap(df, 'V005_vent01_CO2')
    # Se utiliza el método del codo para determinar el número de clusters
    elbow_method(df, 'V005_vent01_CO2', k_max=10)
    # Se realiza el clustering con k=3
    df_kmeans = create_kmeans(df, 'V005_vent01_CO2', 3)
    # Se realiza un plot para observar el comportamiento de los clusters
    plot_clusters(df_kmeans, 'V005_vent01_CO2')

    '''V022_vent02_CO2'''
    # Se realiza un plot para un a;o y observar el comportamiento general
    plot_heatmap(df, 'V022_vent02_CO2')
    # Se utiliza el método del codo para determinar el número de clusters
    elbow_method(df, 'V022_vent02_CO2', k_max=10)
    # Se realiza el clustering con k=3
    df_kmeans = create_kmeans(df, 'V022_vent02_CO2', 3)
    # Se realiza un plot para observar el comportamiento de los clusters
    plot_clusters(df_kmeans, 'V022_vent02_CO2')


    '''V006_vent01_temp_out'''
    # Se realiza un plot para un a;o y observar el comportamiento general
    plot_heatmap(df, 'V006_vent01_temp_out')
    # Se utiliza el método del codo para determinar el número de clusters
    elbow_method(df, 'V006_vent01_temp_out', k_max=10)
    # Se realiza el clustering con k=3
    df_kmeans = create_kmeans(df, 'V006_vent01_temp_out', 3)
    # Se realiza un plot para observar el comportamiento de los clusters
    plot_clusters(df_kmeans, 'V006_vent01_temp_out')


    '''V023_vent02_temp_out'''
    # Se realiza un plot para un a;o y observar el comportamiento general
    plot_heatmap(df, 'V023_vent02_temp_out')
    # Se utiliza el método del codo para determinar el número de clusters
    elbow_method(df, 'V023_vent02_temp_out', k_max=10)
    # Se realiza el clustering con k=3
    df_kmeans = create_kmeans(df, 'V023_vent02_temp_out', 3)
    # Se realiza un plot para observar el comportamiento de los clusters
    plot_clusters(df_kmeans, 'V023_vent02_temp_out')