import json
import numpy as np

def erdos_renyi(n,p):
    adj_mat = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i != j and np.random.random() < p:
                adj_mat[i,j] = 1
    return adj_mat

def convert_to_json(adj_mat):
    adj_dic = {}
    output = open("x.x.x.json","w")
    for i in range(len(adj_mat)):
        neighbors = []
        for j in range(len(adj_mat[i])):
            if adj_mat[i,j] == 1:
                neighbors.append(str(j))
        adj_dic[str(i)] = neighbors
    return json.dump(adj_dic, output)
    output.close()

n = 100
p = 0.5
graph = erdos_renyi(n,p)
print(convert_to_json(graph))


