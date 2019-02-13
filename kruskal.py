import collections
import operator
import heapq
INP_FILE = "kruskal_input.dat"
class Vertex:
    VertexNum = 0

    def __init__(self):
        self.name = chr(ord("A") + Vertex.VertexNum)
        Vertex.VertexNum += 1
        self.indegree = 0
        self.dfsnum = None
        self.indegree = 0
        self.status = None
        self.adj_list=[]
        self.parent = None
        self.color = None
        self.low = None

class Edge:
    EdgeNum = 1

    def __init__(self):
        self.name = Edge.EdgeNum
        Edge.EdgeNum += 1
        self.weight = None
        self.classifi = None
        self.start = None
        self.end = None

class Graph:

    def __init__(self, noOfVertex):
        self.ver_list = []
        self.edge_dict = {}
        self.noOfVertex = noOfVertex
        self.artiPts = []
        filep = open(INP_FILE,"r")

        for i in range(noOfVertex):
            self.ver_list.append(Vertex())

        for i in range(noOfVertex):
            line = filep.readline().split()
            noofadj = int(line[0])
            line = line[1:]

            for j in range(noofadj):
                w = int(line[j*2])-1
                self.ver_list[i].adj_list.append(self.ver_list[w])
                self.ver_list[w].indegree += 1
                self.edge_dict[(self.ver_list[i].name,self.ver_list[w].name)] = int(line[j*2+1])

def find(graph,src,dest,lst):

    source = None
    s_index = -1
    destination = None
    d_index = -1
    for i in range(graph.noOfVertex):
        if graph.ver_list[i].name == src:
            source = graph.ver_list[i]
            s_index = i
            break
    for i in range(graph.noOfVertex):
        if graph.ver_list[i].name == dest:
            destination = graph.ver_list[i]
            d_index = i
            break
    #print s_index," ",d_index
    #print lst[s_index]," ",lst[d_index]
    if lst[s_index] != lst[d_index]:
        return True,s_index,d_index
    else:
        return False,s_index,d_index

def union(graph,s_index,d_index,lst):

    for i in range(graph.noOfVertex):
        if lst[i] == lst[d_index]:
            lst[i] = lst[s_index]



def kruskal(graph):

    fileout = open("krusout.dat","w")
    count = graph.noOfVertex
    dist =  0
    disj_set = []
    group_set = []
    for i in range(count):
        group_set.insert(i,i)
    #print group_set
    sort_edge = sorted(graph.edge_dict.items(), key=operator.itemgetter(1))

    for x in sort_edge:
        src = x[0][0]
        dest = x[0][1]
        cost = x[1]
        #print "+",x[0],"+"

        result,s_index,d_index = find(graph,src,dest,group_set)

        if result == True:
            union(graph,s_index,d_index,group_set)
            disj_set.append(x[0])
            dist += cost
    fileout.write("\nThe edges in the minimum spanning tree for the third graph are:\n")
    for x in disj_set:
        fileout.write("("+x[0]+","+x[1]+") ")
    fileout.write("\nIts cost is "+str(dist)+"\n")
    #while count > 0:

g = Graph(7)
kruskal(g)
