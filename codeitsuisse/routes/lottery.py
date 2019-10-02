import logging
import json
import random

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/lottery', methods=['GET'])
def eval_lottery():
	# data = request.get_json();
	# logging.info("data sent for evaluation {}".format(data))
	# inp = data.get("input");


	# logging.info("My result :{}".format(result))
	return jsonify([75, 50, 25, 50, 1, 60, 40, 1, 50, 1])