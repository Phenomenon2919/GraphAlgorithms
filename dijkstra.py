import operator
INT_MAX = 999999
INP_FILE = "dijk_input.dat"
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
        
def printTable(graph,source):

        fileout = open("dijkout.dat","w")
        fileout.write("\nFor the second graph:\n")
        for x in graph.ver_list:
            fileout.write("Shortest path from "+source.name+" to "+x.name+": "+x.node.path+"(distance = "+str(x.node.dist)+")\n")


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


def dijkstra(graph,source,dist,circ=0):

    #T.row_list[DNode(source)].known = 1
    source.node.known = 1
    if circ==0:
        #T.row_list[DNode(source)].dist = 0
        source.node.dist = 0
        source.node.path = source.node.name
    adj_ver = {}
    #dist = 0

    for w in source.adj_list:
        temp_dist = dist + graph.edge_dict[(source.name,w.name)]
        if w.node.dist>=temp_dist:
            w.node.dist = temp_dist
            w.node.path = source.name
        if w.node.known == 0:
            adj_ver[w] = w.node.dist

    if len(adj_ver)>0:
        adj_ver = sorted(adj_ver.items(), key=operator.itemgetter(1))
        for x in adj_ver:
            if x[0].node.known == 0:
                dijkstra(graph,x[0],x[1],1)

    


g = Graph(7)
dijkstra(g,g.ver_list[0],0)
printTable(g,g.ver_list[0])