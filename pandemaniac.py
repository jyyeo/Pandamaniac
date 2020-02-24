#!/usr/bin/python3

import sys
import json
import networkx as nx
import numpy as np
import networkit as nk
from collections import defaultdict

NUM_ITERS = 50


def read_json_graph(graph_file):
    f = open(graph_file)
    graph = json.load(f)

    G = nk.Graph()

    for node in graph:
        for neighbor in graph[node]:
            G.addEdge(int(node), int(neighbor), addMissing=True)

    return G


def write_seeds(output_file, all_seeds):
    with open(output_file, "w") as f:
        f.write("\n".join("\n".join([str(node)
                                     for node in seeds]) for seeds in all_seeds))
    print("INFO: Seeds successfully written to: {}".format(output_file))


def main(graph_file):
    num_players, num_seeds, _, _ = graph_file.split("/")[1].split(".")
    num_players, num_seeds = int(num_players), int(num_seeds)
    G = read_json_graph(graph_file)
    N = G.numberOfNodes()

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, G.numberOfEdges(), num_seeds, NUM_ITERS))

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
    for _ in range(NUM_ITERS):
        seeds.append(np.random.choice(list(node_scores.keys()),
                                      num_seeds, replace=True, p=list(node_scores.values())))

    # write seeds to file
    output_file = graph_file.strip(".json") + ".out"
    write_seeds(output_file, seeds)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pandemaniac.py [x.x.x.json]")
        exit(1)

    main(sys.argv[1])
