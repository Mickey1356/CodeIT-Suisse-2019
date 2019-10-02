import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

class Subset: 
    def __init__(self, parent, rank): 
        self.parent = parent 
        self.rank = rank 
  
# A utility function to find set of an element 
# node(uses path compression technique) 
def find(subsets, node): 
    if subsets[node].parent != node: 
        subsets[node].parent = find(subsets, subsets[node].parent) 
    return subsets[node].parent 
  
# A function that does union of two sets  
# of u and v(uses union by rank) 
def union(subsets, u, v): 
      
    # Attach smaller rank tree under root  
    # of high rank tree(Union by Rank) 
    if subsets[u].rank > subsets[v].rank: 
        subsets[v].parent = u 
    elif subsets[v].rank > subsets[u].rank: 
        subsets[u].parent = v 
          
    # If ranks are same, then make one as  
    # root and increment its rank by one 
    else: 
        subsets[v].parent = u 
        subsets[u].rank += 1

def solve(data):
	output = []
	for tc_cnt, tc in enumerate(data):
		f = {"test_case":tc_cnt+1,"allocation":[], "satisfiable":True}
		case = tc.get("test_case")
		guests = tc.get("guests")
		tables = tc.get("tables")
		friends = tc.get("friends")
		enemies = tc.get("enemies")
		fams = tc.get("families")

		subsets = []
		for guest in range(1,guests+1):
			subsets.append(Subset(guest, 0))

		for (f1,f2) in friends:
			f1_rep = find(subsets, f1)
			f2_rep = find(subsets, f2)
			if f1_rep != f2_rep:
				union(subsets, f1_rep, f2_rep)

		for (f1,f2) in fams:
			f1_rep = find(subsets, f1)
			f2_rep = find(subsets, f2)
			if f1_rep != f2_rep:
				union(subsets, f1_rep, f2_rep)

		for (e1, e2) in enemies:
			e1_r = find(subsets, e1)
			e2_r = find(subsets, e2)
			if e1_r == e2_r:
				f["satisfiable"] = False
				output.append(f)
				continue

		# determine how many groups are there left
		grps = set()
		for p in range(1,guests+1):
			grps.add(find(subsets, p))

		for p1 in range(1, guests+1):
			for p2 in range(1, guests+1):
				if p1!=p2:
					p1_rep = find(subsets, p1)
					p2_rep = find(subsets, p2)



@app.route('/wedding-nightmare', methods=['POST'])
def eval_wedding():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
			#


	# result = chess(data)
	logging.info("My result :{}".format(f))
	return jsonify(f)



