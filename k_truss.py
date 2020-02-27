#!/usr/bin/python3

import sys
import json
import networkx as nx
import numpy as np
from collections import defaultdict
import heapq


def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = nx.Graph(graph_data)

    k = 0
    truss_nodes = []
    while True:
        k_truss = nx.algorithms.core.k_truss(G, k).nodes
        if not k_truss:
            break

        truss_nodes = k_truss
        k += 1

    # also tried top degree, but it's not good either
    # scores = {x: nx.algorithms.centrality.closeness_centrality(G, x) for x in truss_nodes}
    # scores = nx.algorithms.centrality.degree_centrality(G)
    # truss_nodes_sorted = sorted(list(truss_nodes), key=lambda x: scores[x])

    # src = truss_nodes_sorted[0]
    # path = nx.single_source_shortest_path_length(G, source=src, cutoff=2)

    # nodes = list(set(path).difference(set(G[src])))
    # # for x in nodes:
    # #     if x not in scores:
    # #         scores[x] = nx.algorithms.centrality.closeness_centrality(G, x)

    # nodes_sorted = sorted(nodes, key=lambda x: scores[x])

    seeds = []
    for _ in range(n_rounds):
        # seeds.append(nodes_sorted[:n_seeds])
        seeds.append(np.random.choice(list(truss_nodes), n_seeds))

    return seeds
