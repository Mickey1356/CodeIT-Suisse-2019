import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
from collections import deque
def ff(x,y,ngrid,sizex,sizey,le,outs):

	mystack = deque()
	mystack.append((x,y,1))

	while mystack:
		(x,y,c) = mystack.pop()
		ngrid[y][x]="V"
		cnt = 0

		if y-1>=0 and ngrid[y-1][x]!="X":
			cnt+=1
			if y-1>=0 and ngrid[y-1][x]!="V":
				mystack.append((x,y-1,c+1))
		if y+1<sizey and ngrid[y+1][x]!="X":
			cnt+=1
			if y+1<sizey and ngrid[y+1][x]!="V":
				mystack.append((x,y+1,c+1))

		if x-1>=0 and ngrid[y][x-1]!="X":
			cnt+=1
			if x-1>=0 and ngrid[y][x-1]!="V":
				mystack.append((x-1,y,c+1))

		if x+1<sizex and ngrid[y][x+1]!="X":
			cnt+=1
			if x+1<sizex and ngrid[y][x+1]!="V":
				mystack.append((x+1,y,c+1))

		if cnt==1:
			outs.append(((x,y),c))
	return outs

def knapsack(W, wt, val, n):
	paths=[]
	K = [[0 for x in range(W+1)] for x in range(n+1)]
	for i in range(n+1):
		for w in range(W+1):
			if i==0 or w==0:
				K[i][w]=0
			elif wt[i-1]<=w:
				K[i][w] = max(val[i-1]+K[i-1][w-wt[i-1]], K[i-1][w])
			else:
				K[i][w] = K[i-1][w]
	res = K[n][W]
	for i in range(n,0,-1):
		if res<=0:
			break
		if res==K[i-1][w]:
			continue
		else:
			paths.append(i-1)
			res = res - val[i-1]
			w = w - wt[i-1]
	return K[n][W], paths

def rp1(grid, fuel):
	#cvt grid to array
	ngrid = [[c for c in r] for r in grid]
	outs = ff(0,0,ngrid,len(ngrid[0]),len(ngrid),1,[])
	W = fuel
	nouts = [a for a in outs if not(a[0][0]==0 and a[0][1]==0)]
	wt = [a[1] for a in nouts if not(a[0][0]==0 and a[0][1]==0)]
	val = wt
	n = len(wt)
	res,paths = knapsack(W, wt, val, n)
	print(res)
	fin = {"hits":[]}
	for c in paths:
		x=nouts[c][0][0]+1
		y=nouts[c][0][1]+1
		guns=nouts[c][1]
		fin["hits"].append({"cell":{"x":x, "y":y}, "guns":guns})
	return fin


@app.route('/gun-control', methods=['POST'])
def eval_guncontrol():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	grid = data.get("grid")
	fuel = data.get("fuel")
	f = rp1(grid,fuel)
	# result = chess(data)
	logging.info("My result :{}".format(f))
	return jsonify(f)



