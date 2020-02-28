import json
import networkx as nx
import numpy as np
import sklearn.cluster
import heapq

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = nx.Graph(graph_data)
    
    print("Clustering...")
    # Identify clusters
    adj_mat = nx.adjacency_matrix(G)
    # clustering = sklearn.cluster.DBSCAN(eps=3, n_jobs=-1).fit(adj_mat).labels_
    clustering = sklearn.cluster.SpectralClustering(n_players, n_jobs=-1).fit(adj_mat).labels_
    print("Clustering done")
    
    # Pick out largest cluster
    u, idx = np.unique(clustering[clustering != -1], return_inverse=True)
    # Ignore noisy vertices
    largest_cluster = u[np.argmax(np.bincount(idx))]
    
    # Construct cluster subgraph
    cluster_nodes = set()
    for i in range(len(G.nodes)):
        if clustering[i] == largest_cluster:
            cluster_nodes.add(str(i))
    cluster_sub = nx.Graph()
    cluster_sub.add_nodes_from(cluster_nodes)
    edges = set()
    for n1 in cluster_nodes:
        for n2 in cluster_nodes:
            if n1 in cluster_nodes and n2 in cluster_nodes and G.has_edge(n1, n2):
                edges.add((n1, n2))
    cluster_sub.add_edges_from(edges)
    
    # Algorithm: pick nodes with high clustering coeffs within the cluster
    score = nx.harmonic_centrality(G)
    
    s = sorted(G.nodes, key=lambda x: score[x], reverse=True)
    nodes = []
    for n in s:
        if n in cluster_nodes:
            nodes.append(n)
    
    
    seeds = [nodes[:n_seeds]] * n_rounds
    
    return seeds
        