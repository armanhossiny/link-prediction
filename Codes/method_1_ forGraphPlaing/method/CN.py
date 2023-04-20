import matplotlib.pyplot as plt
import networkx as nx
import random


def percentage(percent, whole):
    return int((percent * whole) / 100.0)

def reverse_weight_edges(G_weight):
    G=[]
    min, max = main_max_wieghted(G_weight)
    for u, v, data in G_weight:
        G.append((u,v,{'weight': round((max+min)-data['weight'], 2)}))
    print("sum Min and Max weight:",max+min)
    return G

def common_neighbors(G, u, v):
    if u not in G:
        raise nx.NetworkXError('u is not in the graph.')
    if v not in G:
        raise nx.NetworkXError('v is not in the graph.')
    CN=[]
    CN_edges=[]
    for w in G[u]:
        if w in G[v] and w not in (u,v):
            CN.append(w)
            CN_edges.append((w, u))
            CN_edges.append((w, v))

    aa = (w for w in G[u] if w in G[v] and w not in (u, v))
#     return CN, CN_edges
    return CN_edges
#     return len(CN)

def weight_common_neighbors(G_weight, CN_edges):
        WCN=0
#     while index<=(len(CN_edges)-1):
        for u, v, data in G_weight:
            if (u, v) in CN_edges or (v, u) in CN_edges:
                WCN+=data['weight']
#                 print(u,v, ": ",data['weight'])
        return (round(WCN,2))

def compare_result_with_target(list_pridect, listEdgesAdded, numEdgeAdded):

    i=0
    numberFoundAnomalyEdge=0
    classEdge=[]
    for edge in list_pridect:
        if (i<numEdgeAdded):
            for node in listEdgesAdded:
                if ((edge[0]==node[0] and edge[1]==node[1]) or (edge[1]==node[0] and edge[0]==node[1])) :
                    numberFoundAnomalyEdge+=1
                    classEdge.append(1)
                    print("num: ", numberFoundAnomalyEdge, "index", i,": ", node)
        classEdge.append(0)
        i+=1
    print(numberFoundAnomalyEdge, "found anomaly edge!")


def NLP_CN(G, G_weight_reverse):

    CN_value=[]

    Matrix=nx.to_numpy_matrix(G,sorted(G.nodes()))
    maxIndex= len(G.nodes())
    TopRank=-1
    TempRank=0
    i=0
    j=0
    for i in list(range((maxIndex-1))):
        for j in list(range(i,(maxIndex))):
    #         print(i,j)
            if Matrix[i,j] !=0:
                TempRank = len(list(nx.common_neighbors(G, i, j)))
    #             print(i,j, ": ", TempRank)
                edges= common_neighbors(G, i, j)
                CN_value.append((i,j,weight_common_neighbors(G_weight_reverse, edges)))
    #             print("node(", i,",",j,")","number_common_neighbors:",TempRank,"weight: ", weight_common_neighbors(G_weight_main, edges))
                if TempRank> TopRank:
    #                 print("TopRank: ",i, j,": ", TempRank)
                    TopRank=TempRank

    common_neighbors_results= sorted(CN_value, reverse=True, key=lambda x: x[2])
    return common_neighbors_results

    
def find_edge_with_lessDegree_avg(nonedges):
    avg_degrees = sum(d for n, d in G.degree()) / float(len(G.nodes()))
    list_degree = sorted(G.degree() , reverse=True, key=lambda x: x[1])
    print("@@@ avrage_degrees: ", avg_degrees)
    list_degree_less_avg=[]
    for node, degree in list_degree:
        nodeA = random.randint(0,(len(nonedges)-1))
        if degree<(avg_degrees):
            list_degree_less_avg.append((node, degree))


    list_edges_with_lessDegreeAvg = []
    for node in nonedges:
        a=-1
        b=-1
        for node_degree in list_degree_less_avg:
            if (node[0] == node_degree[0]) and a==-1 :
                a = node[0]             
            if (node[1] == node_degree[0]) and b==-1  :
                b = node[1]
        if a!=-1 and b!=-1:
            list_edges_with_lessDegreeAvg.append((a,b))
    #         print(a, b)
    return  list_edges_with_lessDegreeAvg

