"""
N := 격자 크기
M := 사람의 수

graph := 0-> 이동가능, 1-> 베이스캠프
"""
from collections import deque
# 상, 좌, 우, 하
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
t = 0
N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
stores = list()
baseCamps = list()
clearTime = [0] * M
for _ in range(M):
    x, y = map(int, input().split())
    stores.append([x - 1, y - 1])

for x in range(N):
    for y in range(N):
        if graph[x][y] == 0:
            continue
        baseCamps.append([x, y])

baseCamps.sort(key=lambda x:(x[0], x[1]))

def isNotInRange(x, y) -> bool:
    return x < 0 or x >= N or y < 0 or y >= N

def findBaseCamp(start, targets) -> any:
    """
    가장 가까운 베이스캠프 좌표를 리턴
    """
    q = deque()
    q.append(start)
    visited = [[False] * N for _ in range(N)]
    res = list()
    while q:
        x, y = q.popleft()

        # 어떤 베이스캠프에 도착했다면, 
        if [x, y] in targets:
            res.append([x, y])
            
        else:
            for i in range(4):  
                nx = x + dx[i]
                ny = y + dy[i]

                if isNotInRange(nx, ny): continue
                if graph[nx][ny] == 2: continue
                if visited[nx][ny]: continue
                visited[nx][ny] = True
                q.append([nx, ny])

        if res:
            res.sort(key = lambda x: (x[0], x[1]))
            return res[0]


game = deque()
visited = [[False] * N for _ in range(N)]
t = 0

while game or t == 0:
    nq = deque()
    rmList = list()

    for player, x, y in game:
        if clearTime[player] != 0: continue
        nPoints = [[x + dx[i], y + dy[i]] for i in range(4) if not isNotInRange(x + dx[i], y + dy[i])]
        nx, ny = findBaseCamp(stores[player], nPoints)

        if [nx, ny] == stores[player]:
            clearTime[player] = t
            rmList.append([nx, ny])
        else:
            nq.append([player, nx, ny])

    game = nq
    for x, y in rmList: 
        graph[x][y] = 2
               
    if t < M:
        # t번째 사람 행이 작은, 열이 작은 베캠으로 들어가기
        x, y = findBaseCamp(stores[t], baseCamps)
        graph[x][y] = 2
        game.append([t, x, y])
        baseCamps.remove([x, y])

    t += 1

print(max(clearTime) + 1)