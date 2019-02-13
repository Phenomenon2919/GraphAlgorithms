INP_FILE = "art_input.dat"
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
        line = filep.readline().split()
        self.root = int(line[0]) - 1
        self.count = 1


    def reset(self):
        for i in range(self.vertexCount):
            self.ver_list[i].status = None

def articulation(graph,source):
    #graph.reset()
    source.dfsnum = graph.count
    source.low = graph.count
    graph.count += 1
    #print(source.name,"--",source.dfsnum,"--",source.low)
    source.status = "visited"
    for w in source.adj_list:
        if w.status == None:
            w.parent = source
            articulation(graph,w)
            if(w.low >= source.dfsnum):
            	if source == graph.ver_list[graph.root]:
            		c = 0
            		for x in graph.ver_list:
            			if x.parent == source:
            				c += 1
            		if c > 1:
            			if source not in graph.artiPts:
            				graph.artiPts.append(source)
                else:
	                if source not in graph.artiPts:
	                    graph.artiPts.append(source)
            if source.low > w.low:
                source.low = w.low
        elif source.parent != w:
            if source.low > w.dfsnum:
                source.low = w.dfsnum

g=Graph(7)
#print(g.ver_list[g.root].name)
fileout = open("artiout.dat","w")
articulation(g,g.ver_list[g.root])
fileout.write("For the fourth graph, the articulation points are:\n")
for v in g.artiPts:
    if v != g.ver_list[g.root]:
        fileout.write(v.name+"\n")
    else:
        fileout.write(v.name+"(root of the dfs tree)\n")

