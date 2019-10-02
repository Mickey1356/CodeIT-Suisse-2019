import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def readyplayeronev2(N, T):
    
    def ready(cur_player, Narray, T):     
    
        if cur_player == 1:
            if (max(Narray) >= T): # base case
                return (1, 1000) # massive cost on player 2
            else:
                permutations = []
                for i in Narray:
                    Narray_copy = Narray.copy()
                    Narray_copy.remove(i)
                    permutations.append(( ready(2,Narray_copy,T-i)[0]+1, ready(2, Narray_copy, T-i)[1]+1))
                return min(permutations, key = lambda t: t[0])
        
        
        elif cur_player == 2:
            if (max(Narray) >= T): # base case
                return (1000, 1) # massive cost on player 1
            else:
                permutations = []
                for i in Narray:
                    Narray_copy = Narray.copy()
                    Narray_copy.remove(i)
                    permutations.append(( ready(1, Narray_copy, T-i)[0]+1, ready(1, Narray_copy, T-i)[1]+1))
                return min(permutations, key = lambda t: t[1])

    # first check that values of N and T are valid. If invalid, then return -1.
    if sum([i for i in range(1, N+1)]) < T:
        return -1

    pair = ready(1, [x for x in range(1, N+1)], T)
    if pair[1] >= 1000:
        return pair[0]
    else: # pair[0] >= 1000:
        return -1


@app.route('/readyplayerone', methods=['POST'])
def eval_rp1():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	N = int(data.get("maxChoosableInteger"))
	T = int(data.get("desiredTotal"))
	f = {"res":readyplayeronev2(N,T)}

	# result = chess(data)
	logging.info("My result :{}".format(f))
	return json.dumps(f);



