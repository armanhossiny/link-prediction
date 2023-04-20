from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community.label_propagation import asyn_lpa_communities
from networkx.algorithms.community.quality import coverage
from networkx.algorithms.community.quality import modularity
from networkx.algorithms.community.quality import performance

def percentage(percent, whole):
    return int((percent * whole) / 100.0)


# split number to N part
def split_number(x, n): 
    list_part=[]
    # If we cannot split the  
    # number into exactly 'N' parts 
    if(x < n):  
        print(-1) 
  
    # If x % n == 0 then the minimum  
    # difference is 0 and all  
    # numbers are x / n 
    elif (x % n == 0): 
        for i in range(n): 
#             print(x//n, end =" ") 
            list_part.append(x//n)
    else: 
        # upto n-(x % n) the values  
        # will be x / n  
        # after that the values  
        # will be x / n + 1 
        zp = n - (x % n) 
        pp = x//n 
        for i in range(n): 
            if(i>= zp): 
#                 print(pp + 1, end =" ") 
                list_part.append(pp+1)
            else: 
#                 print(pp, end =" ") 
                list_part.append(pp)
    return list_part

def ALC(G):
    # algorithm_community="asyn_lpa_communities"
    # print("-----------", algorithm_community)

    community=list(asyn_lpa_communities(G, weight='weight', seed=None))
    mod = modularity (G, community)
    per = performance (G, community)
    cov = coverage (G, community)
    # print("modularity:  ", mod)
    # print("performance: ", per)
    # print("coverage:    ", cov)
    return mod, per, cov

def GMC(G):
    # algorithm_community= "reedy_modularity_communities"
    # print("\n---------", algorithm_community)

    community = greedy_modularity_communities(G, weight='weight')
    mod = modularity (G, community)
    per = performance (G, community)
    cov = coverage (G, community)
    # print("modularity:  ", mod)
    # print("performance: ", per)
    # print("coverage:    ", cov)
    return mod, per, cov

def remove_anomal_edge(Graph, list_edges,alg_name):
    G = Graph.copy()
    mod_list= 0
    per_list = 0 
    cov_list = 0
    
    modularity_list =[]
    performance_list = []
    coverage_list = []
    
    print(len(G.edges()))
    percentage_10 = percentage(10, len(list_edges))
    print("numbers remove edges: ", percentage_10)
    
    num_split = split_number(percentage_10,19)
    if alg_name=="GMC":
        mod_list, per_list, cov_list = GMC(G)

        modularity_list.append(mod_list)
        performance_list.append(per_list)
        coverage_list.append(cov_list)

    elif alg_name=="ALC":
        mod_list, per_list, cov_list = ALC(G)
        modularity_list.append(mod_list)
        performance_list.append(per_list)
        coverage_list.append(cov_list)
    else:
        print("GMC or ALC, selected!!")
            
    for index_split in num_split:
        for indx in range(index_split):
            i=list_edges[0][0]
            j=list_edges[0][1]
            if G.has_edge(i, j):
                G.remove_edge(i, j)
                del list_edges[0]
            else:
                del list_edges[0]
        if alg_name=="GMC":
            mod_list, per_list, cov_list = GMC(G)
            modularity_list.append(mod_list)
            performance_list.append(per_list)
            coverage_list.append(cov_list)

        elif alg_name=="ALC":
            mod_list, per_list, cov_list = ALC(G)
            modularity_list.append(mod_list)
            performance_list.append(per_list)
            coverage_list.append(cov_list)
        else:
            print("GMC or ALC, selected!!")
    print(len(G.edges()))
    return modularity_list, performance_list ,coverage_list


def plot_result(list_CN, list_PA, list_AA, list_JC, msg_nameMetric, name_dataset):
    line_chart1 = plt.plot(range(1,len(list_CN)+1), list_CN,'b')
    line_chart2 = plt.plot(range(1,len(list_PA)+1), list_PA,'r')
    line_chart3 = plt.plot(range(1,len(list_AA)+1), list_AA,'g')
    line_chart4 = plt.plot(range(1,len(list_JC)+1), list_JC, 'c')

    axes = plt.axes()
    axes.set_ylim([0, 1])
    # plt.axis([0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0])
    # plt.style.use('ggplot')
    plt.title(msg_nameMetric,fontsize=20)
    plt.xlabel('Number of removed edges(up to 10% from the all)',fontsize=16)
    plt.ylabel('Quality',fontsize=16)
    plt.legend(['CN','PA', 'AA','JA'], loc=0,fontsize=12)
    # plt.style.use(['dark_background', 'presentation'])
    plt.grid(True)
    name_fig=name_dataset+'.png'
    plt.savefig(name_fig)
    plt.show()

