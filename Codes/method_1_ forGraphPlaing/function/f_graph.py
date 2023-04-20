
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib as plt

# description: draw graph, convert graph to adjacency matrix
# input: garph node
# output: draw graph, adjacency matrix
def draw_graph(G):
    # graph
    # G = nx.karate_club_graph()
  

    # matrix
    nodes= sorted(G)
    A = nx.to_numpy_matrix(G, nodelist=nodes)
    matrix = np.array(A)
    
    G= nx.from_numpy_matrix(matrix)
    # nx.draw(G, with_labels = True)
    return G, matrix


# description: convert adjacency matrix to invers adjacency matrix
# input: adjacency matrix
# output: invers adjacency matrix
def matrix_invers(G):
    # convert graph to matrix adjancey
    matrix= nx.adjacency_matrix(G)
    matrix_adjncy=matrix.todense()

    # convert matrix adjancey to invers
    matrix_invers=np.logical_not(matrix_adjncy)
    matrix_invers= matrix_invers.astype(np.int)

    # conver dimater main to zero
    for i in range(0, len(matrix_invers)):
        for j in range(0, len(matrix_invers)):
            if i==j:
                # print(matrix_invers[i, j])
                matrix_invers[i, j]=0
                
    # convert matrix to graph 
    G_invers = nx.from_numpy_matrix(matrix_invers)
    # nx.draw(G_invers, with_labels = True)
    # print(G_invers)

    return G_invers, matrix_invers

def percentage(percent, whole):
    return int((percent * whole) / 100.0)