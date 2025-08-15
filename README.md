# Minimum Cost Optical Fiber Routing with Prim's Algorithm

The goal of the project is to find a minimum spanning tree for a graph built on coordinate points of a real world city and find the least possible time complexity optimisations to do it. I used a KNN filter as recommneded in the research paper "Fast and Memory-Efficient Approximate Minimum Spanning Tree" by Mahmood K. M. Almansoori, Andras Meszaros and Miklos Telek. The K nearest neighbour filter prunes the graph  and then running the prim's turns into a more managable O(n*k*log(n)) time complexity, if we manage to keep a low value for k then the time complexity will be drastically reduced comapred to the O(n*n*log(n)) given by vanilla prim's. I use two types of graphs, Dense and sparse. sparse graphs have very few edges and as we increase the number of edges to every vertex has an edge to every other vertex we move to a fully dense graph. Below are the time measuerments while running the program in a 16 gb ram and an intel i9 laptop.



# Matplotlib graphs

![alt text](https://github.com/NithishBhat/Minimum-Cost-Optical-Fiber-Routing-with-Prim-s-Algorithm/blob/main/dataset.png?raw=true)
![alt text](https://github.com/NithishBhat/Minimum-Cost-Optical-Fiber-Routing-with-Prim-s-Algorithm/blob/main/Prim's-MST-on-dense-graph-filtered-with-knn.png?raw=true)
![alt text](https://github.com/NithishBhat/Minimum-Cost-Optical-Fiber-Routing-with-Prim-s-Algorithm/blob/main/Prim's-MST-on-sparse-graph-filtered-with-knn.png?raw=true)









# Code output

################################################################################

nodes:649 edges:1844
prim's MST with knn filter clocks at 0.0020008087158203125 secs
prim's MST clocks at 0.0020368099212646484 secs
 
 
nodes:649 dense_edges:21028
dense graphs's prim's MST with knn filter clocks at 0.004999876022338867 secs
dense graphs's prim's MST clocks at 0.006999492645263672 secs
 
 
##################################################################################
 
[{'city': 'San Jose', 'state': 'California', 'country': 'USA'}]
 
nodes:20858 edges:49822
prim's MST with knn filter clocks at 0.049262046813964844 secs
prim's MST clocks at 0.037955522537231445 secs
 
nodes:20858 dense_edges:21751765
dense graphs's prim's MST with knn filter clocks at 7.284931898117065 secs
dense graphs's prim's MST clocks at 29.135838985443115 secs
 
 
############################################################################
 
[{'city': 'Los Angeles', 'state': 'California', 'country': 'USA'}]
 
nodes:49502 edges:135930
prim's MST with knn filter clocks at 0.15575218200683594 secs
prim's MST clocks at 0.11928176879882812 secs
 
 
nodes:49502 dense_edges:122519925
*__________Out of memory error*

###############################################################################


# Result:
The prim's running on knn pruned dense graphs give an increasingly widening runtime when compared to the vanilla prim's.


The program evetually runs out of ram due to it having to store huge number of nodes and its adjacency martrix. There is another intersiting find, when running a just large enough dataset the machine tries to push through the computing even if its out of memory and writing it to a disk. This results in knn prim's taking longer time than the vanilla prim's.



# Note:
This project was a part of  Northeastern's MSCS CS5800. its was a group project , but i am going to include the part of the project i was responsible for. That is the coding  of prims and runtime measurements. The overall project was to find the Minimum-Cost-Optical-Fiber-Routing with 2 different algorithms and then comapre the efficiences of them both and the accuracy of the final minimum spanning tree. we were given 2 weeks to complete the project. but i had to get it done in one week to meet the testing and documentation deadline.
