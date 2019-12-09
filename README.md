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
### Licensing
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
