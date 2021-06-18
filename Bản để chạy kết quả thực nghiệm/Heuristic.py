import Data_generator
import find_path
import numpy as np
import time

m = 10
n = 10


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
    return min(arr, key=lambda z: (abs(z[0] - x) + abs(z[1] - y), board[z[0], z[1]]))


def solution():
    ls = []
    while X:
        sol = X[0]
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
        X.pop(0)
    print(ls)
    print('Cost', len(ls))


board, x_start, y_start = Data_generator.create_data(m, n)
print(board)
print('start point:', x_start, y_start)
start = time.time()
matrix, path = find_path.floyd_warshall(board)
X = []
x, y = x_start, y_start

while not check():
    point = find_candy(x, y)
    if board[point[0], point[1]] == 1:
        route, cost = find_path.find_the_shortest_way_to_crush_heart(board, matrix, path, [x, y], point)
        X.append(([(x, y), tuple(point)], route, 'SuckDust'))
        board[point[0], point[1]] -= 1
        x, y = point[0], point[1]
    else:
        route1, cost1 = find_path.find_the_shortest_way_to_crush_heart(board, matrix, path, [x, y], point)
        X.append(([(x, y), tuple(point)], route1, 'PickUp'))
        board[point[0], point[1]] -= 2
        route2, cost2 = find_path.find_the_shortest_way_to_crush_heart(board, matrix, path, point, [0, 0])
        X.append(([tuple(point), (0, 0)], route2, 'PutDown'))
        x, y = 0, 0
solution()
print(time.time() - start)
