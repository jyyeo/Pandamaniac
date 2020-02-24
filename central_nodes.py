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


# def write_seeds(output_file, all_seeds):
#     with open(output_file, "w") as f:
#         f.write("\n".join("\n".join([str(node)
#                                      for node in seeds]) for seeds in all_seeds))
#     print("INFO: Seeds successfully written to: {}".format(output_file))


def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = make_graph_from_json(graph_data)
    N = G.numberOfNodes()

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, G.numberOfEdges(), n_seeds, n_rounds))

    # estimate centrality measures on top 10% of nodes
    K = int(0.1 * N)
    node_scores = defaultdict(float)
    total_score = 0.0
    ebt = nk.centrality.EstimateBetweenness(
        G, K, normalized=True, parallel=True)
    ebt.run()
    for node, score in ebt.ranking()[:K]:
        node_scores[node] += 0.5 * score
        total_score += 0.5 * score

    tc = nk.centrality.TopCloseness(G, k=K)
    tc.run()
    for node, score in zip(tc.topkNodesList(), tc.topkScoresList()):
        node_scores[node] += 0.5 * score
        total_score += 0.5 * score

    # normalize
    for node in node_scores:
        node_scores[node] /= total_score

    # choose seeds with probability weighted by their score
    seeds = []
    for _ in range(n_rounds):
        seeds.append(np.random.choice(list(node_scores.keys()),
                                      n_seeds, replace=True, p=list(node_scores.values())))

    # # write seeds to file
    # output_file = graph_file.strip(".json") + ".out"
    # write_seeds(output_file, seeds)
    return [[str(node) for node in round] for round in seeds]
