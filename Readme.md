# Project Computational Science
Date: 02-02-2023
## Group
    Students: Diederik Carpay, Rico van Arendonk, Néstor Narbona Chulvi, Bram Stibbe
    Student numbers: 12865605, 11781688, 12611093, 14715376

## Explanation of files
The SocialGraph.py, SophGraph.py and get_metrics.py are files meant to be
imported and used by other files. structure_analysis.py  can be ran to study 
the structure of both used networks. running_model.py is ran to generate data 
for the three used metrics over the parameter ranges chosen and be stored in 
Results. This data is used by visualization_&_results.py to generate plots and 
calculate the average percent error.

## Explanation of network
The two networks used are barabasi-albert and an empirical facebook network.
The facebook network is stored as a list of undirected, unweighted edges in
facebook_combined.txt.

## Code
All code is written in python3

### Used modules/prerequisites
- networkx
- numpy-1.24.1
- pandas-1.5.3
- matplotlib-3.6.3
s
All these can be installed with pip3 install networkx, numpy, pandas, matplotlib
Make sure you have the right version! If you're getting an error while running
visualize_&_results.py, it's likely because you don't have the correct versions

### Running the code
To create the csv's in the results file, run running_model.py and set the steps
variable in running_model to 20, and the sims in the function call to get_param_results() to 20 as well.

**We do not recommend you actually do this, we did it overnight.**

You can however, read in the results by running visualize_&_results.py, this will
produce an image showing three metrics for both models, with changing the decay_rate
parameter.

### Classes
The SocialGraph and SophGraph classes were used to change the network into an
actual model. The SophGraph is a subclass of SocialGraph, having additional parameters
and finetuning.
