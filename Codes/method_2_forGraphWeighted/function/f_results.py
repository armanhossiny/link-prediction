
import numpy as np
from networkx.algorithms import community
from networkx.algorithms.community.quality import performance
from networkx.algorithms.community.quality import modularity
from networkx.algorithms.community.quality import coverage
from function import f_onion_decomposition
from networkx.algorithms.community import greedy_modularity_communities

def results(G, matrix, algorithm_community):

    if (algorithm_community=="asyn_lpa_communities"):
        corelist, layerlist = f_onion_decomposition.compute(matrix)
        print("core list:  ",  corelist)
        print("layer list: ", layerlist)
         # Get the maximum element from a  array corelist
        maxElement = np.amax(corelist)

        nodeCore={}
        num_comunity=1
        index=0
        while(num_comunity<maxElement+1):
            nodeCore[str(num_comunity)]=[]
            index=0
            for core in corelist:
                if num_comunity==core:
                    nodeCore[str(core)].append(index)

        #     print(index)
                index= index+1
            num_comunity= num_comunity+1

        list_comunity = []
        for comunity in nodeCore:
            if len(nodeCore[comunity])!=0:
                list_comunity.append(nodeCore[comunity])
        print("list comunity: ", list_comunity)

    elif( algorithm_community =="greedy_modularity_communities"):
        communities_generator = community.girvan_newman(G)
        top_level_communities = next(communities_generator)
        list_comunity = next(communities_generator)
        sorted(map(sorted, list_comunity))

    elif (algorithm_community =="newman_greedy"):
        list_comunity = community.greedy_modularity_communities(G,'weight')
        list_comunity

   

    print("\n")
    print("algorithm community detection: ", algorithm_community)
    print("\n")
    print("modularity:  ", modularity (G, list_comunity))
    print("performance: ", performance(G, list_comunity))
    print("coverage:    ", coverage   (G, list_comunity))
