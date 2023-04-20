import matplotlib.pyplot as plt
import networkx as nx
from math import log
import random

def percentage(percent, whole):
    return int((percent * whole) / 100.0)


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


    if type=="AA":
        return CN, CN_edges
    else:
        return CN_edges
#     return len(CN)

def weight_Jaccard_Coefficient(G_weight, CN_edges, Z):
    WCN=0

    for u, v, data in G_weight:
        if (u, v) in CN_edges or (v, u) in CN_edges:
            WCN+=data['weight']
#           print(u,v, ": ",data['weight'])

#     for neighor in G[U]:
#             WU += (G[U][neighor]['weight'])

#     for neighor in G[V]:
#             WV += (G[V][neighor]['weight']) 
            
#     a=WU+WV
    return (round(WCN,2))

def Jaccard_Coefficient_index(G, G_weight, ebunch):
    WJC_value=0
    JC_value=0
    JC=[]
    WU=0
    WV=0 
    for u, v in ebunch:
        AA_value=0
        WU=0
        WV=0
        CN, CN_edges=common_neighbors(G, u, v,"AA")

        sumWxzWyz = weight_Jaccard_Coefficient(G_weight, CN_edges, CN)
        
        for neighor in G[u]:
            WU += (G[u][neighor]['weight'])
        for neighor in G[v]:
            WV += (G[v][neighor]['weight']) 
            
#         print(("WU: ",WU,"WV: ",WV))
        WJC_value=sumWxzWyz/(WU+WV)
        JC.append((u,v,WJC_value))
        
# *************************************** JC
        union_size = len(set(G[u]) | set(G[v]))
        if union_size == 0:
             JC_value=0
        else:
            JC_value=(len(list(nx.common_neighbors(G, u, v)))/ union_size)
            
#         print("node(", u,",",v,")","Jaccard_Coefficient_index:",JC_value ,"weight: ", WJC_value)   

    return JC

