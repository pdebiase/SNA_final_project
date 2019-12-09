# SNA_final_project

Authors:
@victorneuteboom & @pdebiase

This repository contains source code of a student project for the course Social Network Analysis for Computer Science at Leiden University.

### Generating Outbreaks
Before running experiments, outbreak simulation data needs to be generated first. This can be done by running the following command:
<i> python3 OutbreaksGenerator.py </i>

### Running Experiments
The experiments are defined in Experiments.py. In this file, you can specify which algorithms, budgets and datasets to use. 
Algorithms will be imported from Algorithms.py. The objective functions are imported from EvaluationFunctions.py.
Run the following command to perform experiments:
<i> python3 Experiments.py </i>
