from functools import reduce
import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
@app.route('/bankbranch', methods=['POST'])
def eval_bank():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = solve(data)

    logging.info("My result :{}".format(result))
    return jsonify(result);

def solve(data):
    n = data.get("N")
    tim = data.get("branch_officers_timings")
    ans = bankbranch(n, tim)
    return {"answer":ans}

from functools import reduce
def bankbranch(N, timings):
    
    def available_officer(time_list):
        # returns the branch ID (i.e. the 1-index of the input time_list) of the available officer
        return time_list.index(min(time_list))+1
    
    def lcm(denominators):
        return reduce(lambda x,y: (lambda a,b: next(i for i in range(max(a,b),a*b+1) if i%a==0 and i%b==0))(x,y), denominators)
    
    # no. of branch officers
    B = len(timings) 
    if B == 1:
        return 1 # only 1 Branch officer is serving
    
    
    ##### IF PEACEFUL MORNING ###############
    if B <= 100 and max(timings) <= 20 and N <= 1000:
        # BRUTE FORCE part
        time_free = [ 0 for x in range(B) ]
        if N == 0:
            return B # the last branch officer serves you
        else:
            for i in range(N-1): # loop until the customer right BEFORE you
                officer_ID = available_officer(time_free)
                # increment that ID by his serving time in time_free
                time_free[officer_ID-1] += timings[officer_ID-1]   
                
        return available_officer(time_free)
    #########################################
    
    ##### IF CRAZY LUNCHTIME CROWD ##########
    # compute LCM of all timings
    lcm = lcm(timings)
    # compute number of customers, cycle_cust before it cycles once
    cycle_cust =  sum([int(lcm/time) for time in timings])
    N = N % cycle_cust 
    

    # BRUTE FORCE part
    time_free = [ 0 for x in range(B) ]
    if N == 0:
        return B # the last branch officer serves you
    else:
        for i in range(N-1): # loop until the customer right BEFORE you
            officer_ID = available_officer(time_free)
            # increment that ID by his serving time in time_free
            time_free[officer_ID-1] += timings[officer_ID-1]
        
    return available_officer(time_free)
    #########################################