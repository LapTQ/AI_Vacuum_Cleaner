import Data_generator
import find_path
import copy
import numpy as np
import time

def check():
    if 1 not in board and not 2 in board and not 3 in board:
        return True
    return False


def find_candy(x, y):
    arr = []
    for i in range(m):
        for j in range(n):
            if board[i, j] == 1 or board[i, j] == 2 or board[i, j] == 3:
                arr.append([i, j])
    if arr:
        arr.sort(key=lambda z: abs(z[0] - x) + abs(z[1] - y))
        return arr
    else:
        return arr


def solution():
    global f_best
    ls = []
    X_ = copy.deepcopy(X)
    while X_:
        sol = X_[0]
        action = sol[2]
        start = sol[0][0]
        end = sol[0][1]
        p = sol[1]
        while p:
            if p[0][0] - start[0] == 1:
                ls.append('MoveDown')
            elif p[0][0] - start[0] == -1:
                ls.append('MoveUp')
            elif p[0][1] - start[1] == 1:
                ls.append('MoveRight')
            elif p[0][1] - start[1] == -1:
                ls.append('MoveLeft')
            start = p[0]
            p.pop(0)
        if start == end:
            ls.append(action)
        else:
            if end[0] - start[0] == 1:
                ls.append('MoveDown')
            elif end[0] - start[0] == -1:
                ls.append('MoveUp')
            elif end[1] - start[1] == 1:
                ls.append('MoveRight')
            elif end[1] - start[1] == -1:
                ls.append('MoveLeft')
            ls.append(action)
        X_.pop(0)
    #print(len(ls))

    if len(ls) < f_best:
        f_best = len(ls)
        X_best[:] = ls[:]
        print('Update X: ',X_best)


def Try(x, y):
    global board, f_best, X,f
    candy = find_candy(x, y)
    for point in candy:
        temp = board.copy()
        tem_X = X.copy()
        g=f
        if board[point[0], point[1]] == 1:
            route,cost=find_path.find_the_shortest_way_to_crush_heart(board,matrix, path, [x, y], point)
            f+=(cost+1)
            X.append(([(x, y), tuple(point)],route, 'SuckDust'))
            board[point[0], point[1]] -= 1
        else:
            route1,cost1=find_path.find_the_shortest_way_to_crush_heart(board,matrix, path, [x, y], point)
            X.append(([(x, y), tuple(point)],route1, 'PickUp'))
            board[point[0], point[1]] -= 2
            route2,cost2=find_path.find_the_shortest_way_to_crush_heart(board,matrix, path, point, [0, 0])
            X.append(([tuple(point), (0, 0)],route2, 'PutDown'))
            f+=(cost1+cost2+2)
            point = [0, 0]
        if check():
            solution()

        else:
            estimate = f
            for row in range(m):
                for col in range(n):
                    if board[row, col] == 3:
                        estimate += (2 * (row + col))
                    elif board[row, col] == 2:
                        estimate += (row + col)
            if estimate < f_best:
                Try(point[0], point[1])
        X = tem_X
        board = temp
        f=g

np.random.seed(10)
m = 10
n = 10
board, x_start, y_start = Data_generator.create_data(m, n)
matrix, path = find_path.floyd_warshall(board)

X = []
f=0
f_best = 1e9
X_best = []
print(board)
print('start point:', x_start, y_start)
start=time.time()
Try(x_start, y_start)

print('The Minimum number of steps to take:', f_best)
print(time.time()-start,'s')
