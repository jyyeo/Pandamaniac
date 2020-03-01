# degree_based_strategy.py

# Going off the intuition given for Erdos-Renyi graphs:
# if avg_degree < ref_one, we have small, unconnected components
## -> pick seed nodes at random, making sure they're all disconnected
# if ref_one < avg_degree < ref_two, each component is a tree
## -> pick seed nodes from each component in proportion to the component's size
## -> also, when choosing mutliple nodes from a single component, try to make nodes non-adjacent (or optimize some other way)
# if ref_two < avg_degree < ref_three, there is one giant component, which may be tree-like
## -> choose all nodes in the giant component and make them non-adjacent to exploit tree structure
# if ref_three < avg_degree, there is one giant connected component
## -> all bets are off.

import k_core

import networkit as nk
import numpy as np

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
    E = G.numberOfEdges()

    print("[INFO]: |V|={}, |E|={}, seeds={}, iters={}".format(
        N, E, n_seeds, n_rounds))

    # compute the connectivity of the graph
    avg_degree = N / E
    print("Average degree: {}".format(avg_degree))
    # compute a few reference points
    ref_one = 1/(N**2)
    ref_two = 1/N
    ref_three = np.log(N)/N
    print("Reference points: {}, {}, {} ".format(ref_one, ref_two, ref_three))

    # Let's code out these cases:
    if avg_degree < ref_one:
        cd = nk.community.CoreDecomposition(G)
        cd.run()
        cores = cd.getPartition()
        s = cd.maxCoreNumber()

        nodes = []
        member_to_add = 0
        while len(nodes) < n_seeds:
            member_to_add += 1
            if cores.getMembers(core_number):
                nodes.append(str( cores.getMembers(core_number)[member_to_add] ))
        nodes = [str(node) for node in nodes]
        print(nodes)

    elif avg_degree < ref_two:
        cd = nk.community.CoreDecomposition(G)
        cd.run()
        cores = cd.getPartition()
        s = cd.maxCoreNumber()

        component_sizes = []
        for core_number in range(s+1):
            if cores.getMembers(core_number):
                component_sizes.append( len(cores.getMembers(core_number)) )
            else:
                component_sizes.append(0)

        # percentage of nodes needed to justify one seed in a component
        threshold = N / n_seeds

        nodes = []
        for core_number in range(s+1):
            if cores.getMembers(core_number):
                multiples = round( len( cores.getMembers(core_number) ) / threshold )
                nodes.append( random.sample( cores.getMembers(core_number), multiples ) )
        nodes = [str(node) for node in nodes]
        print(nodes)

    elif avg_degree < ref_three:
        cd = nk.community.CoreDecomposition(G)
        cd.run()
        cores = cd.getPartition()
        s = cd.maxCoreNumber()
    
        # find largest component
        component_sizes = []
        for core_number in range(s+1):
            if cores.getMembers(core_number):
                component_sizes.append( len(cores.getMembers(core_number)) )
            else:
                component_sizes.append(0)
        largest_core = component_sizes.index(max(component_sizes))

        # choose all nodes from largest component
        nodes = [str(x) for x in cores.getMembers(largest_core)]
        print(nodes)

    else:
        cd = nk.community.CoreDecomposition(G)
        cd.run()
        cores = cd.getPartition()
        s = cd.maxCoreNumber()
    
        # find largest component
        component_sizes = []
        for core_number in range(s+1):
            if cores.getMembers(core_number):
                component_sizes.append( len(cores.getMembers(core_number)) )
            else:
                component_sizes.append(0)
        largest_core = component_sizes.index(max(component_sizes))

        # choose all nodes from largest component
        nodes = [str(x) for x in cores.getMembers(largest_core)]
        print(nodes)
  

    # prep everything for export
    seeds = []
    for _ in range(n_rounds):
        seeds.append(np.random.choice(nodes, n_seeds))

    # return for all rounds
    return seeds
