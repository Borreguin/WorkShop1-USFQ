import os
import numpy as np
from hmmlearn import hmm
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
    #df = prepare_data()
    #plot_data(df, lb_V005_vent01_CO2, lb_V022_vent02_CO2, "CO2")
    #plot_data(df, lb_V006_vent01_temp_out, lb_V023_vent02_temp_out, "Temperature")
    simple_hmm_example()