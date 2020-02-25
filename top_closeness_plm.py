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

    plm_partition = nk.community.PLM(G).run().getPartition()
    partition_size_map = plm_partition.subsetSizeMap()
    largest = heapq.nlargest(2, partition_size_map, key=lambda x: partition_size_map[x])
    
    subgraph_nodes = set()
    for n in largest:
        subgraph_nodes = subgraph_nodes.union(set(plm_partition.getMembers(n)))

    subgraph = nk.graphtools.subgraphFromNodes(G, subgraph_nodes)

    # this is O(|V|*|E|), pretty fast even on 10k nodes
    tc = nk.centrality.TopHarmonicCloseness(subgraph, k=n_seeds)
    tc.run()

    nodes = tc.topkNodesList(includeTrail=True)
    # scores = tc.topkScoresList()

    seeds = []
    for _ in range(n_rounds):
        if len(nodes) == n_seeds:
            seeds.append(nodes)
        else:
            # take the top (n_seeds - 1) and one randomly from the 'trail'
            seeds.append(nodes[:n_seeds - 1] + [np.random.choice(nodes[n_seeds:])])


    return [[str(node) for node in round] for round in seeds]
