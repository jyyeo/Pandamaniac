#!/usr/bin/python3

import sys
import os
import json

import random_samplers
import top_closeness_random
import beat_ta_degree2
import k_truss

import ta_degree
import ta_less
import ta_more

def main(in_graph, outfile):
    # Load graph file
    with open(in_graph) as gf:
        graph_data = json.load(gf)
        
    graph_info = os.path.basename(sys.argv[1]).split(".")

    n_players = int(graph_info[0])
    n_seeds = int(graph_info[1])
    n_rounds = 50

    # CALL FUNCTION TO GET SEED NODES HERE
    if n_players == 2:
        seed_nodes = beat_ta_degree2.get_seed_nodes(graph_data, n_players, n_seeds, n_rounds)
    else:
        seed_nodes = k_truss.get_seed_nodes(graph_data, n_players, n_seeds, n_rounds)

    with open(outfile, 'w') as of:
        for round in seed_nodes:
            for node in round:
                of.write(node + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py [x.x.x.json] [output_file]")
        exit(1)

    main(sys.argv[1], sys.argv[2])