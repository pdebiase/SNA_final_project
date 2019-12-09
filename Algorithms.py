# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:07:31 2019

@authors: @pdebiase, @victorneuteboom
"""
import os
import numpy as np
import functools
import heapq 
import time
from networkx.algorithms.community import  greedy_modularity_communities
import networkx as nx
import copy
from random import choice, randint
import csv   

####################################### ALGORITHMS ###################################################################
def naive_greedy(outbreak_simulations, budget, eval_function, G):
    '''
    Using a naive greedy strategy: find the best placement, given outbreak simulation data and an objective function, constrained to a budget.
    :param outbreak_simulations: outbreak simulation data generated by simulate_outbreak
    :param budget: The total cost of selecting nodes cannot exceed the budget
    :param eval_function: Which objective function to use to calculate placement score
    :param G: networkx graph object to use as network
    :return placement: Return best found solution set of nodes
    
    '''
    eval_function = functools.partial(eval_function, outbreak_simulations=outbreak_simulations)
    nodes = list(G.nodes())
    n_nodes = len(nodes)
    fe_total = 0
    placement = []
    #Finding best placement
    for i in range(budget):
        t_iter = time.time()
        scores = []
        for n in nodes:
            placement.append(n)
            scores.append(eval_function(placement=placement))
            fe_total += 1
            placement.remove(n)
        best_node = nodes[np.argmin(scores)]
        placement.append(best_node)
        nodes.remove(best_node)

    return placement, eval_function(placement=placement), fe_total

def CELF(outbreak_simulations, budget, eval_function, G, verbosity = 2):
    '''
    Using the CELF algorithm: find the best placement, given outbreak simulation data and an objective function, constrained to a budget.
    :param outbreak_simulations: outbreak simulation data generated by simulate_outbreak
    :param budget: The total cost of selecting nodes cannot exceed the budget
    :param eval_function: Which objective function to use to calculate placement score
    :param G: networkx graph object to use as network
    :return placement: Return best found solution set of nodes
    '''
  
    fe_total = 0
    eval_function = functools.partial(eval_function, outbreak_simulations=outbreak_simulations)

    nodes = list(G.nodes())

    # Construct heap for first iteration of format (marginal gain, node)
    node_heap = []
    placement = []
    total_penalty = eval_function(placement = [])
    fe_total += 1
    for node in nodes:
        penalty = eval_function(placement = [node])
        marginal_gain = total_penalty - penalty
        # heapq implements a min heap, which keeps the smallest element at the top of the heap
        # but we need it the other way around, therefore we multiply the marginal_gain by -1
        heapq.heappush(node_heap, (-marginal_gain, node))
    
    fe_total += len(nodes)
    
    # Remove best node from heap and add to solution set
    best_gain, best_node = heapq.heappop(node_heap)
    total_penalty = total_penalty + best_gain
    placement.append(best_node)
 
    while len(placement) < budget:
        top_node_unchanged = False

        while not top_node_unchanged:
            _, current_node = heapq.heappop(node_heap)
            placement.append(current_node)
            current_penalty = eval_function(placement=placement)
            fe_total += 1
            placement.remove(current_node)
            marginal_gain = total_penalty - current_penalty

            # check if the previous top node stayed on the top after pushing
            # the marginal gain to the heap
            heapq.heappush(node_heap, (-marginal_gain, current_node))
            _, top_node = node_heap[0]
            
            if top_node == current_node:
                top_node_unchanged = True
            
        marginal_gain, current_node = heapq.heappop(node_heap)
        # marginal gain is stored as negative, so use plus instead of minus
        total_penalty = total_penalty + marginal_gain
     
        placement.append(current_node)

    return placement, eval_function(placement = placement), fe_total


def community_degree(outbreak_simulations, budget, eval_function, G, verbosity = 2):
    # Creating communities
    communities = greedy_modularity_communities(G,1)
    # Getting the degree distribution
    degree_distribution = nx.degree_centrality(G)
    # Creating a dictionary for each community with its centrality degree distribution
    community_list = []
    for c in communities:
        community_list.append({k: v for k, v in degree_distribution.items() if k in c})
    ## Selecting the placement
    b = 0
    index = 0
    placement = []
    n_communities = len(community_list)
    # Loop runs until there is no more budget
    while True:
        if b >= budget:
            break
        else:
            # Each node with max degree centrality is selected in each community from the biggest to shortest and repeat
            # until the budget is over
            c = (index + n_communities) % n_communities
            try :
                node = max(community_list[c], key=community_list[c].get)
                placement.append(node)
                del community_list[c][node]
                index += 1
                b += 1
            except:
                index += 1
    # Calculatinmg the score
    score = eval_function(outbreak_simulations=outbreak_simulations, placement=placement)
    return placement, score, 1

### Simulated Annealing - all functions below are used in the SA algorithm
def generate_initial_solution(nodes, budget):
    '''
    Creates a random solution of length budget
    '''
    placement = []
    for i in range(0, budget):
        node = nodes[randint(0,len(nodes)-1)]
#         nodes.remove(node)
        placement.append(node)
    return placement

def perturb(placement, nodes):
    '''
    Creates a neighbor solution by 
    randomly replacing a node from placement by a node from nodes
    '''
    to_replace = randint(0, len(placement)-1)
    replace_with = randint(0,len(nodes)-1)
    placement[to_replace] = nodes[replace_with]
    
    return placement

def SA(outbreak_simulations, budget, eval_function, G, t_start = 0.01, t_end = 0.00001, delta_t = 0.0001, n_perturbations = 100):
    '''
    Simulated annealing algorithm to determine the nodes that minimize the total penalty of the eval_function.
    '''
    fe_total = 0
    fe_best = 0
    nodes = list(G.nodes())
    placement = generate_initial_solution(nodes, budget)
    placement_score = eval_function(outbreak_simulations, placement)
    best_placement = placement
    best_score = placement_score
    t = t_start
    while(t > t_end):
        init_time = time.time()
        for i in range(0, n_perturbations):
            new_placement = perturb(copy.deepcopy(placement), nodes)
            new_placement_score = eval_function(outbreak_simulations, new_placement)
            delta_f = new_placement_score - placement_score
            fe_total += 1
            if delta_f <= 0:
                placement = new_placement
                placement_score = new_placement_score
            else:
                probability = np.exp(-delta_f / t)
                if np.random.uniform(0,1) < np.min([1.0, probability]):
                    placement = new_placement
                    placement_score = new_placement_score
             
            if(placement_score < best_score):
                best_placement = placement
                best_score = placement_score
                fe_best = fe_total
                
        t -= delta_t

    return best_placement, best_score, fe_best

def SA_cauchy(outbreak_simulations, budget, eval_function, G, t_start = 0.01, n_eval=10000, n_perturbations = 100):
    '''
    Simulated annealing algorithm to determine the nodes that minimize the total penalty of the eval_function.
    '''
    fe_total = 0
    fe_best = 0
    nodes = list(G.nodes())
    placement = generate_initial_solution(nodes, budget)
    placement_score = eval_function(outbreak_simulations, placement)
    best_placement = placement
    best_score = placement_score
    history = [placement_score]
    p_history = []
    b_history = [placement_score]
    t = t_start
    cur_iter=1
    while(cur_iter <= n_eval/n_perturbations):
        init_time = time.time()
        for i in range(0, n_perturbations):
            new_placement = perturb(copy.deepcopy(placement), nodes)
            new_placement_score = eval_function(outbreak_simulations, new_placement)
            delta_f = new_placement_score - placement_score
            fe_total += 1
            if delta_f <= 0:
                placement = new_placement
                placement_score = new_placement_score
            else:
                probability = np.exp(-delta_f / t)
                if np.random.uniform(0,1) < np.min([1.0, probability]):
                    placement = new_placement
                    placement_score = new_placement_score
             
            if(placement_score < best_score):
                best_placement = placement
                best_score = placement_score
                fe_best = fe_total

                
        t = t_start / cur_iter
        cur_iter += 1

    return best_placement, best_score, fe_best

def SA_geometric(outbreak_simulations, budget, eval_function, G, t_start=0.01, n_eval=10000, n_perturbations = 100, alpha = 0.95):
    '''
    Simulated annealing algorithm to determine the nodes that minimize the total penalty of the eval_function.
    '''
    fe_total = 0
    fe_best = 0
    nodes = list(G.nodes())
    placement = generate_initial_solution(nodes, budget)
    placement_score = eval_function(outbreak_simulations, placement)
    best_placement = placement
    best_score = placement_score

    t = t_start
    cur_iter=1
    while(cur_iter <= n_eval/n_perturbations):
        init_time = time.time()
        for i in range(0, n_perturbations):
            new_placement = perturb(copy.deepcopy(placement), nodes)
            new_placement_score = eval_function(outbreak_simulations, new_placement)
            delta_f = new_placement_score - placement_score
            fe_total += 1
            if delta_f <= 0:
                placement = new_placement
                placement_score = new_placement_score
            else:
                probability = np.exp(-delta_f / t)
                if np.random.uniform(0,1) < np.min([1.0, probability]):
                    placement = new_placement
                    placement_score = new_placement_score
             
            if(placement_score < best_score):
                best_placement = placement
                best_score = placement_score
                fe_best = fe_total
        
        t = t_start * (alpha ** cur_iter)
        cur_iter += 1

    return best_placement, best_score, fe_best

def SA_SASH(outbreak_simulations, budget, eval_function, G, t_start = 0.01, t_end = 0.00001, delta_t = 0.0001, n_perturbations = 100, verbosity = 2):
    '''
    Simulated annealing algorithm to determine the nodes that minimize the total penalty of the eval_function.
    '''
    
    init_time = time.time()
    nodes = list(G.nodes())
    scores = np.array([eval_function(outbreak_simulations, [node]) for node in nodes])
    placement = generate_initial_solution(nodes, budget)
    placement_score = eval_function(outbreak_simulations, placement)
    max_penalty = eval_function(outbreak_simulations, [])
    scores = scores - max_penalty
    best_placement = placement
    best_score = placement_score
    fe_total = 0
    fe_best = fe_total
    
    penalty_sum = np.sum(scores)
    p = [score / penalty_sum for score in scores]
    
    t = t_start
    # print("Initialisation took " + str(time.time()-init_time))
    while(fe_total < 9998):
        for i in range(0, n_perturbations):
            new_placement = SASH(G, copy.deepcopy(nodes), scores, copy.deepcopy(placement), p)
            new_placement_score = eval_function(outbreak_simulations, new_placement)
            fe_total += 1
            delta_f = new_placement_score - placement_score
            if delta_f <= 0:
                placement = new_placement
                placement_score = new_placement_score
            else:
                probability = np.exp(-delta_f / t)
#                 print("f: " + str(delta_f))
#                 print("p: "+ str(probability))
                if np.random.uniform(0,1) < np.min([1.0, probability]):
                    placement = new_placement
                    placement_score = new_placement_score
                    
            if(placement_score < best_score):
                best_placement = placement
                best_score = placement_score
                fe_best = fe_total

        t -= delta_t
#         print("Current score: " + str(placement_score))
#         print("Current best: " + str(best_score))
    # print("Best score: " + str(best_score))
    # print("Final score: " + str(placement_score)) 
#         print(t)
    return best_placement, best_score, fe_best+len(nodes)

def nodes_within_distance(placement, G, distance):
    nodes_within_d = set()
    nodes = placement
    for d in range(0, distance):
        neighbors = set()
        for n in nodes:
            neighbors.update(list(G.neighbors(n)))
        nodes_within_d.update(neighbors)    
        nodes = neighbors    
    return nodes_within_d

def SASH(G, nodes, scores, placement, p):
    neighborhood = nodes_within_distance(placement, G, 2)
    n = len(placement)
    n_nodes = len(nodes)
    # Instead of while 2: use a range to avoid getting stuck with small networks
    for i in range(0, n_nodes):
        r = randint(0, n-1)
        replacement = nodes[np.random.choice(n_nodes, p=p)]
        if(replacement not in neighborhood):
            if(placement[r] != replacement):
                placement[r] = replacement
                return placement


####################################### Experiment Setup ###################################################################
# This code is in this file because it is necessary to be in a separate file to be run in a multiprocess pool
def experiment(L):
    dataname = L[1]
    G = L[2]
    data = L[3]
    algorithm = L[4]
    budget = L[5]
    eval_function = L[6]
    output_file = L[7]
    start = time.time()
    [placement, score, func_evals] = algorithm(data, budget , eval_function, G)
    score = 1-score
    print("Finished main experiment with algorithm " + str(algorithm.__name__) + " and objective "+ str(eval_function.__name__) +" on dataset " + str(dataname))
    print(time.time()-start)

    fields = [dataname,algorithm.__name__,budget,time.time()-start,eval_function.__name__,score, func_evals]

    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    return [dataname,algorithm.__name__,budget,time.time()-start,eval_function.__name__,score, func_evals]

def experiment_test(L):
    dataname = L[1]
    G = L[2]
    traindata = L[3]
    algorithm = L[4]
    budget = L[5]
    eval_function = L[6]
    testdata = L[7]
    output_file = L[8]
    start = time.time()
    [placement, train_score, func_evals] = algorithm(traindata, budget , eval_function, G)
    test_score = 1-eval_function(outbreak_simulations=testdata,placement=placement)
    print("Finished train-test split experiment with algorithm " + str(algorithm.__name__) + " and objective "+ str(eval_function.__name__) +" on dataset " + str(dataname))
    print(time.time()-start)

    fields = [dataname,algorithm.__name__,budget,time.time()-start,eval_function.__name__,score, func_evals]

    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    return [dataname,algorithm.__name__,budget,time.time()-start,eval_function.__name__, train_score, test_score, func_evals]