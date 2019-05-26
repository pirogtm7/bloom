import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Qwerty12345',
    db='flower',
    # charset='utf8mb4'
)

connection = mydb
mycursor = connection.cursor(buffered=True)
street = "SELECT street FROM client"
mycursor.execute(street)
street1 = mycursor.fetchone()
s1 = 'store1'
s2 = 'store2'
s3 = 'store3'
s4 = 'store4'
s5 = 'store5'
s6 = 'store6'

nodes = ('store1', 'store2', 'store3', 'store4', 'store5', 'store6', street1)
distances = {
    'store2': {'store1': 5, 'store4': 1, street1: 2},
    'store1': {'store2': 5, 'store4': 3, 'store5': 12, 'store6': 5},
    'store4': {'store2': 1, street1: 1, 'store5': 1, 'store1': 3},
    street1: {'store2': 2, 'store4': 1, 'store3': 2},
    'store3': {street1: 2, 'store5': 1, 'store6': 16},
    'store5': {'store1': 12, 'store4': 1, 'store3': 1, 'store6': 2},
    'store6': {'store1': 5, 'store5': 2, 'store3': 16}}


def dijkstra():
    unvisited = {node: None for node in nodes}  # using None as +inf
    visited = {}
    current = street1
    currentDistance = 0
    unvisited[current] = currentDistance
    while True:
        for neighbour, distance in distances[current].items():
            if neighbour not in unvisited: continue
            newDistance = currentDistance + distance
            if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                unvisited[neighbour] = newDistance
        visited[current] = currentDistance
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key=lambda x: x[1])[0]
    return visited


dijkstra()
