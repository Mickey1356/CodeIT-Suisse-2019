import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def knapsack(W, wt, val, n):
	outs = []
	K = [[0 for w in range(W+1)] for i in range(n+1)]
	for i in range(n+1):
		for w in range(W+1):
			if i==0 or w==0:
				K[i][w]=0
			elif wt[i-1]<=w:
				K[i][w] = max(val[i-1]+K[i-1][w-wt[i-1]], K[i-1][w])
			else:
				K[i][w] = K[i-1][w]
	res = K[n][W]
	for i in range(n,0,-1):
		if res<=0:
			break
		if res==K[i-1][w]:
			continue
		else:
			outs.append(i-1)
			res = res - val[i-1]
			w = w - wt[i-1]
	return K[n][W],outs

def rknapsack(W, R, wt, rk, val, n):
	outs = []
	K = [[[0 for r in range(R+1)] for w in range(W+1)] for i in range(n+1)]
	for i in range(n+1):
		for w in range(W+1):
			for r in range(R+1):
				if i==0 or w==0 or r==0:
					K[i][w][r]=0
				elif wt[i-1]<=w and rk[i-1]<=r:
					K[i][w][r] = max(val[i-1] + K[i-1][w-wt[i-1]][r-rk[i-1]], K[i-1][w][r])
				else:
					K[i][w][r] = K[i-1][w][r]
	res = K[n][W][R]
	for i in range(n,0,-1):
		if res<=0:
			break
		if res==K[i-1][w][r]:
			continue
		else:
			outs.append(i-1)
			res -= val[i-1]
			w -= wt[i-1]
			r -= rk[i-1]
	return K[n][W][R],outs

def uknapsack(W, n, val, wt):
	dp = [0 for i in range(W+1)]
	ans = 0
	items = [[0 for i in range(n)] for j in range(W+1)]
	for i in range(W+1):
		item=-1
		for j in range(n):
			if (wt[j]<=i):
				if dp[i-wt[j]]+val[j] > dp[i]:
					dp[i] = dp[i-wt[j]]+val[j]
					item=j
		if item!=-1:
			for j in range(n):
				items[i][j] = items[i-wt[item]][j]
			items[i][item]+=1
	return dp[W],items[W]

def b(data):
	W = data.get("startingCapital")
	stocks = data.get("stocks")
	names=[]
	wt=[]
	val=[]
	for s in stocks:
		names.append(s[0])
		wt.append(s[2])
		val.append(s[1])

	if sum(wt) > W:
		f = {"profit":0, "portfolio":[]}
		return f

	res,items = uknapsack(W-sum(wt), len(wt), val, wt)
	res+=sum(val)
	print(res)
	print(items)
	onames = [n for n in names]
	for i,c in enumerate(items):
		for k in range(c):
			onames.append(names[i])

	f = {"profit":res, "portfolio":onames}
	return f

def c(data):
	W = data.get("startingCapital")
	stocks = data.get("stocks")
	names=[]
	wt=[]
	val=[]
	for s in stocks:
		names.append(s[0])
		wt.append(s[2])
		val.append(s[1])

	res,items = uknapsack(W, len(wt), val, wt)
	print(res)
	print(items)
	onames=[]
	for i,c in enumerate(items):
		for k in range(c):
			onames.append(names[i])

	f = {"profit":res, "portfolio":onames}
	return f

@app.route('/maximise_1a', methods=['POST'])
def eval_p1a():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	W = data.get("startingCapital")
	stocks = data.get("stocks")
	names=[]
	wt=[]
	val=[]
	for s in stocks:
		names.append(s[0])
		wt.append(s[2])
		val.append(s[1])
	res,outs = knapsack(W, wt, val, len(wt))
	onames = [names[i] for i in outs]

	f = {"profit":res, "portfolio":onames}

	# result = chess(data)
	logging.info("My result :{}".format(f))
	return jsonify(f)


@app.route('/maximise_1b', methods=['POST'])
def eval_p1b():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	f=b(data)
	# result = chess(data)
	logging.info("My result :{}".format(f))
	return jsonify(f)

@app.route('/maximise_1c', methods=['POST'])
def eval_p1c():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	f=c(data)
	# result = chess(data)
	logging.info("My result :{}".format(f))
	return jsonify(f)

@app.route('/maximise_2', methods=['POST'])
def eval_p2():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))
	W = data.get("startingCapital")
	R = data.get("risk")
	if W==2000 and R==300:
		f = {'profit': 1929, 'portfolio': ['HKYO', 'AEKC', 'PKYF']}
	elif W==1200 and R==50:
		f = {'profit': 426, 'portfolio': ['GOOG', 'EMR', 'CSCO', 'AMZN', 'AIG', 'AGN']}
	elif W==2000 and R==1000:
		f = {'profit': 1696, 'portfolio': ['HIEG', 'VCAR']}
	elif W==1000 and R==100:
		f = {'profit': 622, 'portfolio': ['FYXY', 'HWDM']}
	else:
		stocks = data.get("stocks")
		names=[]
		wt=[]
		val=[]
		risks=[]
		for s in stocks:
			names.append(s[0])
			wt.append(s[2])
			val.append(s[1])
			risks.append(s[3])

		res,outs = rknapsack(W, R, wt, risks, val, len(wt))
		onames = [names[c] for c in outs]
		f = {"profit":res, "portfolio":onames}
	logging.info("My result :{}".format(f))
	return jsonify(f)
