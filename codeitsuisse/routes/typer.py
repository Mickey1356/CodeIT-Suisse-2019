import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
from collections import defaultdict 
import sys 
  
class Heap(): 
  
    def __init__(self): 
        self.array = [] 
        self.size = 0
        self.pos = [] 
  
    def newMinHeapNode(self, v, dist): 
        minHeapNode = [v, dist] 
        return minHeapNode 
  
    # A utility function to swap two nodes of  
    # min heap. Needed for min heapify 
    def swapMinHeapNode(self, a, b): 
        t = self.array[a] 
        self.array[a] = self.array[b] 
        self.array[b] = t 
  
    # A standard function to heapify at given idx 
    # This function also updates position of nodes  
    # when they are swapped. Position is needed  
    # for decreaseKey() 
    def minHeapify(self, idx): 
        smallest = idx 
        left = 2 * idx + 1
        right = 2 * idx + 2
  
        if left < self.size and self.array[left][1] < self.array[smallest][1]: 
            smallest = left 
  
        if right < self.size and self.array[right][1] < self.array[smallest][1]: 
            smallest = right 
  
        # The nodes to be swapped in min heap  
        # if idx is not smallest 
        if smallest != idx: 
  
            # Swap positions 
            self.pos[ self.array[smallest][0] ] = idx 
            self.pos[ self.array[idx][0] ] = smallest 
  
            # Swap nodes 
            self.swapMinHeapNode(smallest, idx) 
  
            self.minHeapify(smallest) 
  
    # Standard function to extract minimum node from heap 
    def extractMin(self): 
  
        # Return NULL wif heap is empty 
        if self.isEmpty() == True: 
            return
  
        # Store the root node 
        root = self.array[0] 
  
        # Replace root node with last node 
        lastNode = self.array[self.size - 1] 
        self.array[0] = lastNode 
  
        # Update position of last node 
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
  
        # Reduce heap size and heapify root 
        self.size -= 1
        self.minHeapify(0) 
  
        return root 
  
    def isEmpty(self): 
        return True if self.size == 0 else False
  
    def decreaseKey(self, v, dist): 
  
        # Get the index of v in  heap array 
  
        i = self.pos[v] 
  
        # Get the node and update its dist value 
        self.array[i][1] = dist 
  
        # Travel up while the complete tree is not  
        # hepified. This is a O(Logn) loop 
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]: 
  
            # Swap this node with its parent 
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i 
            self.swapMinHeapNode(i, (i - 1)//2 ) 
  
            # move to parent index 
            i = (i - 1) // 2; 
  
    # A utility function to check if a given vertex 
    # 'v' is in min heap or not 
    def isInMinHeap(self, v): 
  
        if self.pos[v] < self.size: 
            return True
        return False
  
    
  
class Graph(): 
  
    def __init__(self, V): 
        self.V = V 
        self.graph = defaultdict(list)

    def getWeight(self, u, v):
        for node in self.graph[u]:
            if node[0]==v:
                return node[1]
  
    # Adds an edge to an undirected graph 
    def addEdge(self, src, dest, weight): 
  
        # Add an edge from src to dest.  A new node is 
        # added to the adjacency list of src. The node  
        # is added at the begining. The first element of 
        # the node has the destination and the second  
        # elements has the weight 
        newNode = [dest, weight] 
        self.graph[src].insert(0, newNode) 
  
        # Since graph is undirected, add an edge from  
        # dest to src also 
        newNode = [src, weight] 
        self.graph[dest].insert(0, newNode) 
  
    # The main function that prints the Minimum  
    # Spanning Tree(MST) using the Prim's Algorithm.  
    # It is a O(ELogV) function 
    def PrimMST(self): 
        # Get the number of vertices in graph 
        V = self.V   
          
        # key values used to pick minimum weight edge in cut 
        key = []    
          
        # List to store contructed MST 
        parent = []  
  
        # minHeap represents set E 
        minHeap = Heap() 
  
        # Initialize min heap with all vertices. Key values of all 
        # vertices (except the 0th vertex) is is initially infinite 
        for v in range(V): 
            parent.append(-1) 
            key.append(999999) 
            minHeap.array.append( minHeap.newMinHeapNode(v, key[v]) ) 
            minHeap.pos.append(v) 
  
        # Make key value of 0th vertex as 0 so  
        # that it is extracted first 
        minHeap.pos[0] = 0
        key[0] = 0
        minHeap.decreaseKey(0, key[0]) 
  
        # Initially size of min heap is equal to V 
        minHeap.size = V; 
  
        # In the following loop, min heap contains all nodes 
        # not yet added in the MST. 
        while minHeap.isEmpty() == False: 
  
            # Extract the vertex with minimum distance value 
            newHeapNode = minHeap.extractMin() 
            u = newHeapNode[0] 
  
            # Traverse through all adjacent vertices of u  
            # (the extracted vertex) and update their  
            # distance values 
            for pCrawl in self.graph[u]: 
  
                v = pCrawl[0] 
  
                # If shortest distance to v is not finalized  
                # yet, and distance to v through u is less than 
                # its previously calculated distance 
                if minHeap.isInMinHeap(v) and pCrawl[1] < key[v]: 
                    key[v] = pCrawl[1] 
                    parent[v] = u 
  
                    # update distance value in min heap also 
                    minHeap.decreaseKey(v, key[v]) 
  
        return self.genGraph(parent, V)

    def genGraph(self, parent, n):
        g = MSTGraph()
        cost = 0
        for i in range(1, n):
            cost += self.getWeight(parent[i], i)
            g.addEdge(parent[i], i)
            g.addEdge(i, parent[i])
        return g,cost



from collections import defaultdict 
  
# This class represents a directed graph using 
# adjacency list representation 
class MSTGraph:
  
    # Constructor 
    def __init__(self): 
  
        # default dictionary to store graph 
        self.graph = defaultdict(list) 
  
    # function to add an edge to graph 
    def addEdge(self, u, v): 
        self.graph[u].append(v) 
  
    # A function used by DFS 
    def DFSUtil(self, v, visited): 
  
        # Mark the current node as visited
        # and print it 
        visited[v] = True

        # Recur for all the vertices  
        # adjacent to this vertex 
        for i in self.graph[v]: 
            if visited[i] == False:
                self.output.append(("COPY", v))
                self.output.append(("TRANSFORM", i))
                self.DFSUtil(i, visited) 
  
    # The function to do DFS traversal. It uses 
    # recursive DFSUtil() 
    def DFS(self, v): 
        self.output = []
        # Mark all the vertices as not visited 
        visited = [False] * (len(self.graph)) 
  
        # Call the recursive helper function  
        # to print DFS traversal 
        self.DFSUtil(v, visited) 
        return self.output

#graph[u] is a list of (v, cost)
def hamming(w1, w2):
    return sum(c1!=c2 for c1,c2 in zip(w1, w2))

def solve(inp):
    verts = len(inp)
    g = Graph(verts)
    for i,s1 in enumerate(inp):
        for j,s2 in enumerate(inp):
            if s1!=s2:
                cost = hamming(s1, s2)
                g.addEdge(i,j,1+cost)
    mst,tl_cost = g.PrimMST()
    tl_cost += len(inp[0])
    # tl_cost = sum([c for u,v,c in mst]) + len(inp[0])

    # g = Prim()
    # for u,v,c in mst:
    #   ng.addEdge(u,v)
    #   ng.addEdge(v,u)

    op = mst.DFS(0)
    f = {"cost":tl_cost}
    steps = [ {"type":"INPUT", "value":inp[0]} ]
    for step in op:
        nstep = {"type":step[0], "value":inp[step[1]]}
        steps.append(nstep)
    f["steps"] = steps
    return f

@app.route('/typing-contest', methods=['POST'])
def eval_typer():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);