import numpy as np

def create_data(m,n):
    matrix=np.zeros((m,n),dtype='int')
    for i in range(3):
        x,y=np.random.randint(1,m-1),np.random.randint(1,n-1)
        matrix[x,y]=4
    for x in range(m):
        for y in range(n):
            if matrix[x,y]!=4:
                matrix[x,y]=np.random.randint(0,4)
    matrix[0,0]=0
    x_start, y_start = 0, 0
    a=True
    while a:
        x_start, y_start=np.random.randint(0,m),np.random.randint(0,n)
        if matrix[x_start,y_start]!=4:
            a=False

    return matrix,x_start,y_start


