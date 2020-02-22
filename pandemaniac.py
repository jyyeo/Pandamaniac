import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import sys

# load data and create networkx graph
with open('x.x.x.json') as data_file:
    data = json.load(data_file)
num_nodes = len(data)
adj_mat = np.zeros((num_nodes,num_nodes))
for i in range(num_nodes):
    for neighbor in data[str(i)]:
        adj_mat[i][int(neighbor)] = 1
G = nx.from_numpy_matrix(adj_mat)
print(len(G))
print(len(data))

# calculate centralities
deg_centrality = nx.degree_centrality(G)
sorted_deg_ctr = sorted(deg_centrality.items(),key=itemgetter(1),reverse=False) # least central ones as seeds
print(sorted_deg_ctr)

# seeds
seeds = np.zeros(50)
for i in range(50):
    seeds[i] = sorted_deg_ctr[i][0]
print(seeds)
#return seeds
