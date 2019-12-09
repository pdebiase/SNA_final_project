# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:10:20 2019

@author: pvbia
"""

# Importing packages\import os
import os
path = "C:\\Users\\pvbia\\EPA - Delft\\2o Year\\Social Network\\Final Project\\Experiments"
os.chdir(path)
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from pylab import rcParams
import matplotlib as mpl



## Loading data
df = pd.read_excel(path + "\\Experiments VF with Nodes.xlsx")
label = list(set(df.Algorithm))
colors1 = ['navy','darkred','orange','darkviolet','lightpink','green','dodgerblue']
colors2 = ['darkred','orange','darkviolet','lightpink']
################### INDIVIDUA PLOTS ########################
df.columns

########### Function Eval VS Nodes and Algorithm
rcParams['figure.figsize'] =8, 8

data = pd.pivot_table(df, values='FunctionEvaluations',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)

# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Number of Function Evaluations")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_FunctionEval_Nodes.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Number of Function Evaluations")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_FunctionEval_Nodes.png')
############# Score VS Nodes and Algorithm

### DL
df1 = df.loc[df['Criterion'] == "detection_likelihood_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Detection Likelihood Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_DL_Nodes.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Detection Likelihood Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_DL_Nodes.png')
### DT
df1 = df.loc[df['Criterion'] == "detection_time_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Detection Time Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_DT_Nodes.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Detection Time Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_DT_Nodes.png')


### PA
df1 = df.loc[df['Criterion'] == "population_affected_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Population Affected Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_PA_Nodes.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Number of Nodes")
ax.set_ylabel("Population Affected Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_PA_Nodes.png')

############# Function Evaluation Vs Budget

data = pd.pivot_table(df, values='FunctionEvaluations',index = ['Budget'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Budget")
ax.set_ylabel("Number of Function Evaluations")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_FunctionEval_Budget.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Budget")
ax.set_ylabel("Number of Function Evaluations")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_FunctionEval_Budget.png')


############# Score Vs Budget

### DL
df1 = df.loc[df['Criterion'] == "detection_likelihood_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Budget'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Budget")
ax.set_ylabel("Detection Likelihood Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_DL_Budget.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Budget")
ax.set_ylabel("Detection Likelihood Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_DL_Budget.png')
### DT
df1 = df.loc[df['Criterion'] == "detection_time_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Budget'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Budget")
ax.set_ylabel("Detection Time Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_DT_Budget.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Budget")
ax.set_ylabel("Detection Time Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_DT_Budget.png')

### PA
df1 = df.loc[df['Criterion'] == "population_affected_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Budget'],columns=['Algorithm'], aggfunc=np.mean)
# All
ax = data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1))
ax.set_xlabel("Budget")
ax.set_ylabel("Population Affected Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('All_PA_Budget.png')
# Just SA
data2 = data.iloc[:,[1,2,3,4]]
ax = data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2))
ax.set_xlabel("Budget")
ax.set_ylabel("Population Affected Score")
ax.grid('on', which='major', axis='x' )
ax.grid('on', which='major', axis='y' )
plt.savefig('Sash_PA_Budget.png')



########################################## Plots with Subplots ######################################
########### Function Eval VS Nodes and Algorithm
data = pd.pivot_table(df, values='FunctionEvaluations',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
data2 = data.iloc[:,[1,2,3,4]]
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# All
data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1), ax=ax1)
ax1.set_xlabel("Number of Nodes")
ax1.set_ylabel("Number of Function Evaluations")
ax1.grid('on', which='major', axis='x' )
ax1.grid('on', which='major', axis='y' )
ax1.text(0.5,-0.2, "(a) All Algorithms", size=12, ha="center", transform=ax1.transAxes)
# Just SA
data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2), ax=ax2)
ax2.set_xlabel("Number of Nodes")
ax2.grid('on', which='major', axis='x' )
ax2.grid('on', which='major', axis='y' )
ax2.text(1.7,-0.2, "(b) Simulated Annealing", size=12, ha="center", transform=ax1.transAxes)
# Set common labels
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig('FunctionEval_Nodes.png')

############# Score VS Nodes and Algorithm

### DL
df1 = df.loc[df['Criterion'] == "detection_likelihood_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
data2 = data.iloc[:,[1,2,3,4]]
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# All
data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1), ax=ax1)
ax1.set_xlabel("Number of Nodes")
ax1.set_ylabel("Detection Likelihood Score")
ax1.grid('on', which='major', axis='x' )
ax1.grid('on', which='major', axis='y' )
ax1.text(0.5,-0.2, "(a) All Algorithms", size=12, ha="center", transform=ax1.transAxes)
# Just SA
data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2), ax=ax2)
ax2.set_xlabel("Number of Nodes")
ax2.grid('on', which='major', axis='x' )
ax2.grid('on', which='major', axis='y' )
ax2.text(1.7,-0.2, "(b) Simulated Annealing", size=12, ha="center", transform=ax1.transAxes)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig('DL_Nodes.png')


### DT
df1 = df.loc[df['Criterion'] == "detection_time_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
data2 = data.iloc[:,[1,2,3,4]]
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# All
data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1), ax=ax1)
ax1.set_xlabel("Number of Nodes")
ax1.set_ylabel("Detection Time Score")
ax1.grid('on', which='major', axis='x' )
ax1.grid('on', which='major', axis='y' )
ax1.text(0.5,-0.2, "(a) All Algorithms", size=12, ha="center", transform=ax1.transAxes)
# Just SA
data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2), ax=ax2)
ax2.set_xlabel("Number of Nodes")
ax2.grid('on', which='major', axis='x' )
ax2.grid('on', which='major', axis='y' )
ax2.text(1.7,-0.2, "(b) Simulated Annealing", size=12, ha="center", transform=ax1.transAxes)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig('DT_Nodes.png')


### PA
df1 = df.loc[df['Criterion'] == "population_affected_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Nodes'],columns=['Algorithm'], aggfunc=np.mean)
data2 = data.iloc[:,[1,2,3,4]]
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# All
data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1), ax=ax1)
ax1.set_xlabel("Number of Nodes")
ax1.set_ylabel("Population Affected Score")
ax1.grid('on', which='major', axis='x' )
ax1.grid('on', which='major', axis='y' )
ax1.text(0.5,-0.2, "(a) All Algorithms", size=12, ha="center", transform=ax1.transAxes)
# Just SA
data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2), ax=ax2)
ax2.set_xlabel("Number of Nodes")
ax2.grid('on', which='major', axis='x' )
ax2.grid('on', which='major', axis='y' )
ax2.text(1.7,-0.2, "(b) Simulated Annealing", size=12, ha="center", transform=ax1.transAxes)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig('PA_Nodes.png')

############# Function Evaluation Vs Budget

data = pd.pivot_table(df, values='FunctionEvaluations',index = ['Budget'],columns=['Algorithm'], aggfunc=np.mean)
data2 = data.iloc[:,[1,2,3,4]]
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# All
data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1), ax=ax1)
ax1.set_xlabel("Budget")
ax1.set_ylabel("Number of Function Evaluations")
ax1.grid('on', which='major', axis='x' )
ax1.grid('on', which='major', axis='y' )
ax1.text(0.5,-0.2, "(a) All Algorithms", size=12, ha="center", transform=ax1.transAxes)
# Just SA
data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2), ax=ax2)
ax2.set_xlabel("Budget")
ax2.grid('on', which='major', axis='x' )
ax2.grid('on', which='major', axis='y' )
ax2.text(1.7,-0.2, "(b) Simulated Annealing", size=12, ha="center", transform=ax1.transAxes)
# Set common labels
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig('FunctionEval_Budget.png')

############# Score Vs Budget

df1 = df.loc[df['Criterion'] == "detection_likelihood_mean"]
data = pd.pivot_table(df1, values='Score',index = ['Budget'],columns=['Algorithm'], aggfunc=np.mean)
data2 = data.iloc[:,[1,2,3,4]]
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# All
data.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors1), ax=ax1)
ax1.set_xlabel("Budget")
ax1.set_ylabel("Detection Likelihood Score")
ax1.grid('on', which='major', axis='x' )
ax1.grid('on', which='major', axis='y' )
ax1.text(0.5,-0.2, "(a) All Algorithms", size=12, ha="center", transform=ax1.transAxes)
# Just SA
data2.plot(linestyle='-', marker='o',cmap=mpl.colors.ListedColormap(colors2), ax=ax2)
ax2.set_xlabel("Budget")
ax2.grid('on', which='major', axis='x' )
ax2.grid('on', which='major', axis='y' )
ax2.text(1.7,-0.2, "(b) Simulated Annealing", size=12, ha="center", transform=ax1.transAxes)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig('DL_Budget.png')