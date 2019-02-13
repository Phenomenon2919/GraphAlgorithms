import collections
import heapq
FILE = "1stinput.dat"

class Vertex():
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

class Edge():
	EdgeNum = 0

	def __init__():
		self.name = Edge.EdgeNum
		Edge.EdgeNum += 1
		self.weight = None
		self.classifi = None
		self.start = None
		self.end = None


class Graph():

	def __init__(self,noOfVertex):
		self.ver_list = []
		self.edge_dict = {}
		self.noOfVertex = noOfVertex
		filep = open(FILE,"r")

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

def topological(g):
	fileout = open("topoout.dat","w")
	t_num = 0
	q = collections.deque()
	for v in g.ver_list:
		if v.indegree == 0:
			q.append(v)
			v.status = "In queue"
	fileout.write("The topological sort of the first graph is:\n")
	fileout.write("VERTEX\tNUMBER\n")
	while len(q)!=0:
		v = q.popleft()
		v.status = "visited"

		t_num = t_num + 1
		fileout.write(v.name+"\t")

		for w in v.adj_list:
			if w.status == None:
				w.indegree -= 1
				if w.indegree == 0:
					q.append(w)
					w.status = "In queue"
		fileout.write("-->\t")
		fileout.write(str(t_num)+"\n")
	if t_num != g.noOfVertex:
		fileout.write("\nThere is a cycle in the graph")

graph1 = Graph(7)
topological(graph1)



