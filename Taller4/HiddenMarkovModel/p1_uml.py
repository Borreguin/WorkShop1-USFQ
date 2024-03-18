import os
import numpy as np
from hmmlearn import hmm
#from Taller4.HiddenMarkovModel.p1_uml_util import *
from p1_uml_util import *
import matplotlib.pyplot as plt
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


#-------------------------------------------------------------------------------------------------#
# For simulations
def simul_kmeans_selection(n_sample = 24, plot_name = "test", title = ""):
    model = hmm.GaussianHMM(n_components=4, init_params="")
    model.n_features = 2
    model.startprob_ = np.array([1/4., 1/4., 1/4., 1/4.])
    model.transmat_ = np.array([[0.3, 0.4, 0.2, 0.1],
                                [0.1, 0.2, 0.3, 0.4],
                                [0.5, 0.2, 0.1, 0.2],
                                [0.25, 0.25, 0.25, 0.25]])
    model.means_ = np.array([[-2.5], [0], [2.5], [5.]])
    model.covars_ = np.sqrt([[0.25], [0.25], [0.25], [0.25]])


    X, y = model.sample(n_sample, random_state=1)

    inertias = []
    for k in range(1, 10 + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 10 + 1), inertias, marker='o', linestyle='--')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K:' + title)
    plt.xticks(range(1, 10 + 1))
    plt.grid(True)
    plt.savefig("./Taller4/HiddenMarkovModel/results/" + plot_name + ".png")
    plt.close()

    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(X)
    y_predicted = kmeans.predict(X)

    df = pd.DataFrame(X)
    df = df.rename(columns={0:"x"})
    df["y"] = y
    df["y_predicted"] = y_predicted
    df["t"] = [i for i in range(df.shape[0])]
    
    category_means = df.groupby('y')['x'].mean().reset_index()
    category_means['Rank'] = category_means['x'].rank(method='dense').astype(int) - 1
    category_mapping = dict(zip(category_means['y'], category_means['Rank']))
    df['y'] = df['y'].map(category_mapping)

    category_means = df.groupby('y_predicted')['x'].mean().reset_index()
    category_means['Rank'] = category_means['x'].rank(method='dense').astype(int) - 1
    category_mapping = dict(zip(category_means['y_predicted'], category_means['Rank']))
    df['y_predicted'] = df['y_predicted'].map(category_mapping)

    plt.figure()
    for i in range(4):
        plt.scatter(df.loc[(df["y"]==i),"t"].to_list(),df.loc[(df["y"]==i),"x"].to_list(), label = "s=" + str(i))
    plt.xlabel("Periodo Tiempo")
    plt.ylabel("y-value")
    plt.legend()
    plt.title("Estados Reales: "+ title)
    plt.savefig("./Taller4/HiddenMarkovModel/results/" + plot_name + "_simul_kmeans.png")
    plt.close()

    plt.figure()
    for i in range(4):
        plt.scatter(df.loc[(df["y_predicted"]==i),"t"].to_list(),df.loc[(df["y_predicted"]==i),"x"].to_list(), label = "s="+ str(i))
    plt.xlabel("Periodo Tiempo")
    plt.ylabel("y-value")
    plt.legend()
    plt.title("Estados Predichos, K-Means:" + title)
    plt.savefig("./Taller4/HiddenMarkovModel/results/" + plot_name + "_predicted_kmeans.png")
    plt.close()

    return np.mean(df["y_predicted"]==df["y"])


def simul_hmm(n_sample = 24, plot_name = "test", title = ""):
    model = hmm.GaussianHMM(n_components=4, init_params="")
    model.n_features = 2
    model.startprob_ = np.array([1/4., 1/4., 1/4., 1/4.])
    model.transmat_ = np.array([[0.3, 0.4, 0.2, 0.1],
                                [0.1, 0.2, 0.3, 0.4],
                                [0.5, 0.2, 0.1, 0.2],
                                [0.25, 0.25, 0.25, 0.25]])
    model.means_ = np.array([[-2.5], [0], [2.5], [5.]])
    model.covars_ = np.sqrt([[0.25], [0.25], [0.25], [0.25]])

    X, y = model.sample(n_sample, random_state=1)

    aic = []
    bic = []
    lls = []
    ns = range(2,11)
    for n in ns:
        best_ll = None
        best_model = None
        for i in range(10):
            h = hmm.GaussianHMM(n, n_iter=200, tol=1e-4, random_state=i)
            h.fit(X)
            score = h.score(X)
            if not best_ll or best_ll < best_ll:
                best_ll = score
                best_model = h
        aic.append(best_model.aic(X))
        bic.append(best_model.bic(X))
        lls.append(best_model.score(X))

    fig, ax = plt.subplots()
    ln1 = ax.plot(ns, aic, label="AIC", color="black", marker="o")
    ln2 = ax.plot(ns, bic, label="BIC", color="darkblue", marker="o")
    ax2 = ax.twinx()
    ln3 = ax2.plot(ns, lls, label="LL", color="darkred", marker="o")

    ax.legend(handles=ax.lines + ax2.lines)
    ax.set_title("Using AIC/BIC for Model Selection: " + title)
    ax.set_ylabel("Criterion Value (lower is better)")
    ax2.set_ylabel("LL (higher is better)")
    ax.set_xlabel("Number of HMM Components")
    fig.tight_layout()

    plt.savefig("./Taller4/HiddenMarkovModel/results/" + plot_name + ".png")
    plt.close()

    model = hmm.GaussianHMM(4, n_iter=200, tol=1e-4, random_state=1)
    model.fit(X)
    y_predicted = model.predict(X)

    df = pd.DataFrame(X)
    df = df.rename(columns={0:"x"})
    df["y"] = y
    df["y_predicted"] = y_predicted
    df["t"] = [i for i in range(df.shape[0])]
    
    category_means = df.groupby('y')['x'].mean().reset_index()
    category_means['Rank'] = category_means['x'].rank(method='dense').astype(int) - 1
    category_mapping = dict(zip(category_means['y'], category_means['Rank']))
    df['y'] = df['y'].map(category_mapping)

    category_means = df.groupby('y_predicted')['x'].mean().reset_index()
    category_means['Rank'] = category_means['x'].rank(method='dense').astype(int) - 1
    category_mapping = dict(zip(category_means['y_predicted'], category_means['Rank']))
    df['y_predicted'] = df['y_predicted'].map(category_mapping)

    plt.figure()
    for i in range(4):
        plt.scatter(df.loc[(df["y"]==i),"t"].to_list(),df.loc[(df["y"]==i),"x"].to_list(), label = "s=" + str(i))
    plt.xlabel("Periodo Tiempo")
    plt.ylabel("y-value")
    plt.legend()
    plt.title("Estados Reales: "+ title)
    plt.savefig("./Taller4/HiddenMarkovModel/results/" + plot_name + "_simul.png")
    plt.close()



    plt.figure()
    for i in range(4):
        plt.scatter(df.loc[(df["y_predicted"]==i),"t"].to_list(),df.loc[(df["y_predicted"]==i),"x"].to_list(), label = "s="+ str(i))
    plt.xlabel("Periodo Tiempo")
    plt.ylabel("y-value")
    plt.legend()
    plt.title("Estados Predichos, HMM:" + title)
    plt.savefig("./Taller4/HiddenMarkovModel/results/" + plot_name + "_predicted.png")
    plt.close()

    return np.mean(df["y_predicted"]==df["y"])

#-------------------------------------------------------------------------------------------------#
# Real Data


if __name__ == "__main__":
    df = prepare_data()
    #plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    #plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
    simple_hmm_example()

    #--------------------------------------------------------#
    # Simulations
    h1 = simul_hmm(n_sample = 24, plot_name = "hmm_simul_24n_1x", title = "24 muestras, 1 feature")
    h2 = simul_hmm(n_sample = 100, plot_name = "hmm_simul_100n_1x", title = "100 muestras, 1 feature")
    h3 = simul_hmm(n_sample = 300, plot_name = "hmm_simul_300n_1x", title = "300 muestras, 1 feature")
    h4 = simul_hmm(n_sample = 1000, plot_name = "hmm_simul_1000n_1x", title = "1000 muestras, 1 feature")
    accuracies = [h1,h2,h3,h4]
    df_res = pd.DataFrame({"n muestral":[24,100,300,1000],"accuracy":accuracies})
    df_res.to_markdown("./Taller4/HiddenMarkovModel/results/simul1_results.md")

    h1 = simul_kmeans_selection(n_sample = 24, plot_name = "kmeans_simul_24n_1x", title = "24 muestras, 1 feature")
    h2 = simul_kmeans_selection(n_sample = 100, plot_name = "kmeans_simul_100n_1x", title = "100 muestras, 1 feature")
    h3 = simul_kmeans_selection(n_sample = 300, plot_name = "kmeans_simul_300n_1x", title = "300 muestras, 1 feature")
    h4 = simul_kmeans_selection(n_sample = 1000, plot_name = "kmeans_simul_1000n_1x", title = "1000 muestras, 1 feature")
    accuracies = [h1,h2,h3,h4]
    df_res = pd.DataFrame({"n muestral":[24,100,300,1000],"accuracy":accuracies})
    df_res.to_markdown("./Taller4/HiddenMarkovModel/results/simul2_results.md")
    #--------------------------------------------------------#
    # Real Data