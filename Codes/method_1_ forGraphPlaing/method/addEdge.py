
import random
import networkx as nx
import numpy as np
from function import f_onion_decomposition
from function import f_graph
def percentage(percent, whole):
    return int((percent * whole) / 100.0)

def reverse_weight_edges(G_weight):
    G=[]
    min=False
    max=0
    for u, v, data in G_weight:
        if min==False:
            min=data['weight']
        if data['weight']<min:
            min=data['weight']
        if data['weight']>max:
            max=data['weight']
    for u, v, data in G_weight:
        G.append((u,v,{'weight': round((max+min)-data['weight'], 2)}))
    print("sum Min and Max weight:",max+min)
    return G


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
                    # print("num: ", numberFoundAnomalyEdge, "index", i,": ", node)
        classEdge.append(0)
        i+=1
    print(numberFoundAnomalyEdge, "found anomaly edge!")



def find_edge_with_lessDegree_avg(nonedges, G):
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

def main_max_wieghted(G_weight):
    
    minElement=False
    minElement2=0
    
    all_edges_weight=[]
    for u, v, data in G_weight:
        all_edges_weight.append(data['weight'])
        
    sorted_all_wight = sorted(all_edges_weight)
    for i in sorted_all_wight:
        if minElement==False:
            minElement=i
        elif i>minElement:
            minElement2=i
            break
    minElement = np.amin(sorted_all_wight)
    maxElement = np.amax(sorted_all_wight)
    print(" minElement:",minElement," minElement2:", minElement2," maxElement:", maxElement)

    return minElement, maxElement, minElement2
# def main_max_wieghted(G_weight):
    
#     min=False
#     min1=None
#     min2=0
#     max=0
#     for u, v, data in G_weight:
#         if min==False:
#             min=data['weight']
#         if data['weight']<min:
#             min1=min
#             min=data['weight']   
#         elif min1 == None or min1 > data['weight']  :
#             min1 = data['weight']       
#         if data['weight']>max:
#             max=data['weight']
#     print("min: ", min,"min: ", min1, "max: ", max)
#     return min, max

def avg_wieghted_edge(G):
    list_edge = list(G.edges(data=True))
    sum=0
    for edge in list_edge :
        sum+=edge[2]['weight']
        
    avg = sum/len(G.edges())
    print("avrage weighted: ", avg)
    
    return avg

def addEdgeRanom(G, numEdgeAdded, list_edges_with_lessDegreeAvg, minElement, minElement2):
    '''
    Create a new random edge and delete one of its current edge if del_orig is True.
    :param graph: networkx graph
    :param del_orig: bool
    :return: networkx graph
    '''
    print("===================================================== add rendom egde")
    graph=G.copy()
    edges = list(graph.edges)
    
    listEdgesAdded = []


    print("list_edges_with_lessDegreeAvg:",len(list_edges_with_lessDegreeAvg))
   
    avg_weighted = avg_wieghted_edge(G)
    
    num_list=len(list_edges_with_lessDegreeAvg)-1
    for i in range(0, numEdgeAdded):
        
        # random edge choice
        nodeA = random.randint(0,num_list)
#         print("noda", nodeA, "num: ", num_list)
#         print(list_edges_with_lessDegreeAvg[nodeA])
        random_weighted=random.uniform(minElement, minElement2)
        listEdgesAdded.append((list_edges_with_lessDegreeAvg[nodeA][0], list_edges_with_lessDegreeAvg[nodeA][1], random_weighted))

        graph.add_edge(list_edges_with_lessDegreeAvg[nodeA][0], list_edges_with_lessDegreeAvg[nodeA][1],weight=random_weighted)
        del list_edges_with_lessDegreeAvg[nodeA]
        num_list-=1
        
    print(numEdgeAdded, "edge added with Random to graph!!")
    return graph, listEdgesAdded

def od_community(matrix):
    corelist, layerlist = f_onion_decomposition.compute(matrix)
#     print("core list:  ",  sorted(corelist))
#     print("layer list: ", sorted(layerlist))
    # Get the maximum element from a  array corelist
    maxElement = np.amax(corelist)
    list_nodes_anomaly = []
    num_comunity = 1
    index = 0
    while(num_comunity < maxElement+1):
        index = 0
        for core in corelist:
            if num_comunity == core:
                list_nodes_anomaly.append(index)
            index = index+1
        num_comunity = num_comunity+1
    print("---------------------od")
    return list_nodes_anomaly, layerlist

def smart_edge_add(G,list_node_anomaly, numEdgeAdded, minElement):
    list_degree = sorted(G.degree() , reverse=False, key=lambda x: x[1])
    print()
    G_new=G.copy()
    indx=0
    listEdgesAdded = []

    index_node=0
    j_id=0
    while (indx<numEdgeAdded):
    #     print(idx, item)
        if index_node<(len(list_node_anomaly)/15):
            i,j = list_node_anomaly[0][index_node], list_node_anomaly[0][index_node+1]
            if not(G.has_edge(i,j)):
                if minElement !=0 and minElement>=0.5:
                    random_weighted=random.uniform(minElement-0.5, minElement)
                elif minElement<0.5 and minElement>0.4:
                    random_weighted=random.uniform(minElement-0.4, minElement)
                elif minElement<0.4 and minElement>0.3:
                    random_weighted=random.uniform(minElement-0.3, minElement)
                elif minElement<0.3 and minElement>0.2:
                    random_weighted=random.uniform(minElement-0.2, minElement)
                elif minElement<0.2 and minElement>0.1:
                    random_weighted=random.uniform(minElement-0.1, minElement)
                elif minElement<0.1 and minElement>0.000000001:
                    random_weighted=random.uniform(minElement-0.09, minElement)
                else:
                    random_weighted=0
                
                G_new.add_edge(i, j, weight=random_weighted)
                listEdgesAdded.append((i,j, random_weighted))    
                print("j: ", j_id, i,j, random_weighted)
                j_id+=1
                indx+=1
        else:
            index_node=0
            G3, matrix = f_graph.draw_graph(G_new)
            list_node_anomaly = od_community(matrix)
        index_node+=1

    print(numEdgeAdded,"add anomaly!")
    return G_new, listEdgesAdded
