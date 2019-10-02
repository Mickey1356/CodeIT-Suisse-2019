import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
@app.route('/encryption', methods=['POST'])
def eval_encrypt():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);

def solve(datum):
    f = []
    for data in datum:
        n = data.get("n")
        text = data.get("text")
        clean_text = ''.join([c.upper() for c in text if c.isalnum()])
        out = ['' for c in clean_text]
        if n >= len(clean_text):
            f.append(clean_text)
            continue
        index = 0
        done = False
        for i in range(len(clean_text)):
            for j in range(i, len(clean_text), n):
                out[j] = clean_text[index]
                index += 1
                if all(c.isalnum() for c in out):
                    done = True
                    break
            if done:
                break
        f.append(''.join(out))
    return f
