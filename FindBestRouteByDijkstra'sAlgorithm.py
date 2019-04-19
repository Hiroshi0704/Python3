######################################################################################## import
import math
######################################################################################## setting
################################################ ユーザ指定項目
# [開始位置, 目的地, コスト]
ROUTE_INFORMAION = [
    [0,1, 200],
    [0,2, 300],
    [0,3, 400],
    [1,2, 500],
    [1,3, 600],
    [2,4, 700],
    [3,4, 800],
]
SIZE = 5
################################################ ユーザ指定項目 ここまで
VISITED     = 1
NOT_VISITED = 0

ROUTE_DATA = [[math.inf for _ in range(SIZE)] for _ in range(SIZE)]
for i in ROUTE_INFORMAION:
    x = i[0]
    y = i[1]
    v = i[2]
    ROUTE_DATA[x][y] = v

cost    = [math.inf for _ in range(SIZE)]
visit   = [NOT_VISITED for _ in range(SIZE)]
before  = [None for _ in range(SIZE)]
cost[0] = 0

for e, i in enumerate(ROUTE_DATA):
    print('ROUTE_DATA{} : {}'.format(str(e).rjust(2),i))
print('size         : {}'.format(SIZE))
print('cost         : {}'.format(cost))
print('visit        : {}'.format(visit))
print('before       : {}'.format(before))
print('cost[0] = 0  : {}'.format(cost))
print('==============================='*2)
######################################################################################## class
######################################################################################## def
######################################################################################## main
if __name__ == '__main__':
    while True:
        min = math.inf
        for i in range(SIZE):
            if visit[i] == NOT_VISITED and cost[i] < min:
                x = i
                min = cost[x]
        if min == math.inf: break
        visit[x] = VISITED

        for i in range(SIZE):
            if cost[i] > (cost[x] + ROUTE_DATA[x][i]):
                cost[i] = (cost[x] + ROUTE_DATA[x][i])
                before[i] = x

        print('size         : {}'.format(SIZE))
        print('cost         : {}'.format(cost))
        print('visit        : {}'.format(visit))
        print('before       : {}'.format(before))
        print('-------------------------------'*2)

    best_route = []
    i = SIZE - 1
    while True:
        best_route.insert(0, i)
        if i == 0: break
        i = before[i]

    print('The Best Route is')
    print(' [ ', end='')
    for i in best_route[:-1]:
        print(i, end=' -> ')
    print(best_route[-1], end=' ]\n')
    print('==============================='*2)
######################################################################################## test