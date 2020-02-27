import json
import networkx as nx
import numpy as np
from operator import itemgetter


def create_deg_ctr_neighbors(G, ctr_ind, sorted_deg_ctr):
    deg_ctr_neighbors = np.zeros((1,len([n for n in G[ctr_ind]])))
    deg_ctr_neighbors = [n for n in G[ctr_ind]]
    deg_ctr_neighbors = np.array(deg_ctr_neighbors)
    deg_ctr_neighbors = np.reshape(deg_ctr_neighbors,(1,len(deg_ctr_neighbors))).T
    # print(deg_ctr_neighbors)
    ind = np.where(np.isin(sorted_deg_ctr[:,0],deg_ctr_neighbors))
    deg_ctr_neighbors2 = (itemgetter(*np.asarray(ind))(sorted_deg_ctr[:,1]))
    deg_ctr_neighbors2 = np.array(deg_ctr_neighbors2)
    deg_ctr_neighbors2 = np.reshape(deg_ctr_neighbors2,(1,len(deg_ctr_neighbors))).T
    # print(deg_ctr_neighbors2)
    deg_ctr_neighbors = np.concatenate((deg_ctr_neighbors,deg_ctr_neighbors2),axis=1)
    #print(deg_ctr_neighbors)
    deg_ctr_neighbors = deg_ctr_neighbors[deg_ctr_neighbors[:,1].argsort()[::-1]]
    # print(deg_ctr_neighbors)
    return deg_ctr_neighbors

def get_seed_nodes(graph_data, n_players, n_seeds, n_rounds):
    num_nodes = len(graph_data)
    adj_mat = np.zeros((num_nodes,num_nodes))
    for i in range(num_nodes):
        for neighbor in graph_data[str(i)]:
            adj_mat[i][int(neighbor)] = 1
    G = nx.from_numpy_matrix(adj_mat)
    
    deg_centrality = nx.degree_centrality(G)
    sorted_deg_ctr = sorted(deg_centrality.items(),key=itemgetter(1),reverse=False) # least central ones as seeds
    sorted_deg_ctr = np.array(sorted_deg_ctr).reshape([len(sorted_deg_ctr),2])
    
    seeds = np.zeros((50,n_seeds))
    ctr_ind = 0 #keeps track of centres of influence
    sorted_ind = 0 #keeps track of sorted centres
    temp_ind = 0 #index within deg_ctr_neighbor
    deg_ctr_neighbors = np.zeros((1,2))
    for i in range(50):
        for j in range(n_seeds):
            if j == 0 and i == 0 or ([n for n in G[ctr_ind]]==[]):
                seeds[i,j] = sorted_deg_ctr[sorted_ind][0]
                ctr_ind = seeds[i,j]
                if [n for n in G[ctr_ind]]!=[]:
                    deg_ctr_neighbors = create_deg_ctr_neighbors(G, ctr_ind, sorted_deg_ctr)                   
                sorted_ind += 1
                # print(i,j,seeds[i][j],'1',sorted_ind, ctr_ind)
            else:
                if temp_ind >= len(deg_ctr_neighbors):
                    temp_ind = 0
                    ctr_ind = deg_ctr_neighbors[0,0]
                    deg_ctr_neighbors = create_deg_ctr_neighbors(G, ctr_ind, sorted_deg_ctr)
                    seeds[i,j] = deg_ctr_neighbors[temp_ind,0]
                    temp_ind += 1
                    # print(i,j,seeds[i,j],'3', sorted_ind, ctr_ind)
                else:
                    seeds[i,j] = deg_ctr_neighbors[temp_ind,0]
                    temp_ind += 1
                    # print(i,j,seeds[i,j],'4')
    ret = []
    for round in seeds:
        x = []
        for s in round:
            x.append(str(int(s)))
        ret.append(x)
    return ret