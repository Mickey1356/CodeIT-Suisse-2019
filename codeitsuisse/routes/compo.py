import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

from itertools import product

logger = logging.getLogger(__name__)

def solve(data):
	setid = data.get("setId")
	compoL = data.get("compositionLength")
	compo = data.get("composition")
	numC = data.get("noOfCase")
	patterns = data.get("patterns")
	np = []
	for p in patterns:
		if p!=p[::-1]:
			np.append(p[::-1])
		np.append(p)
	for i in range(1,compoL):
		prod = product(range(compoL), repeat=i)
		for p in prod:
			nstr = ''.join([c for k,c in enumerate(compo) if k not in p])
			if all(nstr.find(pat)==-1 for pat in np):
				f = {"testId":setid, "result":i}
				return f
	

@app.route('/composition', methods=['POST'])
def eval_compo():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);