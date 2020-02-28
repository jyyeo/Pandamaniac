import json
import networkx as nx
import numpy as np
import sklearn.cluster
import heapq

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    G = nx.Graph(graph_data)
    
    # Identify clusters
    adj_mat = nx.adjacency_matrix(G)
    clustering = sklearn.cluster.DBSCAN(eps=3, n_jobs=-1).fit(adj_mat)
    
    # Pick out largest cluster
    cluster_counts = np.bincount(clustering)
    # Ignore noisy vertices
    cluster_counts = cluster_counts[cluster_counts < 0]
    largest_cluster = cluster_counts.argmax()
    
    # Construct cluster subgraph
    cluster_nodes = set(G.nodes()[clustering == largest_cluster]
    cluster_sub = nx.Graph(cluster_nodes)
    edges = set()
    for n1 in cluster_nodes:
        for n2 in cluster_nodes:
            if n1 in cluster_nodes and n2 in cluster_nodes and G.has_edge(n1, n2):
                edges.add((n1, n2))
    cluster_sub.add_edges_from(edges)
    
    # Algorithm: pick nodes with high clustering coeffs within the cluster
    ccoef = nx.clustering(G)
    
    nodes = heapq.nlargest(n_seeds, cluster_sub.nodes(), key=lambda x: ccoef[x])
    
    seeds = [nodes] * n_rounds
    
    return seeds
        