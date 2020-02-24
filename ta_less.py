#!/usr/bin/python3

import networkx as nx
import numpy as np
import heapq

N_LESS = 2

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = nx.Graph(graph_data)
    n_seeds -= N_LESS

    all_seeds = []
    for _ in range(n_rounds):
        all_seeds.append(np.random.choice(list(G.nodes), n_seeds))

    return all_seeds
