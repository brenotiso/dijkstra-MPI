import sys
import time
from mpi4py import MPI


def path(prev, src, dest):
    # monta o caminho até o destino
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


def dijkstra(local_v, nodes, n):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    def min_dist():
        # encontra a menor distancia no set local
        dist = float('inf')
        pos = -1
        for index, distance in enumerate(set):
            if distance < dist:
                dist = distance
                pos = index
        return set[pos]

    dist = {}
    prev = {}

    set = []
    # inicializando o set local
    for i in range(len(local_v)):
        dist[i] = float('inf')
        prev[i] = -1
        set.append(i)
    if rank == 0:
        dist[0] = 0

    for _ in range(nodes):
        local_min = [float('inf'), rank]
        if len(set) != 0:
            actual = min_dist()
            local_min = [dist[actual], rank * n + actual]

        # encontrando o minimo global
        actual_global = comm.allreduce(local_min, op=MPI.MINLOC)

        global_dist = actual_global[0]
        global_pos = actual_global[1]

        # se o minimo global for desse processo, o elemento é removido do set
        if ((actual_global[1] - actual) / n) == rank:
            if global_dist == float('inf'):
                continue
            set.remove(actual)
            global_pos = rank * n + actual

        # atualizando as distancias em relacao ao global
        for neigthbor, col in enumerate(local_v):
            if col[global_pos] != 0 and (neigthbor in set):
                distance = global_dist + col[global_pos]
                if distance < dist[neigthbor]:
                    dist[neigthbor] = distance
                    prev[neigthbor] = global_pos

    return dist, prev

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        start_time = time.time()

    processes = comm.Get_size()
    local_v = None  # colunas dos processos
    division = None
    nodes = None
    n = None  # quantidade de colunas por processo
    if rank == 0:
        if len(sys.argv) != 4:
            print('Foramto de execução: {} <arquivo-test> <origem> <destino>'.format(sys.argv[0]))
            sys.exit(1)

        file = sys.argv[1]
        source = int(sys.argv[2])
        destination = int(sys.argv[3])

        # leitura do arquivo
        try:
            f = open(file, "r")
        except FileNotFoundError:
            print('Arquivo de entrada não encontrado.')
            sys.exit(1)

        f.readline()  # ignora primeira linha (dl)
        nodes = int(f.readline().split("=")[1])  # leitura da qtd de vértices
        f.readline()  # ignora primeira linha (format=edgelist1)
        f.readline()  # ignora primeira linha (data:)

        graph = []
        for i in range(nodes):
            graph.append([])
            for _ in range(nodes):
                graph[i].append(0)

        for line in f:
            row = line.split(" ")
            graph[int(row[0]) - 1][int(row[1]) - 1] = int(row[2][:-1])
        # print(graph)

        # configurando a execução paralela
        n = int(nodes / processes)
        chunck = nodes % processes
        division = []
        for i in range(processes):
            columns = []
            for j in range(i * n, (i + 1) * n):
                columns.append([row[j] for row in graph])
            division.append(columns)
        if chunck:
            # sobrou colunas a serem divididas
            # elas seram colocadas para o ultimo processo
            # para assim manter a ordem das colunas
            for j in range(nodes - chunck, nodes):
                column = [row[j] for row in graph]
                division[-1].append(column)

        # print(division)

    nodes = comm.bcast(nodes, root=0)
    n = comm.bcast(n, root=0)
    # division guarda as colunas divididas pelo número de processos
    # para então fazer o scatter (enviar para os processos)
    local_v = comm.scatter(division, root=0)

    loc_dist, loc_pred = dijkstra(local_v, nodes, n)

    # juntando os resutlados
    dist_global = comm.gather(loc_dist, root=0)
    prev_global = comm.gather(loc_pred, root=0)

    if rank == 0:
        # print(dist_global)
        # print(prev_global)

        # juntando as distancias
        result_dist = {}
        i = 0
        while i < nodes:
            for dict_dit in dist_global:
                for j in dict_dit:
                    result_dist[i] = dict_dit[j]
                    i += 1

        # juntando os anteriores
        result_prev = {}
        i = 0
        while i < nodes:
            for dict_prev in prev_global:
                for j in dict_prev:
                    result_prev[i] = dict_prev[j]
                    i += 1

        # print(result_dist)
        # print(result_prev)

        try:
            print("Custo de 0 até {}: {}".format(destination, result_dist[destination]))
            print("Caminho: ", path(result_prev, 0, destination))
        except KeyError:
            print("Não é possível alcançar {} por 0.".format(destination))

        print("\n--- %s seconds ---" % (time.time() - start_time))

    MPI.Finalize()
