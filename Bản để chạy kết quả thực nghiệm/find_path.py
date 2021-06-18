import numpy as np

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
def find_the_shortest_way_to_crush_heart(board,matrix,path,start,end):
    m = len(board)
    n = len(board[1])
    i=start[0]*n+start[1]
    j=end[0]*n+end[1]
    lis=[]
    if i >= j:
        while path[i,j]!=-1:
            lis.append(path[i,j])
            i=path[i,j]
        arr=[(index//n,index%n) for index in lis]
    else:
        while path[i,j]!=-1:
            lis.append(path[i,j])
            j=path[i,j]
        lis=lis[::-1]
        arr=[(index//n,index%n) for index in lis]
    return arr, matrix[start[0]*n+start[1],end[0]*n+end[1]]

