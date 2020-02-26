#!/usr/bin/python3

import sys
import json
import networkx as nx
import numpy as np
import networkit as nk
from collections import defaultdict

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
    nodes = [str(x) for x in tc.topkNodesList(includeTrail=True)]

    # get top K degree centrality nodes
    ta_nodes = ta_degree.get_seed_nodes(graph_data, n_players, K, 1)[0]

    # merge both
    combined_nodes = list(set(nodes).union(set(ta_nodes)))

    # while we don't beat TAs, find another random set of top nodes
    seen = set()
    ta_seeds = ta_degree.get_seed_nodes(graph_data, n_players, n_seeds, 1)[0]
    our_seeds = np.random.choice(combined_nodes, n_seeds)
    sim_nodes = {'ta': ta_seeds, 'us': our_seeds}
    result = sim.run(graph_data, sim_nodes)
    seen.add(','.join(sorted(our_seeds)))
    
    while result['us'] <= result['ta']:
        our_seeds = np.random.choice(combined_nodes, n_seeds)
        
        our_seeds_str = ','.join(sorted(our_seeds))
        if our_seeds_str in seen:
            continue

        seen.add(our_seeds_str)
        sim_nodes = {'ta': ta_seeds, 'us': our_seeds}
        result = sim.run(graph_data, sim_nodes)

    # just use the same seeds for all rounds since we know it beats TAs
    print(result)
    seeds = []
    for _ in range(n_rounds):
        seeds.append(our_seeds)

    return seeds
