import sys
import time


def path(prev, src, dest):
    path = [dest]
    actual = prev[dest]
    path.append(actual)
    while actual != src:
        path.append(actual)
        actual = prev[actual]
    string = ''
    for x in path[::-1]:
        string += "{} ".format(x)
    return string


def dijkstra(graph, src, nodes):
    dist = {}
    prev = {}

    def min_dist():
        dist = float('inf')
        pos = -1
        for index, distance in enumerate(set):
            if distance < dist:
                dist = distance
                pos = index
        return set[pos]

    set = []
    for i in range(nodes):
        dist[i] = float('inf')
        prev[i] = -1
        set.append(i)

    dist[src] = 0

    while len(set) != 0:
        actual = min_dist()
        set.remove(actual)
        for neigthbor, element in enumerate(graph[actual]):
            if element != 0 and (neigthbor in set):
                distance = dist[actual] + element
                if distance < dist[neigthbor]:
                    dist[neigthbor] = distance
                    prev[neigthbor] = actual

    return dist, prev

if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) != 4:
        print('Foramto de execução: {} <arquivo-test> <origem> <destino>'.format(sys.argv[0]))
        sys.exit(1)

    file = sys.argv[1]
    source = int(sys.argv[2])
    destination = int(sys.argv[3])

    f = open(file, "r")
    f.readline()
    nodes = int(f.readline().split("=")[1])
    f.readline()
    f.readline()

    graph = []
    for i in range(nodes):
        graph.append([])
        for _ in range(nodes):
            graph[i].append(0)

    for line in f:
        row = line.split(" ")
        graph[int(row[0]) - 1][int(row[1]) - 1] = int(row[2][:-1])

    dist, prev = dijkstra(graph, source, nodes)

    # print(dist)
    # print(prev)

    try:
        print("Custo de {} até {}: {}".format(source, destination, dist[destination]))
        print("Caminho: ", path(prev, source, destination))
    except KeyError:
        print("Não é possível alcançar {} por {}.".format(destination, source))

    print("\n--- %s seconds ---" % (time.time() - start_time))
