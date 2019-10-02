import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def solve(data):
	num = data.get("number_of_elements")
	nop = data.get("number_of_operations")
	elements = data.get("elements")

	

@app.route('/yin-yang', methods=['POST'])
def eval_yy():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);