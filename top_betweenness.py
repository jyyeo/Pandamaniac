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

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, G.numberOfEdges(), n_seeds, n_rounds))

    # this is O(m)
    bc = nk.centrality.EstimateBetweenness(G, nSamples=8, normalized=True)
    bc.run()

    nodes = [x[0] for x in bc.ranking()[:n_seeds]]
    # scores = tc.topkScoresList()

    seeds = []
    for _ in range(n_rounds):
        seeds.append(nodes)

    return [[str(node) for node in round] for round in seeds]
