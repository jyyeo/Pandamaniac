#!/usr/bin/python3

import sys
import json
import networkx as nx
import numpy as np
import networkit as nk
from collections import defaultdict
import itertools

from pandemaniac_sim import sim
import ta_degree



def make_graph_from_json(json_data):
    G = nk.Graph()

    for node in json_data:
        for neighbor in json_data[node]:
            G.addEdge(int(node), int(neighbor), addMissing=True)

    return G

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = make_graph_from_json(graph_data)
    N = G.numberOfNodes()
    K = int(1.5 * n_seeds)

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, G.numberOfEdges(), n_seeds, n_rounds))

    tc = nk.centrality.TopHarmonicCloseness(G, k=K)
    tc.run()

    # get top K closeness centrality nodes
    tc_nodes = [str(x) for x in tc.topkNodesList(includeTrail=True)]

    # get top K degree centrality nodes
    td_nodes = ta_degree.get_seed_nodes(graph_data, n_players, K, 1)[0]

    # merge both
    combined_nodes = list(set(tc_nodes).union(set(td_nodes)))

    # ta_more gets 1.5x the amount of seeds?
    ta_seeds = ta_degree.get_seed_nodes(graph_data, n_players, n_seeds, 1)[0]

    # try all subsets
    found = False
    for our_seeds in itertools.combinations(combined_nodes, n_seeds):
        sim_nodes = {'ta': ta_seeds, 'us': our_seeds}
        result = sim.run(graph_data, sim_nodes)
        if result['us'] > result['ta']:
            found = True
            break

    if not found:
        print("can't beat them :(")
        seeds = []
        for _ in range(n_rounds):
            # no combination worked, just randomly choose from top centrality nodes
            seeds.append(np.random.choice(combined_nodes, n_seeds))
        return seeds

    else:
        print(result)
        # just use the same seeds for all rounds since we know it beats TAs
        return [our_seeds] * n_rounds
