import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def dependencyManager(modules, dependencyPairs):

    #Python program to print topological sorting of a DAG 
    from collections import defaultdict 
      
    #Class to represent a graph 
    class Graph: 
        def __init__(self,vertices): 
            self.graph = defaultdict(list) #dictionary containing adjacency List 
            self.V = vertices #No. of vertices 
      
        # function to add an edge to graph 
        def addEdge(self,u,v): 
            self.graph[u].append(v) 
      
        # A recursive function used by topologicalSort 
        def topologicalSortUtil(self,v,visited,stack): 
      
            # Mark the current node as visited. 
            visited[v] = True
      
            # Recur for all the vertices adjacent to this vertex 
            for i in self.graph[v]: 
                if visited[i] == False: 
                    self.topologicalSortUtil(i,visited,stack) 
      
            # Push current vertex to stack which stores result 
            stack.insert(0,v) 
      
        # The function to do Topological Sort. It uses recursive  
        # topologicalSortUtil() 
        def topologicalSort(self): 
            # Mark all the vertices as not visited 
            visited = [False]*self.V 
            stack =[] 
      
            # Call the recursive helper function to store Topological 
            # Sort starting from all vertices one by one 
            for i in range(self.V): 
                if visited[i] == False: 
                    self.topologicalSortUtil(i,visited,stack) 
    
            # Print contents of stack 
            # print(stack)
            return stack
        
        def isCyclicUtil(self, v, visited, recStack): 
      
            # Mark current node as visited and  
            # adds to recursion stack 
            visited[v] = True
            recStack[v] = True
      
            # Recur for all neighbours 
            # if any neighbour is visited and in  
            # recStack then graph is cyclic 
            for neighbour in self.graph[v]: 
                if visited[neighbour] == False: 
                    if self.isCyclicUtil(neighbour, visited, recStack) == True: 
                        return True
                elif recStack[neighbour] == True: 
                    return True
      
            # The node needs to be poped from  
            # recursion stack before function ends 
            recStack[v] = False
            return False
        
        def isCyclic(self): 
            visited = [False] * self.V 
            recStack = [False] * self.V 
            for node in range(self.V): 
                if visited[node] == False: 
                    if self.isCyclicUtil(node,visited,recStack) == True: 
                        return True
            return False
    
    if len(modules) == 0:
        return []
            
    gh = Graph(len(modules))
    
    diction = {}
    for i in range(len(modules)):
        diction[modules[i]] = i # key is module name, value is index
    
    
    for pair in dependencyPairs:
        if pair["dependee"] in diction and pair["dependentOn"] in diction:
            dependee = diction[pair["dependee"]]
            master = diction[pair["dependentOn"]]
            gh.addEdge(master, dependee)

    if len(modules) == 1:
        for pair in dependencyPairs:
            if pair["dependee"] == modules[0]:
                return []
        return modules
    

    if gh.isCyclic():
        vertices = []
        [ vertices.append(node) for node in gh.graph ]
        
        leftovers = []
        for i in range(len(modules)):
            if i in vertices:
                pass
            else:
                leftovers.append(i)
    #    print(leftovers) 
        
        output = []
        for node in leftovers:
            output.append(modules[node])
#        print(output)
        
    
    else:
        sort_gh = gh.topologicalSort()
        
        output = []
        for node in sort_gh:
            output.append(modules[node])
#        print(output)
    return output
    
@app.route('/generateSequence', methods=['POST'])
def eval_dm():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	mods = data.get("modules");
	dps = data.get("dependencyPairs")

	out = dependencyManager(mods, dps)

	logging.info("My result :{}".format(out))
	return json.dumps(out);



