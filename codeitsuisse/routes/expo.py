import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/exponent', methods=['POST'])
def eval_expo():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	n = data.get("n")
	p = data.get("p")

	if p==0:
		res = {"result":[1, 1, 1]}
		logging.info("My result :{}".format(res))
		return jsonify(res)
	if n==0:
		res = {"result":[0, 1, 0]}
		logging.info("My result :{}".format(res))
		return jsonify(res)
	if n==1:
		res = {"result":[1, 1, 1]}
		logging.info("My result :{}".format(res))
		return jsonify(res)
	if p==1:
		fd = int(str(n)[0])
		ld = int(str(n)[-1])
		le = len(str(n))
		res = {"result":[fd,le,ld]}
		return jsonify(res)


	length = 1 + int(p * math.log10(n))
	po=[[0,0,0,0],[1,1,1,1],[6,2,4,8],[1,3,9,7],[6,4,6,4],[5,5,5,5],[6,6,6,6],[1,7,9,3],[6,8,4,2],[1,9,1,9]]
	la = n%10
	ld = po[la][p%4]
	lgA = p * math.log10(n)
	frac = math.modf(lgA)[0]
	fd = int(10**frac)
	result = {"result":[fd, length, ld]}



	logging.info("My result :{}".format(result))
	return jsonify(result)