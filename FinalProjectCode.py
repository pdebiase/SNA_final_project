# Importing packages
import numpy as np
import pandas as pd
#import time
import networkx as nx
from functools import reduce
import operator
import math

############################################ DATA PREPARATION ############################################

# Reading a dataframe
df = pd.read_csv("./data/5livemocha.csv",sep=";")
# Creating a network
G = nx.from_pandas_edgelist(df, source="Source", target="Target")
# Creating the outbreak generator

############################################ Outbreak Function ############################################
#The output is a list in which each element i is the set of nodes that was infected at time step i.
def outbreak(G,initial_infected_nodes,p=0.5,runs=10):
    # List with all runs output
    all_runs_list = []
    # Run the algorithm 'runs' times
    for run in range(runs):
        # Random seed equals to run so we always can recover the same output
        np.random.seed(run)
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
                infection = np.random.uniform(0,1,len(list(G.neighbors(n)))) < p
                just_infected += list(np.extract(infection, list(G.neighbors(n))))
            # Now the recent infected become the trasmissible nodes (only if they were not infected before)
            transmissible_nodes = list(set(just_infected) - set(reduce(operator.concat, all_infected)))
            # And they are added to the list with the history of all nodes infected
            all_infected.extend([transmissible_nodes])
        # Removing the last blank element (the last element is always a blank list)
        all_infected = all_infected[:-1]
        # Appending t the list with the output from all runs
        all_runs_list.append(all_infected)

    return all_runs_list


# Creating outbreak simulations
initial_infected_nodes = [1]
outbreak_simulations = outbreak(G,initial_infected_nodes,p=0.5,runs=10)

########################################## Criteria Computation ##########################################
    
###### Detection Likelihood (DL)

#Fraction of information cascades and contamination events detected by the selected nodes
def DL(outbreak_simulations, placement):
    detection_count = 0
    # For each run we need to compute the detection likelihood
    for run in outbreak_simulations:
        # If any node in the placement got infeceted then we detected the outbreak
        if list(set(placement) & set(reduce(operator.concat, run))):
            detection_count += 1
    # We need the detection likelihood thus the number of detection divded by the total number of simulations
    return detection_count/len(outbreak_simulations)

### Testing
# Calculating the DL
placement = [112394,22310]
print('DL')
print(DL(outbreak_simulations, placement))

    ###### Detection time (DT)
    
#Measures the time passed from outbreak till detection by one of the selected nodes
def DT(outbreak_simulations, placement, max_penalty=math.inf):
    # Output is a list with the time step in which the outbreak was detected for each run
    output = []
    # Creating a set for the placement
    set_placement = set(placement)
    # For each run we need to compute the detection time
    for run in outbreak_simulations:
        # If any node in the placement got infeceted then we detected the outbreak and we need to check the detection time
        intersection = list(set_placement & set(reduce(operator.concat, run)))
        if intersection:
            # For each step and nodes infected in this step we are going to check if the placement detected it
            for step,nodes in enumerate(run):
                # If any element in the intersection is in this set of nodes, than it was detected at this time step
                if list(set(intersection) & set(nodes)):
                    output.append(step)
                    break
        # If not detected, than the detection time is the max penalty
        else:
            output.append(max_penalty)
    return output

### Testing
    # Calculating the DT
placement = [112394,22310]
print('DT')
print(DT(outbreak_simulations, placement))

    ###### Population affected (PA)
    
def PA(outbreak_simulations, placement):
    # Output is a list with the population affected in each outbreak run
    output = []
    # Creating a set for the placement
    set_placement = set(placement)
    # For each run we need to compute the population affected
    for run in outbreak_simulations:
        pa = 0
        # If any node in the placement got infeceted then we detected the outbreak and we need to check the population affected
        intersection = list(set_placement & set(reduce(operator.concat, run)))
        if intersection:
            # For each step and nodes infected in this step we are going to check if the placement detected it
            for nodes in run:
                # If any element in the intersection is in this set of nodes, then it was detected at this time step
                # and we can finish by appending the population affected to the output and breaking the run
                if list(set(intersection) & set(nodes)):
                    output.append(pa)
                    break
                else:
                # If not, then we need to sum the non-detected nodes to the pop affected
                    pa += len(nodes)
        # If not detected, than the pop affected is the size of the outbreak
        else:
            output.append(len(reduce(operator.concat, run)))
    return output

### Testing
    # Calculating the PA
placement = [112394,22310]
print("PA")
print(PA(outbreak_simulations, placement))