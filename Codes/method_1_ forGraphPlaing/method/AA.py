import matplotlib.pyplot as plt
import networkx as nx
from math import log
import pandas as pd
import linkpred


def common_neighbors(G, u, v, type=None):
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
    if type=="AA":
        return CN, CN_edges
    else:
        return CN_edges
#     return len(CN)

def weight_common_neighbors(G_weight, CN_edges):
        WCN=0
#     while index<=(len(CN_edges)-1):
        for u, v, data in G_weight:
            if (u, v) in CN_edges or (v, u) in CN_edges:
                WCN+=data['weight']
#                 print(u,v, ": ",data['weight'])
        return WCN


def weight_adamic_adar_index(G_weight,CN_edges, Z):
        Sz=[]
        sumWeightNeigZ=0
        CNxy=0.0
        wsz=0.0
        result=0.0
        logg=0.0
        for z in Z:
            for neighor in G[z]:
                sumWeightNeigZ += (G[z][neighor]['weight'])
            CNxy=float(weight_common_neighbors(G_weight,CN_edges))

            logg=float(log((1+sumWeightNeigZ),10))
            if(logg!=0):
    #             print("aa",(wsz), (CNxy),logg)        
                result=CNxy/logg
        return (result)

def adamic_adar_index(G, G_weight,ebunch):
    AA_value=0
    AA=[]
    for u, v in ebunch:
        AA_value=0
        CN, CN_edges=common_neighbors(G, u, v,"AA")
        
        for w in CN:
            AA_value+=(1/log(G.degree(w),10))
              
#         print("node(", u,",",v,")","adamic_adar_index:",AA_value ,"weight: ", weight_adamic_adar_index(G_weight, CN_edges, CN))
        AA.append((u,v,AA_value))
    
    return AA