import os
import matplotlib.pyplot as plt
from datetime import time
import seaborn as sns
from sklearn.cluster import KMeans
from p1_uml_util import *



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
        sns.boxplot(x=df_to_plot[lb_timestamp].dt.hour, y=variable, data=df_to_plot, showfliers=False, color=(i/24, 0.5, 1/(i+1)))
        plt.ylim(y_min, y_max) 
        plt.xlabel("")
        
        plt.ylabel("")
        
    plt.title(legend)
    plt.tight_layout()  # Ajusta el diseño de los subplots para evitar superposiciones
    plt.show()  # Mostrar el gráfico


def plot_data_correlation(_df: pd.DataFrame, variable, i: int):
    n = 0
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')
    
    for x in range(i,i+5):
        df_to_plot_x=_df[_df[lb_timestamp].dt.hour == x]
        for y in range(i,i+5):
            df_to_plot_y=_df[_df[lb_timestamp].dt.hour == y]
            n += 1
            plt.subplot(5, 5, n)
            plt.subplots_adjust(hspace=0.5, wspace=0.5)
            sns.regplot(x=df_to_plot_x[variable], y=df_to_plot_y[variable]) # regression plot
            #plt.ylabel(y.split()[0] + ' ' + y.split()[1] if len(y.split()) > 1 else y)
            plt.xlabel("")
            plt.ylabel("")

    plt.title(f"hours correlation: {i} hasta {(i+5)}")        
    plt.tight_layout()  # Ajusta el diseño de los subplots para evitar superposiciones
        
    plt.show()  # Mostrar el gráfico

def kmeans_clustering (_df: pd.DataFrame, variable):
    df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], format='%d.%m.%Y %H:%M')

    caracteristicas = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    X = iris[caracteristicas]
    y = iris["species"]
    g = sns.pairplot(X, kind="reg", vars=caracteristicas)
    km = KMeans(n_clusters = 3, n_jobs = 4, random_state=21)
    km.fit(X)
    sns.pairplot(iris[["sepal_length", "sepal_width"] + ["species"]], hue="species",height=2)
    
if __name__ == "__main__":
    df = prepare_data()
    #plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    #plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
    plot_data_ejercicio1(df, lb_V006_vent01_temp_out, "CO2")
    
    plot_data_correlation(df,lb_V006_vent01_temp_out,10)
    #kmeans_clustering (df,lb_V005_vent01_CO2)

