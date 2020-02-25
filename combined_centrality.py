#!/usr/bin/python3

import sys
import json
import networkx as nx
import numpy as np
import networkit as nk
from collections import defaultdict
import heapq

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

    K = 0.1 * N  # Top 10% of nodes
    node_scores = defaultdict(float)

    dc = nk.centrality.DegreeCentrality(G, normalized=True)
    dc.run()
    
    for node, score in dc.ranking():
        node_scores[node] += 0.5 * score

    tc = nk.centrality.TopHarmonicCloseness(G, k=K)
    tc.run()

    nodes = tc.topkNodesList(includeTrail=True)
    scores = np.array(tc.topkScoresList(includeTrail=True))

    for node, score in zip(nodes, scores):
        node_scores[node] += 0.5 * score

    top = heapq.nlargest(n_seeds, node_scores, key=lambda x: node_scores[x])
    seeds = []
    for _ in range(n_rounds):
        seeds.append(top)

    return [[str(node) for node in round] for round in seeds]
