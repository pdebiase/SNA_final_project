# Importing packages
import numpy as np
import pandas as pd
import networkx as nx
from functools import reduce
import operator
from random import choice
import pickle
import time
import os

### CSV READING AND NETWORK CREATION ### 

def edgelist_csv_to_graph(filename="./data/2tvshow_edges.csv"):
    '''
    Converts a .csv file in edgelist format to a networkX graph. 
    :param filename: relative path to the csv file
    :return G: Returns a networkx undirected graph object
    '''

    df = pd.read_csv(filename, sep=";")
    G = nx.from_pandas_edgelist(df, source="Source", target="Target")
    del df
    return G

### OUTBREAK GENERATOR ### 
def simulate_outbreak_inverted_index(G, init_nodes=[], p=0.05, n_runs=10):
    '''
    Simulates an outbreak, either from a random node or a prespecified set of nodes.
    :param G: networkx graph object to use as network
    :param initial_infected nodes: list of nodes to start the outbreak from, if empty choose random node
    :param n_runs: how many outbreaks to simulate
    :return all_runs_list: returns a list of lists, where each 
                            inner list is a list of infected nodes resulting from that run
    '''
    
    # List with all runs output
    all_runs_dicts = []
    # Run the algorithm 'n_runs' times
    for run in range(n_runs):
        outbreak_dict = dict()
        initial_infected_nodes = []
        # Using a fixed p or sampling from a 20-60 distribution
        if p==False:
            prob = np.random.uniform(20,60,1)[0]/100
        else:
            prob = p

        if init_nodes==[]:
            initial_infected_nodes = [choice(list(G.nodes()))]
            
        else:
            initial_infected_nodes = init_nodes

        # Random seed equals to run so we always can recover the same output
        # np.random.seed(run)
        # Nodes that are infecting other nodes in this time step
        transmissible_nodes = initial_infected_nodes
        # Nodes that become infected in this time step - at start, by default, none
        just_infected = []
        # History of all nodes that become infected - at the start just the the initial nodes
        [outbreak_dict.update({node:0}) for node in initial_infected_nodes]
        # The algorithm runs when there is at least one trasmissible node
        i = 1
        all_infected = [initial_infected_nodes]
        while transmissible_nodes:
            # For each node recently infected we are going to check its neighbors and infect new nodes with probability p
            for n in transmissible_nodes:
                current_neighbors = list(G.neighbors(n))
                infection = np.random.uniform(0,1,len(current_neighbors)) < prob
                just_infected += list(np.extract(infection, current_neighbors))
            # Now the recent infected become the trasmissible nodes (only if they were not infected before)
            transmissible_nodes = list(set(just_infected) - set(reduce(operator.concat, all_infected)))
            # And they are added to the list with the history of all nodes infected
#             all_infected.extend([transmissible_nodes])
            [outbreak_dict.update({node:i}) for node in transmissible_nodes]
            all_infected.extend([transmissible_nodes])
            i += 1
        # Removing the last blank element (the last element is always a blank list)
        all_infected = all_infected[:-1]
        # Appending t the list with the output from all runs
        output = (outbreak_dict, all_infected)
        all_runs_dicts.append(output)

    return all_runs_dicts

### RUNNING FOR ALL FIVE FILES### 

#folders

path = "C:\\Users\\pvbia\\EPA - Delft\\2o Year\\Social Network\\Final Project\\SNA_final_project (v optimized)"
os.chdir(path)
os.getcwd()


def main():
    np.random.seed(1874)
    file_names = [["1jazz_outbreaks.data", "./data/1jazz_edges.csv"],
                  ["2tvshow_outbreaks.data","./data/2tvshow_edges.csv"],
                  ["3politician_outbreaks.data","./data/3politician_edges.csv"],
                  ["4public_figure_outbreaks.data","./data/4public_figure_edges.csv"],
                  ["5new_sites_outbreaks.data","./data/5new_sites_edges.csv"]
#                  ,
#                  ["6artist_outbreaks.data","./data/6artist_edges.csv"],
#                  ["7livemocha_outbreaks.data","./data/7livemocha_edges.csv"]
                 ]

    for f in file_names:
        G = edgelist_csv_to_graph(f[1])
        t_start = time.time()
        outbreak = simulate_outbreak_inverted_index(G=G, init_nodes=[], p=0.05, n_runs=10000)
        with open(f[0], 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(outbreak, filehandle)
        print("Simulated outbreaks for "+str(f[1])+" in "+str(time.time()-t_start))

        del G
if __name__ == '__main__':
    main()
