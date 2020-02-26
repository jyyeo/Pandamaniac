#!/usr/bin/python3

import sys
import os
import json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
import matplotlib.animation
import matplotlib.pyplot as plt

from pandemaniac_sim import sim

import random_samplers
import top_closeness
import top_betweenness
import combined_centrality
import beat_ta_degree
import beat_ta_degree2
import k_truss

import ta_degree
import ta_less
import ta_more

# 2-player graph visualization

def main(in_graph):
    # Load graph file
    with open(in_graph) as gf:
        graph = json.load(gf)
        
    graph_info = os.path.basename(sys.argv[1]).split(".")

    n_players = int(graph_info[0])
    n_seeds = int(graph_info[1])
    n_rounds = 50

    # CALL FUNCTION TO GET SEED NODES HERE
    s1 = ta_degree.get_seed_nodes(graph, n_players, n_seeds, n_rounds)
    s2 = beat_ta_degree2.get_seed_nodes(graph, n_players, n_seeds, n_rounds)

    s1_name = 'degree'
    s2_name = 'beat_ta_degree2'

    nodes = {s1_name: s1[0], s2_name: s2[0]}

    result, hist = sim.run(graph, nodes, return_hist=True)
    G = nx.Graph(graph)
    pos = nx.spring_layout(G, seed=0)

    fig, ax = plt.subplots(figsize=(6,4))

    def update(i):
        ax.clear()

        node_colors = hist[i][1]
        colors = []
        for node in G.nodes:
            if node in node_colors:
                if node_colors[node] == '__CONFLICT__':
                    colors.append('w')
                elif node_colors[node] == None:
                    colors.append('k')
                elif node_colors[node] == s1_name:
                    colors.append('b')
                else:
                    colors.append('r')
            else:
                colors.append('k')
   
        nx.draw(G, pos, node_size=1, width=0.1, node_color=colors)
        ax.set_title("Iteration: " + str(i), fontweight="bold")

    print(result)
    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(hist), interval=500, repeat=True)
    plt.show()

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [x.x.x.json]")
        exit(1)

    main(sys.argv[1])