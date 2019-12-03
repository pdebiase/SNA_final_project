# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:07:31 2019

@author: pvbia
"""
import os
import pandas as pd
import pickle
import EvaluationFunctions as ef
import OutbreaksGenerator as ob
import Algorithms as a
import multiprocessing
import csv
from datetime import datetime
####################################### EXPERIMENTS ###################################################################
    
def experiment_all_data(file_names, budgets, functions, algorithms, n_cores, output_file):
    ######### Creating a list with all the experiment setup - TRAIN TEST ########

    experiments = list()
    index = 0
    for file in file_names:
        with open(file[0], 'rb') as f:
            # read the data as binary data stream
            data = pickle.load(f)
        dataname = file[2]
        G = ob.edgelist_csv_to_graph(file[1])
        for alg in algorithms:
            for b in budgets:
                for eval_function in functions:
                    experiments.append([index,dataname,G,data,alg,b,eval_function,output_file])
                    index +=1
    del data

    fields = ['Dataset','Algorithm','Budget','Runtime','Criterion','Score','Function Evaluations']

    with open(output_file, 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    pool = multiprocessing.Pool(n_cores)
    t = pool.map(a.experiment, experiments)
        
    # df = pd.DataFrame(t,columns=['Dataset','Algorithm','Budget','Runtime','Criterion','Score', 'Function Evaluations'])  

    # Saving in CSV
    # df.to_csv("main_experiment.csv")

def experiment_train_test_split(file_names, budgets, functions, algorithms, n_cores, output_file):
    ######### Creating a list with all the experiment setup - TEST SET ########
    experiments = list()
    index = 0
    for file in file_names:
        with open(file[0], 'rb') as f:
            # read the data as binary data stream
            data = pickle.load(f)
        length = int(round(0.8*len(data),0))
        traindata = data[0:length]
        testdata = data[length:]
        dataname = file[2]
        G = ob.edgelist_csv_to_graph(file[1])
        for alg in algorithms:
            for b in budgets:
                for eval_function in functions:
                    experiments.append([index,dataname,G,traindata,alg,b,eval_function,testdata, output_file])
                    index +=1
    del data

    fields = ['Dataset', 'Algorithm', 'Budget', 'Runtime', 'Criterion', 'Train Score', 'Test Score', 'Function Evaluations']

    with open(output_file, 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    # Running experiments Using multiprocessing
    pool = multiprocessing.Pool(n_cores)
    t = pool.map(a.experiment_test, experiments)
        
    # df = pd.DataFrame(t,columns=['Dataset', 'Algorithm', 'Budget', 'Runtime', 'Criterion', 'Train Score', 'Test Score', 'Function Evaluations'])  

    # Saving in CSV
    # df.to_csv("train_test_experiment.csv")


def main():
    ####### Creating experiments setup ########
    n_cores = 3
    file_names = [
                    ["1jazz_outbreaks.data", "./data/1jazz_edges.csv","1jazz"],
                    ["2tvshow_outbreaks.data","./data/2tvshow_edges.csv","2tvshow"],
                    ["3politician_outbreaks.data","./data/3politician_edges.csv","3politician"],
                    ["4public_figure_outbreaks.data","./data/4public_figure_edges.csv","4public_figure"],
                    ["5new_sites_outbreaks.data","./data/5new_sites_edges.csv","5news_sites"]
                ]


    budgets = [5]

    functions = [ef.detection_likelihood_mean,ef.detection_time_mean,ef.population_affected_mean]

    output_file1 = "all_data.csv"
    output_file2 = "train_test.csv"
    algorithms = [
                    a.naive_greedy, 
                    a.CELF,
                    a.community_degree, 
                    a.SA, 
                    a.SA_cauchy, 
                    a.SA_geometric,
                    # a.SA_SASH,
                ]
    # path = "C:\\Users\\pvbia\\EPA - Delft\\2o Year\\Social Network\\Final Project\\SNA_final_project (v optimized)"
    # os.chdir(path)

    experiment_all_data(file_names, budgets, functions, algorithms, n_cores, output_file1)
    experiment_train_test_split(file_names, budgets, functions, algorithms, n_cores, output_file2)

if __name__ == '__main__':
    main()
