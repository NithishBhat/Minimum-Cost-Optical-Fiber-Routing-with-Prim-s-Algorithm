import osmnx as ox
import heapq

import math

import matplotlib.pyplot as plt
import time

#use the latest libaries and i recommend sypyder anaconda 
#pip install matplotlib
#pip install osmnx



# there is a RAM bottle neck for this progarm,
# it fails to generate dense grapgh for 100k datapoint 

def get_node_edge_coords(places):
    """
    takes a list of locations and gives node and edge coordinates from the 
    open street map dataset.
    """
    #API quries the grapgh to get street coordinates dataset
    df = ox.graph_from_place(places, network_type="drive")
    #API gives a dataframe filled with data not needed for this project
    #so just extrating the nodes and edges
    nodes, edges = ox.graph_to_gdfs(df)
    node_coords = []
    # making a list of node coordinates
    for x, y in zip(nodes['x'], nodes['y']):
        node_coords.append((x, y))
    edge_coords = []
    #edge point consists of several datapoints  as a geometry object 
    #we just need start and end point for the edge we can ditch the rest
    #Total two data points give the edge location.
    #we make a list of those datapoints.
    for geom in edges.geometry:
        start = geom.coords[0] #pickin firsst
        end = geom.coords[-1]#picking last
        edge_coords.append((start, end))
    return node_coords, edge_coords



def build_adj_list(nodes, edges):
    """
    uses nodes and edges coordinate list as input and transforms it into a 
    adjacency list. a list of weights that are distances between the
    nodes or vertexes
    """
    index_map = {}
    for i, node in enumerate(nodes):
        index_map[node] = i
    adj = {}
    for i in range(len(nodes)):
        adj[i] = []
    for a, b in edges:
        i = index_map[a]
        j = index_map[b]
        # it return the euclidean distance between the two coordinate points
        dist = math.hypot(b[0] - a[0], b[1] - a[1])
        adj[i].append((j, dist))
        adj[j].append((i, dist))
    return adj

def filter_knn(adj, k):
    """
    takes the adjacency list and the number of neighbours we want to pick for
    each vertexthen gives back adj(n*k) list with exactly k shortest edge 
    weights for each vertex 
    """
    filtered = {} 
    for node, neighbors in adj.items():
        neighbors.sort(key=lambda x: x[1])# sort list of edge weights of a vertex
        filtered[node] = neighbors[:k]# pick k smallest edge weights from that 
    return filtered




def prim_mst(adj, nodes):
    """
    takes in adjacency list and nodes , traverses through the smallest edge 
    weights from node to node and after all nodes are visited returns the 
    mst edges.

    """
    visited = set() #stores nodes already visisted
    mst = []#stores mst edges
    heap = []

    # taking a random source node
    for start_node in adj:
        break

    visited.add(start_node)

    # pushing all edges from the start node a the heap

    start_edges = adj[start_node]
    for pair in start_edges:
        neighbor = pair[0]
        weight = pair[1]
        entry = (weight, start_node, neighbor)
        heapq.heappush(heap, entry)


    # keeping looping untill we visit all nodes ,

    while heap and len(visited) < len(adj):
        # removing the edge with the smallest weight from the heap
        weight, u, v = heapq.heappop(heap)
        #if node is already visited we  skip it and check next edge 
        if v in visited:
            continue
        #else add the node to visited
        visited.add(v)

        # add the edge to the final mst edge list 
        if nodes is not None:
            mst.append((nodes[u], nodes[v]))
        else:
            mst.append((u, v, weight))

        # pushing in edges from the newly added node
        for nbr, w in adj[v]:
            if nbr not in visited:
                heapq.heappush(heap, (w, v, nbr))

    return mst


def Plot_graph(nodes, edges, plot_name):
    """
    takes in nodes ,edge and  plotname and plots a graph , visible in the plots
    section in spyder anaconda

    """
    fig, ax = plt.subplots()
    ax.set_title(plot_name)
    for (lon1, lat1), (lon2, lat2) in edges:
        ax.plot([lon1, lon2], [lat1, lat2], linewidth=1)
    lons, lats = zip(*nodes)
    ax.scatter(lons, lats, s=2)
    ax.set_aspect('equal')
    plt.show()
    
    
def make_dense(nodes):
    """
    takes in nodes and returns list of edges such that every vertex is
    connected to every other vertex in the grapgh

    """
    dense = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            dense.append((nodes[i], nodes[j]))
    return dense


import networkx as nx

def make_dense_percent(nodes, density, seed=42):

    n = len(nodes)
    p = density/100 if density > 1 else density
    k = int(round(p * n*(n-1)/2))
    G = nx.gnm_random_graph(n, k, seed=seed)
    m = dict(enumerate(nodes))
    return [(m[u], m[v]) for u, v in G.edges()]



# # First, pull the nodes and edges from the API for a place and create a dataset
# #of node coordinates and edge coordinates then create a adjacency list (dict(list))
# places = [
#     {"city": "Los Angeles", "state": "California", "country": "USA"},
#     #{"city": "Los Angeles", "state": "California", "country": "USA"}
# ]


# print(places)
# nodes,edges=get_node_edge_coords(places)
# adj=build_adj_list(nodes, edges)
# print("nodes:"+str(len(nodes))+" edges:"+str(len(edges)))
# #Plot_graph(nodes, edges, "dataset")
# #------------------------------------------------------------------------------
# # use knn filter function  to remove edges that are unlikey to be in the final MST
# start=time.time()#measure start time at this point
# filtered_adj=filter_knn(adj, k=10)
# mst_edges=prim_mst(filtered_adj, nodes)
# end=time.time()#measure end time at this point 
# print("prim's MST with knn filter clocks at "+str(end-start)+" secs")
# #Plot_graph(nodes, mst_edges , "Prim's MST on sparse graph filtered with Knn")


# # running MST on sparse graph without any filtering
# #the sparse graph came with the dataset 
# start=time.time()
# mst_edges=prim_mst(adj, nodes)
# end=time.time()
# print("prim's MST clocks at "+str(end-start)+" secs\n")
# #Plot_graph(nodes, mst_edges , "Prim's MST on sparse graph")
# #but this doesnt create a true MST since the sparse grapgh
# # doesnt have the MST subset
#dense grapgh gurantees MST subset


#----------------------------------------------------------------------------
# #make a dense grapgh from the given nodes and then build adjacency for that grapgh
# dense_edges=make_dense(nodes)
# dense_adj=build_adj_list(nodes,dense_edges)

# Plot_graph(nodes, dense_edges, "dataset")
# #Use knn to filter out unlikey to be in the final MST edges
# start=time.time()
# filtered_adj=filter_knn(dense_adj, k=10)
# mst_edges=prim_mst(filtered_adj, nodes)
# end=time.time()
# print("dense graphs's prim's MST with knn filter clocks at "+str(end-start)+" secs")
# Plot_graph(nodes, mst_edges , "Prim's MST on dense graph filtered with Knn")

# #running prim on dense graph without any filtering
# start=time.time()
# mst_edges=prim_mst(dense_adj, nodes)
# end=time.time()
# print("dense graphs's prim's MST clocks at "+str(end-start)+" secs")
# Plot_graph(nodes, mst_edges , "Prim's MST on dense graph")



#------------------------------------------------------------------------------


# dense_edges=make_dense_percent(nodes, 0.1)
# dense_adj=build_adj_list(nodes,dense_edges)

# print("nodes:"+str(len(nodes))+" dense_edges:"+str(len(dense_edges)))
# #Plot_graph(nodes, dense_edges, "dataset")
# #Use knn to filter out unlikey to be in the final MST edges
# start=time.time()
# filtered_adj=filter_knn(dense_adj, k=10)
# mst_edges=prim_mst(filtered_adj, nodes)
# end=time.time()
# print("dense graphs's prim's MST with knn filter clocks at "+str(end-start)+" secs")
# #Plot_graph(nodes, mst_edges , "Prim's MST on dense graph filtered with Knn")

# #running prim on dense graph without any filtering
# start=time.time()
# mst_edges=prim_mst(dense_adj, nodes)
# end=time.time()
# print("dense graphs's prim's MST clocks at "+str(end-start)+" secs")
# #Plot_graph(nodes, mst_edges , "Prim's MST on dense graph")





places_city=[   
    [
        {"city": "Beverly Hills", "state": "California", "country": "USA"},
    ]
    ]


for i in places_city:
    
    # First, pull the nodes and edges from the API for a place and create a dataset
    #of node coordinates and edge coordinates then create a adjacency list (dict(list))
    places = [
        {"city": "Los Angeles", "state": "California", "country": "USA"},
        #{"city": "Los Angeles", "state": "California", "country": "USA"}
    ]
    
    
    print(i)
    nodes,edges=get_node_edge_coords(i)
    adj=build_adj_list(nodes, edges)
    print("nodes:"+str(len(nodes))+" edges:"+str(len(edges)))
    #Plot_graph(nodes, edges, "dataset")
    #------------------------------------------------------------------------------
    # use knn filter function  to remove edges that are unlikey to be in the final MST
    start=time.time()#measure start time at this point
    filtered_adj=filter_knn(adj, k=10)
    mst_edges=prim_mst(filtered_adj, nodes)
    end=time.time()#measure end time at this point 
    print("prim's MST with knn filter clocks at "+str(end-start)+" secs")
    #Plot_graph(nodes, mst_edges , "Prim's MST on sparse graph filtered with Knn")
    
    
    # running MST on sparse graph without any filtering
    #the sparse graph came with the dataset 
    start=time.time()
    mst_edges=prim_mst(adj, nodes)
    end=time.time()
    print("prim's MST clocks at "+str(end-start)+" secs\n")
    #Plot_graph(nodes, mst_edges , "Prim's MST on sparse graph")
    #but this doesnt create a true MST since the sparse grapgh
    # doesnt have the MST subset
    #dense grapgh gurantees MST subset
    
    
    #----------------------------------------------------------------------------
    # #make a dense grapgh from the given nodes and then build adjacency for that grapgh
    # dense_edges=make_dense(nodes)
    # dense_adj=build_adj_list(nodes,dense_edges)
    
    # Plot_graph(nodes, dense_edges, "dataset")
    # #Use knn to filter out unlikey to be in the final MST edges
    # start=time.time()
    # filtered_adj=filter_knn(dense_adj, k=10)
    # mst_edges=prim_mst(filtered_adj, nodes)
    # end=time.time()
    # print("dense graphs's prim's MST with knn filter clocks at "+str(end-start)+" secs")
    # Plot_graph(nodes, mst_edges , "Prim's MST on dense graph filtered with Knn")
    
    # #running prim on dense graph without any filtering
    # start=time.time()
    # mst_edges=prim_mst(dense_adj, nodes)
    # end=time.time()
    # print("dense graphs's prim's MST clocks at "+str(end-start)+" secs")
    # Plot_graph(nodes, mst_edges , "Prim's MST on dense graph")
    
    
    
    #------------------------------------------------------------------------------
    
    
    dense_edges=make_dense_percent(nodes, 0.05)
    dense_adj=build_adj_list(nodes,dense_edges)
    
    print("nodes:"+str(len(nodes))+" dense_edges:"+str(len(dense_edges))+"Percent dense=5")
    #Plot_graph(nodes, dense_edges, "dataset")
    #Use knn to filter out unlikey to be in the final MST edges
    start=time.time()
    filtered_adj=filter_knn(dense_adj, k=10)
    mst_edges=prim_mst(filtered_adj, nodes)
    end=time.time()
    print("dense graphs's prim's MST with knn filter clocks at "+str(end-start)+" secs")
    #Plot_graph(nodes, mst_edges , "Prim's MST on dense graph filtered with Knn")
    
    #running prim on dense graph without any filtering
    start=time.time()
    mst_edges=prim_mst(dense_adj, nodes)
    end=time.time()
    print("dense graphs's prim's MST clocks at "+str(end-start)+" secs")
    #Plot_graph(nodes, mst_edges , "Prim's MST on dense graph")
    print("#############################################################")