import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

import numpy as np
from scipy import optimize
from scipy.signal import argrelextrema

def tech_anal(inputs):

    def sine_one(t, base, trend, scale, w):
        return base + (trend*t) + (scale * np.sin(2* 3.14159 * w * t))
    
    output = []
    for scenario in inputs:

        train_data = scenario
        t_data = [ i for i in range(100) ]
        
        #let optimizer converge
        start_base = train_data[0] # close to the first data point
        start_trend = ( train_data[99] - train_data[0] ) / 100 # rise over run
        start_scale = 5 # no idea
        start_w = 0.05
        
        params, params_covariance = optimize.curve_fit(sine_one, t_data, train_data, p0 = [start_base, start_trend, start_scale, start_w])
        
        t_predicted = [ i for i in range(100, 1100) ] # starts at index 100 to 1099
        y_predicted = [ sine_one(t, params[0], params[1], params[2], params[3]) for t in t_predicted ]
        
        y_prednp = np.asarray(y_predicted) # convert y_predicted into np array to locate maxina and minima
        
        # for local maxima
        local_max_np = argrelextrema(y_prednp, np.greater)
        max_list = np.array([ i+100 for i in local_max_np ]).tolist()[0]
        
        # for local minima
        local_min_np = argrelextrema(y_prednp, np.less)
        min_list = np.array([ i+100 for i in local_min_np ]).tolist()[0]
        
        # Should my first action, which is to buy, be at 100?
        ## Note that the argrelextrema function ignores time 100.
        ## I should buy at 100 if first time-point is maxima
        ## I should not buy at 100 if first time-point is minima
        ## Therefore, if first occurance of maxima is before first occurance of minima,
        ## prepend a 100 to scen_output.
        scen_output = max_list + min_list
        scen_output.sort()
        scen_output = [100] + scen_output
        print(len(scen_output))
        
        output.append(scen_output)
        
    return output

@app.route('/technical-analysis', methods=['POST'])
def eval_ta():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = tech_anal(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);