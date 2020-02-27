#!/usr/bin/python3

import sys
import json
import networkx as nx
import numpy as np
import networkit as nk
from collections import defaultdict

def make_graph_from_json(json_data):
    G = nk.Graph()

    for node in json_data:
        for neighbor in json_data[node]:
            G.addEdge(int(node), int(neighbor), addMissing=True)

    return G

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = make_graph_from_json(graph_data)
    N = G.numberOfNodes()
    K = 1.5 * n_seeds

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, G.numberOfEdges(), n_seeds, n_rounds))

    # this is O(|V|*|E|), pretty fast even on 10k nodes
    tc = nk.centrality.TopHarmonicCloseness(G, k=K)
    tc.run()

    nodes = [str(x) for x in tc.topkNodesList(includeTrail=True)]
    # scores = tc.topkScoresList()

    seeds = []
    for _ in range(n_rounds):
        seeds.append(np.random.choice(nodes, n_seeds))

    return seeds
