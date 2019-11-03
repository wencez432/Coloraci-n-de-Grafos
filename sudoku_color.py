from random import shuffle
from sys import stdin

def index(r, c):
    return 9 * r + c

def mk_sudoku_graph():
    def mk_complete_graph(vertices):
        graph = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                edge = (vertices[i], vertices[j])
                graph += [tuple(sorted(edge))]
        return graph

    graph = []
    for r in range(9):
        edges = []
        for c in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    for c in range(9):
        edges = []
        for r in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    for rb in range(0, 9, 3):
        for cb in range(0, 9, 3):
            edges = []
            for r in range(3):
                for c in range(3):
                    edges += [index(rb + r, cb + c)]
            graph += mk_complete_graph(edges)
    return list(set(graph))

def adj_list(graph):
    alist = {}
    def insert_edge(v1, v2):
        if v1 in alist:
            alist[v1] += [v2]
        else:
            alist[v1] = [v2]

    for (v1, v2) in graph:
        insert_edge(v1, v2)
        insert_edge(v2, v1)
    return alist

constraints = adj_list(mk_sudoku_graph())
colors = [0]*81
fixed = [False]*81
ncolored = 0
debug = False

def read_puzzle():
    global ncolored
    for r in range(9):
        l = stdin.readline()
        for c in range(9):
            if l[c] == '.':
                continue
            v = index(r, c)
            fixed[v] = True
            colors[v] = int(l[c])
            ncolored += 1

def print_solution(soln):
    for r in range(9):
        if r%3==0:
            print("-------------")
        for c in range(9):
            v = soln[index(r, c)]
            if c%3==0:
                print("|", end="")
            if v == 0:
                print(".", end="")
            else:
                print(v, end="")
        print("|")
    print("-------------")

def printS(soln):
    for r in range(9):
        for c in range(9):
            v = soln[index(r, c)]
            if v == 0:
                print(".", end="")
            else:
                print(v, end="")
        print("")

def color_puzzle(max_solns, shuffle_colors):
    global ncolored, colors, debug
    if debug:
        print("coloring %d" % (ncolored,))

    if max_solns != None and max_solns <= 0:
        return []

    if ncolored >= 81:
        return [colors*1]

    def neighbor_colors(v):
        ncs = set([])
        for v0 in constraints[v]:
            if colors[v0] > 0:
                ncs = ncs.union({colors[v0]})
        return ncs

    def most_constrained_free():
        ncs = -1
        target = -1
        for v in range(len(colors)):
            if colors[v] > 0:
                continue
            ncsv = len(neighbor_colors(v))
            if ncsv > ncs:
                target = v
                ncs = ncsv
        assert target != -1
        return target

    def first_free():
        for v in range(len(colors)):
            if colors[v] == 0:
                return v
        assert False

    if max_solns == 1:
        v = most_constrained_free()
    else:
        v = first_free()

    cs = set(range(1,10)).difference(neighbor_colors(v))

    if len(cs) == 0:
        return []

    if shuffle_colors:
        cs = list(cs)
        shuffle(cs)

    ncolored += 1
    solns = []
    for c in cs:
        if debug:
            print("coloring %d with %d (%d)" % (v, c, ncolored))
        colors[v] = c
        solns_cur = color_puzzle(max_solns, shuffle_colors)
        if debug:
            print("found %d solutions" % (len(solns_cur),))
        solns += solns_cur
        if max_solns != None:
            max_solns -= len(solns_cur)
            if max_solns <= 0:
                break
    colors[v] = 0
    ncolored -= 1
    return solns
