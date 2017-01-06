from Library import *
from igraph import Graph

i=0
while i<20:
	g = Graph.Erdos_Renyi(200, 0.5)
	write_graph(g,"test"+str(i))
	i+=1
