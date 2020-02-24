import sys
import os
import json
import random_samplers

# Load graph file
in_graph = sys.argv[1]
with open(in_graph) as gf:
    graph_data = json.load(gf)
    
graph_info = os.path.basename(sys.argv[1]).split(".")

n_players = int(graph_info[0])
n_seeds = int(graph_info[1])
n_rounds = 50

# CALL FUNCTION TO GET SEED NODES HERE
seed_nodes = random_samplers.get_seed_nodes(graph_data, n_players, n_seeds, n_rounds)

outfile = sys.argv[2]
with open(outfile, 'w') as of:
    for round in seed_nodes:
        for node in round:
            of.write(node + "\n")
