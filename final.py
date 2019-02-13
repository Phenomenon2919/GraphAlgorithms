import operator
import collections
import sys
INT_MAX = 999999                    #Constant Value to denote infinity while implementing dijkstra's algorithm
INP_FILE = "input.dat"              #Stores the name of the input file

#DNode Class is used as structure by each vertex to store values that are used in dijkstra's algorithm
#'name' stores name of the vertex
#'dist' stores the distance/cost of the current vertex from the root vertex
#'path' stores the name of the vertex which forms the path from the root to the current vertex
#'known' acts like flag to denote whether a node/vertex has been fully mapped out in dijkstra's algorithm; 0: Unmapped, 1: Mapped
class DNode:

    def __init__(self,name):
        self.name = name
        self.dist = INT_MAX
        self.path = None
        self.known = 0

#Vertex class is used as a structure to denote the nodes of a graph
#VertexNum is integer variable that serves as index used for reading the variable number from the adjecency list
#           and assigning the alphabet name to the vertex
class Vertex:
    VertexNum = 0

    #Constructor for the objects of Vertex class
    def __init__(self):
        self.name = chr(ord("A") + Vertex.VertexNum)        #stores the name of the vertex as alphabet character
        Vertex.VertexNum += 1                               #VertexNum is incremented after every name assignment
        self.indegree = 0                                   #stores the number of incoming edges from other vertices
        self.dfsnum = None                                  #stores the dfs number; essential in articulation point calculation
        self.status = None                                  #stores the status of the vertex i.e. "Visited","In Queue" or None
        self.adj_list=[]                                    #list of all the adjecent vertices to the current vertex 
        self.rev_adj_list = []                     #list of all the adjecent vertices to the current vertex with all the edges reversed
        self.parent = None                              #points to the parent vertex of the current vertex
        self.low = None                                 #stores the dfs number of the adjecent vertex with lowest dfs number
        self.node = DNode(self.name)                    #creates DNode structure object for the current vertex

#Edge class is a structure to denote the edges of the graph
#EdgeNum keeps track of the number of edges (object) created for a graph
class Edge:
    EdgeNum = 1

    #Constructor of the objects of Edge class
    def __init__(self):
        self.name = Edge.EdgeNum
        Edge.EdgeNum += 1                               #EdgeNum is incremented, so as to name every new next edge
        self.weight = None                              #stores the weight/cost of the edge between two nodes (used only for debugging purpose)
        self.start = None                               #stores the begin point of current edge (used only for debugging purpose)
        self.end = None                                 #stores the end point of current edge (used only for debugging purpose)

#Graph class is structure to denote a graph and all its properties
class Graph:

    #Constructor for objects of Graph Class; takes 2 arguements: file pointer to input file, number of vertices for the graph 
    def __init__(self, filep, noOfVertex):
        self.ver_list = []                              #list to store all the vertices in the graph
        self.edge_dict = {}                             #dictionary to store the edges present in the graph; (key,value) = ((start,end),cost)
        self.edge_dict_trans = {}                       #dictionary to store the edges present in the transpose graph
        self.noOfVertex = noOfVertex                    #stores number of vertices in the current graph
        self.artiPts = []                               #list to store the articulation points in the graph
        self.root = -1                                  #stores the index of root node of graph
        self.count = 1                                  #stores the number of vertices explored yet to assign dfs number to vertices
        
        #loop to add all the vertices to graph based on the number of vertices present
        for i in range(noOfVertex):
            self.ver_list.append(Vertex())

        #loop to read the adjecency list
        for i in range(noOfVertex):
            #reading the number of adjecent vertices to the vertex in consideraton
            line = filep.readline().split()
            noofadj = int(line[0])
            line = line[1:]

            #reading the index of adjecent vertices and its cost from current vertex and adding the same to the adjecency list
            #The edge dictionary and the transpose edge dictionary has a structure 
            #key,value = (tuple(start Vertex name,end Vertex name):cost)
            for j in range(noofadj):
                w = int(line[j*2])-1
                self.ver_list[i].adj_list.append(self.ver_list[w])
                self.ver_list[w].indegree += 1                                      #updating the indegree of the current vertex
                self.edge_dict[(self.ver_list[i].name,self.ver_list[w].name)] = int(line[j*2+1])
                self.edge_dict_trans[(self.ver_list[w].name,self.ver_list[i].name)] = int(line[j*2+1])

    #A function to set the status of all vertices in graph to None and reinitialize VertexNum and EdgeNum to 0
    #Called before reading a new graph or before re traversing the graph
    def reset(self):
        for i in range(self.noOfVertex):
            self.ver_list[i].status = None
        Vertex.VertexNum = 0
        Edge.EdgeNum = 0

    #A function to get the transpose of the graph
    def get_rev(self):

        #stores all the adjecent vertices to rev adjecent vertices,resets the indegree and empties the adjecent vertex list
        for i in range(self.noOfVertex):
            self.ver_list[i].rev_adj_list = self.ver_list[i].adj_list
            self.ver_list[i].adj_list = []
            self.ver_list[i].indegree = 0
        
        #reverses the adjecency list of the vertices
        for v in self.ver_list:
            for w in v.rev_adj_list:
                w.adj_list.append(v)
                w.indegree += 1

#Function to find out all the strongly connected components in the graph
#Arguements = (Graph object, Source vertex object, Output file Pointer)
#Calls DFS on the object twice: once before reversing the graph & once after
def SCC(graph,source,fileop):

    Stack = collections.deque()                             #Stack is declared
    DFS_scc_1(graph,source,Stack)                           #The first DFS call is made from the source
    
    #Loop to call DFS on all the unvisited nodes in case of a disconnected graph
    for v in graph.ver_list:                                
        if v.status != "Visited":        
            DFS_scc_1(graph, v, Stack)
            break

    #Graph is reset and transposed
    graph.reset()
    graph.get_rev()

    SCC_list = []                                       #list to store all strongly connected components
    comp_list = []                                      #Component list to store the Vertices of each strongly connected component

    #Loop to pop each Vertex of the graph from stack and call DFS on the reversed graph
    while len(Stack)!=0:
        top = Stack.pop()                               #pop out a vertex from stack
        if top.status == None:          
            DFS_scc_2(graph,top,comp_list)              #Second DFS call if the popped vertex is unvisited
            SCC_list.append(comp_list)                  #Add new Component list of vertices to the SCC list
            
            comp_list = []                              #Component list is reset
            

    #Writing output of the Strongly Connected Components of graph to the output file specified
    fileop.write("The strongly connected components of the sixth graph are:\n")
    for l in SCC_list:
        fileop.write("{ ")
        for n in l:
            fileop.write(n+" ")
        fileop.write("} ")
    fileop.write("\n")

#The First DFS function called for a vertex in SCC() function
#Arguement = (Graph object, Source Vertex object, Stack)
def DFS_scc_1(graph, source,S):      
    source.status = "Visited"
    for neighbour in source.adj_list:
        if neighbour.status != "Visited":
            DFS_scc_1(graph, neighbour,S)
    S.append(source)                        #pushing vertex into the Stack after completely discovering its adjecents

#The Second DFS function for a vertex in SCC() function
#Arguement = (Graph object, Source Vertex object, Component List)
def DFS_scc_2(graph, source,lst):  
    source.status = "Visited"
    lst.append(source.name)                 #adding vertex to component list after visiting it
    for w in source.adj_list:
        if w.status != "Visited":     
            DFS_scc_2(graph, w, lst)

#Function definition to print the Shortest Path table after execution Dijkstra's algorithm 
#Arguement = (Graph object, Source Vertex object,Output file Pointer)       
def printTable(graph,source,fileop):
    fileop.write("\nFor the second graph:\n")
    for x in graph.ver_list:
        fileop.write("Shortest path from "+source.name+" to "+x.name+": "+x.node.path+"(distance = "+str(x.node.dist)+")\n")

#Function to find out all the articulation points in the graph
#Arguements = (Graph object, Source Vertex object)
def articulation(graph,source):
    
    #The dfsnum and low of the current vertex are set in accordance with the count variable in the Graph object
    #Count is incremented for the next vertex
    source.dfsnum = graph.count
    source.low = graph.count
    graph.count += 1

    #current vertex status is set to "Visited"
    source.status = "Visited"

    #Loop for going through every adjecent vertex of the current vertex
    for w in source.adj_list:
        if w.status == None:                        #check if status of neighbouring vertex is unvisited
            w.parent = source                       #parent attribute of the neigbour is set to the current vertex
            articulation(graph,w)                   #recursive call for the function made to the neighbour
            
            #After the neighbour is explored, check if low of the neighbour is greater than/equal to dfsnum of the current vertex
            #if so then the current vertex is an articulation point
            if(w.low >= source.dfsnum):

                #condition to check if the current vertex is root, it needs to have more than a child to be considered articulation point
                if source == graph.ver_list[graph.root]:
                    c = 0
                    for x in graph.ver_list:
                        if x.parent == source:
                            c += 1
                    if c > 1:
                        if source not in graph.artiPts:
                            graph.artiPts.append(source)           #appending the current vertex to the graphs articualtion pt. list
                else:
                    if source not in graph.artiPts:
                        graph.artiPts.append(source)
            if source.low > w.low:                                  #updating the low of the current vertex
                source.low = w.low
        elif source.parent != w:                            #updating low of current vertex if they are adjecent to a Visited node
            if source.low > w.dfsnum:
                source.low = w.dfsnum

#Function to find the shortest path from each vertex to the current vertex
#Arguement = (Graph object, Source Vertex object, Distance of the current node from the root node, Flag to check the fn call number)
def dijkstra(graph,source,dist,circ=0):

    #setting known = 1 for current vertex i.e. Mapped
    source.node.known = 1
    #condition to check if the call is made from the root
    #if so set dist = 0 and path = source object name
    if circ==0:
        source.node.dist = 0
        source.node.path = source.node.name
    adj_ver = {}          #Dictionary to store (key,value) = (Adjecent Vertex object, Distance of the vertex from source via current vertex)

    #Loop updates the distance of all adjecent vertex from the root based on the current vertex
    for w in source.adj_list:
        temp_dist = dist + graph.edge_dict[(source.name,w.name)]
        if w.node.dist>=temp_dist:
            w.node.dist = temp_dist
            w.node.path = source.name
        if w.node.known == 0:                       #add vertex and distance to dictionary if Vertex not yet known
            adj_ver[w] = w.node.dist

    #checking if there are still any vertices not known
    #if so, sort the dictionary as tuple according to the shortest distance, and recursively call this function for the corresponding vertices
    if len(adj_ver)>0:
        adj_ver = sorted(adj_ver.items(), key=operator.itemgetter(1))
        for x in adj_ver:
            if x[0].node.known == 0:
                dijkstra(graph,x[0],x[1],1)

#Function to find the topological ordering of the vertices in the graph
#Arguement = (Graph object, Output file Pointer)
def topological(graph,fileop):
    t_num = 0                           #Create a counter for topological numbering of vertices
    q = collections.deque()             #Queue designed storing each vertex that has indegree = 0
    
    #Loop to check for vertices int he unaltered graph with indegrre = 0
    for v in graph.ver_list:
        if v.indegree == 0:
            q.append(v)
            v.status = "In queue"               #Status of each such vertex set to "In queue"

    fileop.write("The topological sort of the first graph is:\n")
    fileop.write("VERTEX\tNUMBER\n")
    
    #Loop to pop each vertex and decrement the indegree of each adjecent vertex
    while len(q)!=0:
        v = q.popleft()
        v.status = "Visited"            #Status of current vertex changed to "Visited"

        t_num = t_num + 1               #Counter increased when a vertex is visited
        fileop.write(v.name+"\t")

        #Loop to decrement the indegree of each adjecent vertex, and append it to queue if their indegree becomes 0
        for w in v.adj_list:
            if w.status == None:
                w.indegree -= 1
                if w.indegree == 0:
                    q.append(w)
                    w.status = "In queue"
        
        #Output to file specified
        fileop.write("-->\t")
        fileop.write(str(t_num)+"\n")
    #Condition to check if there is a cycle in the graph
    if t_num != graph.noOfVertex:
        fileop.write("\nThere is a cycle in the graph")

#Function that performs 'find' part of the union-find combo
#This function checks if the edge formed is between vertices of the same group
#if so, it would indicate a cycle, and so returns False, else True
#Arguement = (Graph object, Source name, Destination name, Group Set [List])
#Return Value: (True/False based on if there is a cycle, Source Vertex Index, Destination Vertex Index)
def find(graph,src,dest,lst):

    source = None
    s_index = -1
    destination = None
    d_index = -1
    #Loop to find the index of the source vertex using its name
    for i in range(graph.noOfVertex):
        if graph.ver_list[i].name == src:
            source = graph.ver_list[i]
            s_index = i
            break
    #Loop to find the index of the destination vertex using its name
    for i in range(graph.noOfVertex):
        if graph.ver_list[i].name == dest:
            destination = graph.ver_list[i]
            d_index = i
            break

    #Condition to check for a cycle: if their correspoding value in the Group set is equal
    #if so, it indicates they belong to same group and so already connected
    #The current edge if added to the spanning tree would create a cycle
    if lst[s_index] != lst[d_index]:
        return True,s_index,d_index
    else:
        return False,s_index,d_index

#Function that performs the 'union' part in union-find combo
#This function forms a connection between the source and destination of the edge
#Arguement (Graph object, Source Vertex Index, Destination Vertex Index, Group Set [List])
def union(graph,s_index,d_index,lst):

    #Loop to change the values of all the Vertices in the destination group to those in the source group in the Group set
    for i in range(graph.noOfVertex):
        if lst[i] == lst[d_index]:
            lst[i] = lst[s_index]


#Function to find the minimum spanning tree for a graph using Kruskal's algorithm
#Arguements = (Graph Object, Output File Pointer)
def kruskal(graph,fileop):

    dist =  0                           #variable stores the total distance for traversing the minimum spanning tree
    disj_set = []                       #list to store the disjoint set
    group_set = []                      #list to store group number of each vertex

    #Loop initializes the group number of each vertex as its own index
    for i in range(graph.noOfVertex):
        group_set.insert(i,i)

    #Sort the edges of the edge dictionary in graph object as a tuple based on their weight
    sort_edge = sorted(graph.edge_dict.items(), key=operator.itemgetter(1))

    #Loop to traverse through the edges
    for x in sort_edge:
        src = x[0][0]           #stores Source Vertex Name
        dest = x[0][1]          #stores Destination Vertex Name
        cost = x[1]             #stores cost/weight of the edge

        #calling the find() function; Also returns the source index and destinaton index
        result,s_index,d_index = find(graph,src,dest,group_set)         

        #if no cycle formed, then union the vertices and add the edge top the disjoint set
        #Add the cost of the edge to the distance present
        if result == True:
            union(graph,s_index,d_index,group_set)
            disj_set.append(x[0])
            dist += cost
    
    #Output
    fileop.write("\nThe edges in the minimum spanning tree for the third graph are:\n")
    for x in disj_set:
        fileop.write("("+x[0]+","+x[1]+") ")
    fileop.write("\nIts cost is "+str(dist)+"\n\n")

#main() part of function begins from here
#
#
#
#Two file pointers: One to read the input from "input.dat", Second to write output to file passed as arguement
filep = open(INP_FILE,"r")
fileop = open(sys.argv[1],"w")

#Perform topological sort on graph 1
graph1 = Graph(filep,7)
topological(graph1,fileop)
graph1.reset()

#Find the shortest path of all vertices to the root using Dijkstra's algorithm on graph 2
#and print the table for the same
graph2 = Graph(filep,7)
dijkstra(graph2,graph2.ver_list[0],0)
printTable(graph2,graph2.ver_list[0],fileop)
graph2.reset()

#Find th minimum spanning tree of graph 3 using Kruskal's algorithm
graph3 = Graph(filep,7)
kruskal(graph3,fileop)
graph3.reset()

#Find the articulation points for graph 4 after reading from the input file the index of root
graph4 = Graph(filep,7)
root = filep.readline().split()
graph4.root = int(root[0]) - 1
articulation(graph4,graph4.ver_list[graph4.root])
#Output the name of all articularion point in graph 4
fileop.write("For the fourth graph, the articulation points are:\n")
for v in graph4.artiPts:
    if v != graph4.ver_list[graph4.root]:
        fileop.write(v.name+"\n")
    else:
        fileop.write(v.name+"(root of the dfs tree)\n")
fileop.write("\n")
graph4.reset()

#Find the articulation points for graph 5 after reading from the input file the index of root
graph5 = Graph(filep,7)
root = filep.readline().split()
graph5.root = int(root[0]) - 1
articulation(graph5,graph5.ver_list[graph5.root])
#Output the name of all articularion point in graph 5
fileop.write("For the fifth graph, the articulation points are:\n")
for v in graph5.artiPts:
    if v != graph5.ver_list[graph5.root]:
        fileop.write(v.name+"\n")
    else:
        fileop.write(v.name+"(root of the dfs tree)\n")
fileop.write("\n")
graph5.reset()

#Find all the strongly connected components for graph 6
graph6 = Graph(filep,7)
SCC(graph6,graph6.ver_list[0],fileop)
fileop.write("\n")
graph6.reset()

#Close the file pointers
filep.close()
fileop.close()