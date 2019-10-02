import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def chess(inp):
	pos = ()
	#find the queen
	size = len(inp)
	for y in range(size):
		for x in range(size):
			if inp[y][x] == "K":
				pos=(x,y)
	cnt = 0
	x = pos[0]
	y = pos[1]
	print(pos)
	for nx in range(x+1, size):
		if inp[y][nx]=="X":
			break
		else:
			inp[y][nx]='1'
			cnt+=1
	for nx in range(x-1,-1,-1):
		if inp[y][nx]=="X":
			break
		else:
			inp[y][nx]='2'
			cnt+=1
	for ny in range(y+1,size):
		if inp[ny][x]=="X":
			break
		else:
			inp[ny][x]='3'
			cnt+=1
	for ny in range(y-1,-1,-1):
		if inp[ny][x]=="X":
			break
		else:
			inp[ny][x]='4'
			cnt+=1
	for c in range(1,size):
		if y+c<size and x+c<size:
			if inp[y+c][x+c]=="X":
				break
			else:
				inp[y+c][x+c]='5'
				cnt+=1
	for c in range(1,size):
		if y+c<size and x-c>=0:
			if inp[y+c][x-c]=="X":
				break
			else:
				inp[y+c][x-c]='6'
				cnt+=1
	for c in range(1,size):
		if y-c>=0 and x+c<size:
			if inp[y-c][x+c]=="X":
				break
			else:
				inp[y-c][x+c]='7'
				cnt+=1
	for c in range(1,size):
		if y-c>=0 and x-c>=0:
			if inp[y-c][x-c]=="X":
				break
			else:
				inp[y-c][x-c]='8'
				cnt+=1
	print(inp)
	print(cnt)
	return cnt


@app.route('/chessgame', methods=['POST'])
def eval_chess():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	# inp = data.get("input");
	result = chess(data)
	logging.info("My result :{}".format(chess(data)))
	return json.dumps(result);



