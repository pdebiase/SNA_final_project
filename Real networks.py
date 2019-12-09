# Importing packages\import os
import os
path = "C:\\Users\\pvbia\\EPA - Delft\\2o Year\\Social Network\\Final Project\\SNA_final_project (v optimized)"
os.chdir(path)
import numpy as np
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

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



file_names = [["1jazz_outbreaks.data", "./data/1jazz_edges.csv","Musician Network"],
              ["2tvshow_outbreaks.data","./data/2tvshow_edges.csv","TV Show Network"],
              ["3politician_outbreaks.data","./data/3politician_edges.csv","Politician Network"],
              ["4public_figure_outbreaks.data","./data/4public_figure_edges.csv","Public Figure Network"],
              ["5new_sites_outbreaks.data","./data/5new_sites_edges.csv","News Site Network"]
             ]

## Density
for i in file_names:
    print(i[1])
    print(nx.density(edgelist_csv_to_graph(i[1])))


## Degree

def plot_degree_dist(Network, degree_type=None, title = None):
    if degree_type=="in":
        degrees = [Network.in_degree(node) for node in Network.nodes()]
    if degree_type=="out":    
        degrees = [Network.out_degree(node) for node in Network.nodes()]
    if degree_type==None:
        degrees = [Network.degree(node) for node in Network.nodes()]
    # Plotting
    #sns.distplot(degrees,kde=False, bins=np.unique(degrees))
    sns.distplot(degrees,kde=False)
    # Adding legend
    plt.gca().set(title=title, ylabel='frequency (log scale)', xlabel='degree')
    plt.yscale('log''', nonposy='clip''')
    # Showing the graph
    plt.show()
    
for i in file_names:
    a = edgelist_csv_to_graph(i[1])
    print(i[1])
    plot_degree_dist(a)

## Components


def number_components(network):
    return len(list(nx.weakly_connected_components(network)))

        # Geetting the list with all strngly connected components
        #list_with_strongly_connected_components = list(nx.strongly_connected_components(network))
            # Removing the values that has only themselves as components
        #for element in list_with_strongly_connected_components.copy():
        #    if len(element)==1:
        #        list_with_strongly_connected_components.remove(element)
        #return len(list_with_strongly_connected_components)


def number_nodes_and_edges_components(network):
    biggest_component = max(nx.weakly_connected_components(network),key=len)
    return len(biggest_component)

for i in file_names:
    med_net = edgelist_csv_to_graph(i[1])
    med_net = med_net.to_directed()
    print(i[1])

    print("There are " + str(number_components(med_net)) + " WEAKLY connected components in the network")
    print("There are " + str(number_nodes_and_edges_components(med_net)) + " nodes in the biggest component")
   
    
def diagram_distance_distribution(network):
    biggest_component_set = max(nx.weakly_connected_components(network),key=len)
    # Getting the network from the bigest weakly component
    network2 = network.copy()
    for node in network2.nodes():
        if node not in biggest_component_set:
            network.remove_node(node)
    # Creating the tupple with (node,dic) where the dic has all the path distances to this node
    paths_generator = nx.shortest_path_length(network)
    # Creating an empty counter to sum all the counter's values
    C = Counter()
    # Looping through all dic with all paths
    for dic in paths_generator:
        # Adding the values for each node
        C += Counter(dic[1].values())
    # Removing the paths with 0 distance
    C_no_zero = {k:v for k,v in C.items() if k != 0}
    # Getting the relative frequency
    total = sum(C_no_zero.values())
    list_final_distribution_per_node_no_zero = {k:(v/total) for k,v in C_no_zero.items()}
    # Plotting 
    labels, values = zip(*list_final_distribution_per_node_no_zero.items())
    plt.bar(labels,values)
    plt.xticks(np.arange(min(labels), max(labels)+1, 1.0))
    # Adding legend
    plt.gca().set(ylabel='frequency', xlabel='distance')
    plt.show()

for i in file_names:
    med_net = edgelist_csv_to_graph(i[1])
    med_net = med_net.to_directed()
    print(i[1])

    plot_title="Distance distribution for largest " + i[2] 
    diagram_distance_distribution(med_net)
    
#med_net = edgelist_csv_to_graph(file_names[4][1])
#med_net = med_net.to_directed()
#print(i[1])
#
#plot_title="Distance distribution for largest " + i[2] 
#diagram_distance_distribution(med_net,plot_title=plot_title)
    
   
## Clustering coefficient
for i in file_names:
    print(i[1])
    print(nx.average_clustering(edgelist_csv_to_graph(i[1])))


