import operator
import collections
INT_MAX = 999999
INP_FILE = "strong_input.dat"
class DNode:

    def __init__(self,name):
        self.name = name
        self.dist = INT_MAX
        self.path = None
        self.known = 0

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
        self.rev_adj_list = []
        self.parent = None
        self.color = None
        self.low = None
        self.node = DNode(self.name)

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
        self.edge_dict_trans = {}
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
                self.edge_dict_trans[(self.ver_list[w].name,self.ver_list[i].name)] = int(line[j*2+1])

    def reset(self):
        for i in range(self.noOfVertex):
            self.ver_list[i].status = None

    def get_rev(self):

        for i in range(self.noOfVertex):
            self.ver_list[i].rev_adj_list = self.ver_list[i].adj_list
            self.ver_list[i].adj_list = []
            self.ver_list[i].indegree = 0
        
        for v in self.ver_list:
            for w in v.rev_adj_list:
                w.adj_list.append(v)
                w.indegree += 1

def SCC(graph,source,fileout):

    Stack = collections.deque()
    DFS_scc_1(graph,source,Stack)
    for v in graph.ver_list:
        if v.status != "Visited":        
            DFS_scc_1(graph, v, Stack)
            break

    graph.reset()
    graph.get_rev()

    SCC_list = []
    comp_list = [] 

    while len(Stack)!=0:
        top = Stack.pop()
        if top.status == None:
            DFS_scc_2(graph,top,comp_list)
            SCC_list.append(comp_list)
            
            comp_list = []
            
    fileout.write("The strongly connected components of the sixth graph are:\n")
    for l in SCC_list:
        fileout.write("{ ")
        #print "{",
        for n in l:
            fileout.write(n+" ")
            #print n," ",
        fileout.write("} ")
        #print "}"," ",
    fileout.write("\n")

def DFS_scc_1(graph, source,S):      
    source.status = "Visited"
    for neighbour in source.adj_list:
        if neighbour.status != "Visited":
            DFS_scc_1(graph, neighbour,S)
    S.append(source)

def DFS_scc_2(graph, source,lst):  
    source.status = "Visited"
    lst.append(source.name)
    for w in source.adj_list:
        if w.status != "Visited":     
            DFS_scc_2(graph, w, lst)




fileout = open("sccout.dat","w")
g = Graph(7)
SCC(g,g.ver_list[0],fileout)