INP_FILE = "1stinput.dat"


class Vertex:
    count = 0

    def __init__(self):
        self.name = chr(ord('A') + Vertex.count)
        Vertex.count += 1
        self.adjVertices = []
        self.status = None
        self.indegree = 0

    def __del__(self):
        Vertex.count -= 1


    def __cmp__(self, other):
        return self.indegree < other.indegree


class Edge:
    count = 1

    def __init__(self):
        self.label = Edge.count
        Edge.count += 1
        self.weight = 0
        self.src = None
        self.dest = None
        self.type = None

    def __del__(self):
        Edge.count -= 1


class Graph:

    def __init__(self, vertexCount):
        self.vertexCount = vertexCount
        self.vertices = []
        self.edges = {}
        fin = open(INP_FILE, "r")

        for i in range(vertexCount):
            self.vertices.append(Vertex())

        for i in range(vertexCount):
            line = fin.readline().split()
            adjVerticesCount = int(line[0])
            line = line[1:]

            for j in range(adjVerticesCount):
                neighbour = self.vertices[int(line[j*2]) - 1]
                neighbour.indegree += 1
                weight = int(line[j*2 + 1])
                self.vertices[i].adjVertices.append(neighbour)
                self.edges[(self.vertices[i], neighbour)] = weight


    def reset(self):
        for i in range(self.vertexCount):
            self.vertices[i].status = None


def DFS(graph, source, id=0, dfsTreeNum=1):       # id is used to identify the source/parent node from where DFS started
    if id == 0 and dfsTreeNum == 1:
        graph.reset()
        print()
    if id == 0:
        print("DFS Tree number", dfsTreeNum)

    source.status = "Visited"
    print(source.name, "  ", end="")
    for neighbour in source.adjVertices:
        if neighbour.status != "Visited":
            DFS(graph, neighbour, 1, dfsTreeNum)

    if id == 0:
        for vertex in graph.vertices:
            if vertex.status != "Visited":
                print()         # adding a newline for a better looking output
                DFS(graph, vertex, dfsTreeNum=dfsTreeNum+1)
                break
        if dfsTreeNum == 1:
            print()

g=Graph(7)
for i in range(7):
    print(g.vertices[i].name)
    DFS(g,g.vertices[i])
    print()