#!/usr/bin/python3

import networkx as nx
import numpy as np
import heapq

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = nx.Graph(graph_data)
    nodes = heapq.nlargest(n_seeds, list(G.nodes), key=lambda n: G.degree[n])
    return [nodes] * n_rounds
