#!/usr/bin/python3

import sys
import json
import networkit as nk
import numpy as np
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
    G.removeSelfLoops()
    N = G.numberOfNodes()

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, G.numberOfEdges(), n_seeds, n_rounds))

    cd = nk.community.CoreDecomposition(G)
    cd.run()

    cores = cd.getPartition()
    s = cd.maxCoreNumber()
    nodes = [str(x) for x in cores.getMembers(s)]
    # nodes = tc.topkNodesList(includeTrail=True)
    # scores = tc.topkScoresList()

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
        seeds.append(np.random.choice(nodes, n_seeds))

    return seeds
