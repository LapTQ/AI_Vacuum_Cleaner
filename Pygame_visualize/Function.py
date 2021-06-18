import numpy as np
import copy
from constant import *


def create_data(m, n):
    matrix = np.zeros((m, n), dtype='int')
    for i in range(3):
        x, y = np.random.randint(1, m - 1), np.random.randint(1, n - 1)
        matrix[x, y] = 4
    for x in range(m):
        for y in range(n):
            if matrix[x, y] != 4:
                matrix[x, y] = np.random.randint(0, 4)
    matrix[0, 0] = 0
    x_start, y_start = 0, 0
    a = True
    while a:
        x_start, y_start = np.random.randint(0, m), np.random.randint(0, n)
        if matrix[x_start, y_start] != 4:
            a = False

    return matrix, x_start, y_start


def floyd_warshall(board):
    m = len(board)
    n = len(board[1])
    N = m * n
    matrix = np.full((N, N), 1e9, dtype='int32')
    for i in range(N):
        for j in range(N):
            if i != j:
                x0, y0 = i // n, i % n
                x, y = j // n, j % n
                if board[x, y] != 4 and abs(x - x0) + abs(y - y0) == 1:
                    matrix[i, j] = 1
            else:
                matrix[i, j] = 0
    path = np.full((N, N), -1)
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if matrix[i, k] + matrix[k, j] < matrix[i, j]:
                    matrix[i, j] = matrix[i, k] + matrix[k, j]
                    path[i][j] = k
    return matrix, path


def find_the_shortest_way_to_crush_heart(board, path, start, end):
    m = len(board)
    n = len(board[1])
    i = start[0] * n + start[1]
    j = end[0] * n + end[1]
    lis = []
    if i >= j:
        while path[i, j] != -1:
            lis.append(path[i, j])
            i = path[i, j]
        arr = [[index // n, index % n] for index in lis]
    else:
        while path[i, j] != -1:
            lis.append(path[i, j])
            j = path[i, j]
        lis = lis[::-1]
        arr = [[index // n, index % n] for index in lis]
    return arr


def check(board):
    if 1 not in board and not 2 in board and not 3 in board:
        return True
    return False


def find_candy(board, x, y):
    arr = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i, j] == 1 or board[i, j] == 2 or board[i, j] == 3:
                arr.append([i, j])
    return min(arr, key=lambda z: (abs(z[0] - x) + abs(z[1] - y),board[z[0],z[1]]))


def simplify_route(X):
    X1=X[0]
    arr1 = [X1[0][0]]+[title for title in X1[1]] + [X1[0][1]] + [X1[2]]
    arr2 = []
    if len(X)==2:
        X2=X[1]
        arr2= [X2[0][0]]+[title for title in X2[1]] + [X2[0][1]] + [X2[2]]
    lis=[]
    for ele in arr1 + arr2:
        if len(ele)!=0:
            lis.append(ele)
    return lis




def f(board, path, x, y, X):
    if not check(board):
        point = find_candy(board, x, y)
        if board[point[0], point[1]] == 1:
            route = find_the_shortest_way_to_crush_heart(board, path, [x, y], point)
            X.append(([[x, y], point], route, 'SuckDust'))
            board[point[0], point[1]] -= 1
            x_new, y_new = point[0], point[1]
        else:
            route1 = find_the_shortest_way_to_crush_heart(board, path, [x, y], point)
            X.append(([[x, y], point], route1, 'PickUp'))
            board[point[0], point[1]] -= 2
            route2 = find_the_shortest_way_to_crush_heart(board, path, point, [0, 0])
            X.append(([point, [0, 0]], route2, 'PutDown'))
            x_new, y_new = 0, 0
        return x_new, y_new, X
