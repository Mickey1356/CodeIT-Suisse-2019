import logging
import json
import os

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

import pickle
from sklearn.linear_model import LogisticRegression
import re
from sklearn.feature_extraction.text import CountVectorizer

# and later you can load it
with open(os.getcwd() + '/codeitsuisse/routes/analyser_pkl', 'rb') as f:
    mymodel = pickle.load(f)
with open(os.getcwd() + '/codeitsuisse/routes/countvec_pkl', 'rb') as g:
    my_cv = pickle.load(g)
    
def sent_anal(reviews):
    
    REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    def preprocess_reviews(reviews):
        reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
        reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
        return reviews
    
    # processing the reviews
    review_clean = preprocess_reviews(reviews)
    review_processed = my_cv.transform(review_clean)
    
    
    responses = []
    for string in review_processed:
        if mymodel.predict(string)[0] == 1:
            responses.append("positive")
        elif mymodel.predict(string)[0] == 0:
            responses.append("negative")

    
    return responses

def solve(data):
	reviews = data.get("reviews")

	resp = sent_anal(reviews)

	result = {"response": resp }
	return result
	
@app.route('/sentiment-analysis', methods=['POST'])
def eval_sentanal():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)


	# sid = SentimentIntensityAnalyzer()
	# for review in reviews:
	# 	ss = sid.polarity_scores(review)
	# 	compound = ss["compound"]
	# 	if compound > 0:
	# 		result["response"].append("positive")
	# 	else:
	# 		result["response"].append("negative")


	logging.info("My result :{}".format(result))
	return jsonify(result);