import math

INF         = math.inf
VISITED     = 1
NOT_VISITED = 0

route = [
    [INF, 2, 3, INF, INF, INF],
    [2, INF, 4, 3, 5, INF],
    [3, 4, INF, 6, 4, INF],
    [INF, 3, 6, INF, 1, 5],
    [INF, 5, 4, 1, INF, 3],
    [INF, INF, INF, 5, 3, INF]
    ]
# 場所の数を格納
size    = len(route)
# それぞれの場所への最小コストを格納
cost    = [INF for _ in range(size)]
# 探索済みかどうか格納
visit   = [NOT_VISITED for _ in range(size)]
# それぞれ場所への最短ルートの直前の場所を格納
before  = [None for _ in range(size)]
# スタート位置のコストを０とする
cost[0] = 0

print('size       : {}'.format(size))
print('cost       : {}'.format(cost))
print('visit      : {}'.format(visit))
print('before     : {}'.format(before))
print('cost[0] = 0: {}'.format(cost))
print('==============================='*2)

while True:
    min = INF
    for i in range(size):
        if visit[i] == NOT_VISITED and cost[i] < min:
            x = i
            min = cost[x]
    if min == INF: break
    visit[x] = VISITED

    for i in range(size):
        if cost[i] > route[x][i] + cost[x]:
            cost[i] = route[x][i] + cost[x]
            before[i] = x

    print("visited to {}".format(x))
    print('cost       : {}'.format(cost))
    print('visit      : {}'.format(visit))
    print('before     : {}'.format(before))
    print('-------------------------------'*2)
 
i = size - 1
optimum_route = []
while True:
    optimum_route.insert(0, i)
    if i == 0: break
    i = before[i]

print("minimal cost is {}.".format(cost[size-1]))
print('optinum route is ', end='')
for o in optimum_route[:-1]:
    print(o, end=' -> ')
print(optimum_route[-1])
print('==============================='*2)