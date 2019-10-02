import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

class IDAStar:
    def __init__(self, h, neighbours):
        """ Iterative-deepening A* search.

        h(n) is the heuristic that gives the cost between node n and the goal node. It must be admissable, meaning that h(n) MUST NEVER OVERSTIMATE the true cost. Underestimating is fine.

        neighbours(n) is an iterable giving a pair (cost, node, descr) for each node neighbouring n
        IN ASCENDING ORDER OF COST. descr is not used in the computation but can be used to
        efficiently store information about the path edges (e.g. up/left/right/down for grids).
        """

        self.h = h
        self.neighbours = neighbours
        self.FOUND = object()


    def solve(self, root, is_goal, max_cost=None):
        """ Returns the shortest path between the root and a given goal, as well as the total cost.
        If the cost exceeds a given max_cost, the function returns None. If you do not give a
        maximum cost the solver will never return for unsolvable instances."""

        self.is_goal = is_goal
        self.path = [root]
        self.is_in_path = {root}
        self.path_descrs = []
        self.nodes_evaluated = 0

        bound = self.h(root)

        while True:
            t = self._search(0, bound)
            if t is self.FOUND: return self.path, self.path_descrs, bound, self.nodes_evaluated
            if t is None: return None
            bound = t

    def _search(self, g, bound):
        self.nodes_evaluated += 1

        node = self.path[-1]
        f = g + self.h(node)
        if f > bound: return f
        if self.is_goal(node): return self.FOUND

        m = None # Lower bound on cost.
        for cost, n, descr in self.neighbours(node):
            if n in self.is_in_path: continue

            self.path.append(n)
            self.is_in_path.add(n)
            self.path_descrs.append(descr)
            t = self._search(g + cost, bound)

            if t == self.FOUND: return self.FOUND
            if m is None or (t is not None and t < m): m = t

            self.path.pop()
            self.path_descrs.pop()
            self.is_in_path.remove(n)

        return m


def slide_solved_state(n):
    return tuple(i % (n*n) for i in range(1, n*n+1))

def slide_randomize(p, neighbours):
    for _ in range(len(p) ** 2):
        _, p, _ = random.choice(list(neighbours(p)))
    return p

def slide_neighbours(n):
    movelist = []
    for gap in range(n*n):
        x, y = gap % n, gap // n
        moves = []
        if x > 0: moves.append(-1)    # Move the gap left.
        if x < n-1: moves.append(+1)  # Move the gap right.
        if y > 0: moves.append(-n)    # Move the gap up.
        if y < n-1: moves.append(+n)  # Move the gap down.
        movelist.append(moves)

    def neighbours(p):
        gap = p.index(0)
        l = list(p)

        for m in movelist[gap]:
            l[gap] = l[gap + m]
            l[gap + m] = 0
            yield (1, tuple(l), (l[gap], m))
            l[gap + m] = l[gap]
            l[gap] = 0

    return neighbours

def slide_print(p):
    n = int(round(len(p) ** 0.5))
    l = len(str(n*n))
    for i in range(0, len(p), n):
        print(" ".join("{:>{}}".format(x, l) for x in p[i:i+n]))

def encode_cfg(cfg, n):
    r = 0
    b = n.bit_length()
    for i in range(len(cfg)):
        r |= cfg[i] << (b*i)
    return r


def gen_wd_table(n):
    goal = [[0] * i + [n] + [0] * (n - 1 - i) for i in range(n)]
    goal[-1][-1] = n - 1
    goal = tuple(sum(goal, []))

    table = {}
    to_visit = [(goal, 0, n-1)]
    while to_visit:
        cfg, cost, e = to_visit.pop(0)
        enccfg = encode_cfg(cfg, n)
        if enccfg in table: continue
        table[enccfg] = cost

        for d in [-1, 1]:
            if 0 <= e + d < n:
                for c in range(n):
                    if cfg[n*(e+d) + c] > 0:
                        ncfg = list(cfg)
                        ncfg[n*(e+d) + c] -= 1
                        ncfg[n*e + c] += 1
                        to_visit.append((tuple(ncfg), cost + 1, e+d))

    return table

def slide_wd(n, goal):
    wd = gen_wd_table(n)
    goals = {i : goal.index(i) for i in goal}
    b = n.bit_length()

    def h(p):
        ht = 0 # Walking distance between rows.
        vt = 0 # Walking distance between columns.
        d = 0
        for i, c in enumerate(p):
            if c == 0: continue
            g = goals[c]
            xi, yi = i % n, i // n
            xg, yg = g % n, g // n
            ht += 1 << (b*(n*yi+yg))
            vt += 1 << (b*(n*xi+xg))

            if yg == yi:
                for k in range(i + 1, i - i%n + n): # Until end of row.
                    if p[k] and goals[p[k]] // n == yi and goals[p[k]] < g:
                        d += 2

            if xg == xi:
                for k in range(i + n, n * n, n): # Until end of column.
                    if p[k] and goals[p[k]] % n == xi and goals[p[k]] < g:
                        d += 2

        d += wd[ht] + wd[vt]

        return d
    return h

def puzz_bfs(start, end):
    mout = []
    front = [[start]]
    expanded = []
    expanded_nodes = 0
    while front:
        i = 0
        for j in range(1, len(front)):
            if len(front[i]) > len(front[j]):
                i = j
        path = front[i]
        front = front[:i] + front[i+1:]
        endnode = path[-1]
        if endnode in expanded:
            continue
        for k in moves3(endnode):
            if k in expanded:
                continue
            front.append(path + [k])
        expanded.append(endnode)
        expanded_nodes += 1
        if endnode == end:
            break
    for i in range(len(path)-1):
        mout.append(getMove3(path[i], path[i+1]))
    return mout

def puzz_astar(start, end):
    front = [[heuristic_2(start), start]]
    expanded = []
    expanded_nodes = 0
    while front:
        i = 0
        for j in range(1, len(front)):
            if front[i][0] > front[j][0]:
                i = j
        path = front[i]
        front = front[:i] + front[i+1:]
        endnode = path[-1]
        if endnode == end:
            break
        if endnode in expanded: continue
        for k in moves3(endnode):
            if k in expanded: continue
            newpath = [path[0] + heuristic_2(k) - heuristic_2(endnode)] + path[1:] + [k] 
            front.append(newpath)
            expanded.append(endnode)
        expanded_nodes += 1

    # for p in path:
    #     print(p)
    mout = []
    for i in range(1,len(path)-1):
        if type(path[i]) is not int:
            mout.append(getMove3(path[i], path[i+1]))
    return mout

def getMove3(mat1, mat2):
    m1 = eval(mat1)
    m2 = eval(mat2)

    print(m1)

    i1 = 0
    while not any(0 in c for c in m1[i1]):
        i1+=1
    j1 = 0
    while 0 not in m1[i1][j1]:
        j1+=1
    k1 = m1[i1][j1].index(0)

    i2 = 0
    while not any(0 in c for c in m2[i2]):
        i2+=1
    j2 = 0
    while 0 not in m2[i2][j2]:
        j2+=1
    k2 = m2[i2][j2].index(0)

    # print(i1,j1,k1)
    # print(i2,j2,k2)

    if i1==i2 and j1==j2 and k1>k2:
        return "L"
    if i1==i2 and j1==j2 and k1<k2:
        return "R"
    if i1==i2 and j1>j2:
        return "B"
    if i1==i2 and j1<j2:
        return "F"
    if i1>i2:
        return "D"
    if i1<i2:
        return "U"

def moves3(mat_in):
    output = []
    m = eval(mat_in)
    i = 0
    while not any(0 in c for c in m[i]):
        i+=1
    j = 0
    while 0 not in m[i][j]:
        j+=1
    k = m[i][j].index(0)

    if i>0: # move U
        m[i][j][k],m[i-1][j][k] = m[i-1][j][k],m[i][j][k]
        output.append(str(m))
        m[i][j][k],m[i-1][j][k] = m[i-1][j][k],m[i][j][k]
    if i < len(m) - 1: # move D
        m[i][j][k],m[i+1][j][k] = m[i+1][j][k],m[i][j][k]
        output.append(str(m))
        m[i][j][k],m[i+1][j][k] = m[i+1][j][k],m[i][j][k]

    if j>0: # move F
        m[i][j][k],m[i][j-1][k] = m[i][j-1][k],m[i][j][k]
        output.append(str(m))
        m[i][j][k],m[i][j-1][k] = m[i][j-1][k],m[i][j][k]
    if j < len(m) - 1: # move B
        m[i][j][k],m[i][j+1][k] = m[i][j+1][k],m[i][j][k]
        output.append(str(m))
        m[i][j][k],m[i][j+1][k] = m[i][j+1][k],m[i][j][k]

    if k>0: # move L
        m[i][j][k],m[i][j][k-1] = m[i][j][k-1],m[i][j][k]
        output.append(str(m))
        m[i][j][k],m[i][j][k-1] = m[i][j][k-1],m[i][j][k]
    if k < len(m) - 1: # move R
        m[i][j][k],m[i][j][k+1] = m[i][j][k+1],m[i][j][k]
        output.append(str(m))
        m[i][j][k],m[i][j][k+1] = m[i][j][k+1],m[i][j][k]

    return output

def solve3(data):
    init = str(data.get("initial"))
    goal = str(data.get("goal"))

    return puzz_bfs(init, goal)

def solve(data):
    initial = data.get("initial")
    goal = data.get("goal")

    moves = []
    # check if problem 1
    if type(initial[0]) is int:
        start = initial.index(0)
        end = goal.index(0)
        if end > start:
            # move R
            moves = ["R"] * (end-start)
        elif end < start:
            # move L
            moves = ["L"] * (start-end)
        return {"moves":moves}

    elif type(initial[0]) is list:
        if type(initial[0][0]) is int:
            # problem 2
            solved_state = slide_solved_state(4)
            neighbours = slide_neighbours(4)
            is_goal = lambda p: p == solved_state
            slide_solver = IDAStar(slide_wd(4, solved_state), neighbours)

            grid = tuple(c for r in initial for c in r)
            path, moves, cost, num_eval = slide_solver.solve(grid, is_goal, 80)
            slide_print(grid)
            outpt = [{-1: "L", 1: "R", -4: "B", 4: "F"}[move[1]] for move in moves]
            return {"moves":outpt}
        else:
            init = str(initial)
            goa = str(goal)
            return {"moves":puzz_astar(init, goa)}

def heuristic_2(puzz):
    distance = 0
    m = eval(puzz)
    N = len(m)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if m[i][j][k] == 0:
                    continue
                # print(m[i][j][k], (m[i][j][k]//(N*N), (m[i][j][k]%(N*N))//N, (m[i][j][k]%(N*N))%N))
                distance += abs(i - (m[i][j][k]-1)//(N*N)) + abs(j - ((m[i][j][k]-1)%(N*N))//N) + abs(k - ((m[i][j][k]-1)%(N*N))%N)
    return distance
    
@app.route('/prismo', methods=['POST'])
def eval_prismo():
	data = request.get_json();
	logging.info("data sent for evaluation {}".format(data))

	result = solve(data)

	logging.info("My result :{}".format(result))
	return jsonify(result);