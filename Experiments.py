# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:07:31 2019

@author: pvbia
"""
import os
path = "C:\\Users\\pvbia\\EPA - Delft\\2o Year\\Social Network\\Final Project\\SNA_final_project (v optimized)"
os.chdir(path)
import pandas as pd
import pickle
import EvaluationFunctions as ef
import OutbreaksGenerator as ob
import Algorithms as a
import multiprocessing
####################################### EXPERIMENTS ###################################################################
    
####### Creating experiments setup ########

file_names = [["1jazz_outbreaks.data", "./data/1jazz_edges.csv","1jazz"],
#              ["2tvshow_outbreaks.data","./data/2tvshow_edges.csv","2tvshow"],
#              ["3politician_outbreaks.data","./data/33politician_edges.csv","3politician"],
#              ["4public_figure_outbreaks.data","./data/4public_figure_edges.csv","4public_figure"],
#              ["5new_sites_outbreaks.data","./data/5new_sites_edges.csv","5news_sites"]
             ]


budgets = [1,5]

functions = [ef.detection_likelihood_mean,ef.detection_time_mean,ef.population_affected_mean]

algorithms = [a.naive_greedy,a.CELF,a.community_degree]#,a.SA_SASH]

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
                experiments.append([index,dataname,G,data,alg,b,eval_function])
                index +=1
del data

if __name__ == '__main__':
    pool = multiprocessing.Pool(5)
    t = pool.map(a.experiment, experiments)
    
df = pd.DataFrame(t,columns=['Dataset','Algorithm','Budget','Runtime','Criterion','Score'])  

# Saving in CSV
df.to_csv("performance_train_df.csv")

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
                experiments.append([index,dataname,G,traindata,alg,b,eval_function,testdata])
                index +=1
del data


# Running experiments Using multiprocessing
if __name__ == '__main__':
    pool = multiprocessing.Pool(5)
    t = pool.map(a.experiment, experiments)
    
df = pd.DataFrame(t,columns=['Dataset','Algorithm','Budget','Runtime','Criterion','Score'])  

# Saving in CSV
df.to_csv("performance_test_df.csv")