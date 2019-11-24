# Importing packages
import numpy as np
import pandas as pd
import networkx as nx
from functools import reduce
import operator
from random import choice
import pickle
from multiprocessing import Pool
import functools

### CSV READING AND NETWORK CREATION ### 

def edgelist_csv_to_graph(filename="./data/1jazz_edges.csv"):
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
def simulate_outbreak(G,run, init_nodes=[], p=False):
    
    # Run the algorithm 'n_runs' times
    np.random.seed(run)
    initial_infected_nodes = []
    
    # Using a fixed p or sampling from a 1-10 distribution
    if p==False:
        prob = np.random.uniform(1,10,1)[0]/100
    else:
        prob = p
    # Getting initial notes
    if init_nodes==[]:
        initial_infected_nodes = [choice(list(G.nodes()))]
    else:
        initial_infected_nodes = init_nodes

    # Nodes that are infecting other nodes in this time step
    transmissible_nodes = initial_infected_nodes
    # Nodes that become infected in this time step - at start, by default, none
    just_infected = []
    # History of all nodes that become infected - at the start just the the initial nodes
    all_infected = [initial_infected_nodes]
    # The algorithm runs when there is at least one trasmissible node
    while transmissible_nodes:
        # For each node recently infected we are going to check its neighbors and infect new nodes with probability p
        for n in transmissible_nodes:
            infection = np.random.uniform(0,1,len(list(G.neighbors(n)))) < prob
            just_infected += list(np.extract(infection, list(G.neighbors(n))))
        # Now the recent infected become the trasmissible nodes (only if they were not infected before)
        transmissible_nodes = list(set(just_infected) - set(reduce(operator.concat, all_infected)))
        # And they are added to the list with the history of all nodes infected
        all_infected.extend([transmissible_nodes])
    # Removing the last blank element (the last element is always a blank list)
    all_infected = all_infected[:-1]

    return all_infected


def simulate_outbreaks(G, init_nodes=[], p=False, n_runs=10):
    '''
    Simulates an outbreak, either from a random node or a prespecified set of nodes.
    :param G: networkx graph object to use as network
    :param initial_infected nodes: list of nodes to start the outbreak from, if empty choose random node
    :param n_runs: how many outbreaks to simulate
    :return all_runs_list: returns a list of lists, where each 
                            inner list is a list of infected nodes resulting from that run
    '''
    runs = list(range(n_runs))
    
    function = functools.partial(simulate_outbreak,G=G, init_nodes=init_nodes, p=p)
   
    if __name__ == '__main__':
        pool = Pool(6)
        results = pool.map(function, runs)    
    
    return results


### RUNNING FOR ALL FIVE FILES### 

file_names = [["1jazz_outbreaks.data", "./data/1jazz_edges.csv"],
              ["2tvshow_outbreaks.data","./data/2tvshow_edges.csv"],
              ["3politician_outbreaks.data","./data/3politician_edges.csv"],
              ["4public_figure_outbreaks.data","./data/4public_figure_edges.csv"],
              ["5new_sites_outbreaks.data","./data/5new_sites_edges.csv"]
             ]

for f in file_names:
    G = edgelist_csv_to_graph(f[1])
    outbreak = simulate_outbreaks(G, init_nodes=[], p=False, n_runs=10000)
    with open(f[0], 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(outbreak, filehandle)
        
        





