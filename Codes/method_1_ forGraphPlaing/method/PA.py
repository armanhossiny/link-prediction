import matplotlib.pyplot as plt
import networkx as nx
from math import log

def weight_preferential_attachment(G, G_weight,U, V):
        WU=0
        WV=0
        result=0.0
  
        
        for neighor in G[U]:
                WU += (G[U][neighor]['weight'])

        for neighor in G[V]:
                WV += (G[V][neighor]['weight'])   
        result=WU*WV
        return (result)

def preferential_attachment_index(G, G_weight, ebunch):
    PA_value=0
    PA=[]
    WNu=0
    for u, v in ebunch:
        PA_value=G.degree(u) * G.degree(v)
        PA.append((u,v,PA_value))
        WNu = weight_preferential_attachment(G, ebunch, u, v)           
#         print("node(", u,",",v,")","adamic_adar_index:",PA_value ,"weight: ", WNu)
    return PA