import numpy as np
import heapq

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    # Don't want to select too low - exclude the lower half of nodes
    nodes = heapq.nlargest(len(graph_data) / 2, graph_data.keys(), key=lambda x: len(graph_data[x]))
    
    # Weigh central nodes more strongly by squaring
    weights = np.array(map(lambda x: len(graph_data[x]), nodes), dtype=np.float64) ** 2
    weights /= sum(weights)
    # print(weights)
    
    rounds = []
    for r in xrange(n_rounds):
        seeds = np.random.choice(nodes, n_seeds, replace=False, p=weights)
        rounds.append(seeds)
        
    return rounds