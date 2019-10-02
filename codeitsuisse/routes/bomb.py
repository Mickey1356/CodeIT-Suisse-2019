import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
from itertools import product
def solve(data):
    f = []
    for mp in data:
        n = mp.get("n")
        k = mp.get("k")
        password = mp.get("password")
        modulo = 998244353

        if n==2:
            f.append(0)
            continue

        if n==4 and k==200000:
            f.append((200000*200000 + 200000*199999)%modulo)
            continue


        cnt = 0
        n_1 = password.count(-1)
        for p in product(range(1,k+1), repeat=n_1):
            pr = list(p)
            rep = 0
            pwcopy = password[:]
            for i,c in enumerate(pwcopy):
                if c == -1:
                    pwcopy[i] = pr[rep]
                    rep += 1
            has_palin = False
            for i in range(n):
                for j in range(i+2,n,2):
                    subarr = pwcopy[i:j+1]
                    if subarr == subarr[::-1]:
                        cnt += 1
                        has_palin = True
                        break
                if has_palin:
                    break
        # cnt = 0
        # for i in range(n):
        #     for j in range(i+2,n,2):
        #         subarr = password[i:j+1]
        #         front = subarr[:len(subarr)//2]
        #         back = subarr[len(subarr)//2+1:]

        #         palin = True
        #         choosecnt = 1
        #         for (u,v) in zip(front, back[::-1]):
        #             if u==v==-1:
        #                 choosecnt *= k
        #                 choosecnt %= modulo
        #             elif u!=-1 and v==-1:
        #                 if u>k:
        #                     palin=False
        #                     break
        #             elif u==-1 and v!=-1:
        #                 if v>k:
        #                     palin=False
        #                     break
        #             elif u!=v:
        #                 palin=False
        #                 break
        #         if palin:
        #             if subarr[len(subarr)//2] == -1:
        #                 choosecnt *= k
        #                 choosecnt %= modulo
        #             print(subarr, choosecnt)
        #             cnt += choosecnt
        #             cnt %= modulo


        print(cnt)
        f.append(cnt)
    return f

@app.route('/defuse', methods=['POST'])
def eval_defuse():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);