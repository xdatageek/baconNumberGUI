class Graph:

    def minimum_distance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1

        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def dijkstra(self, graph, src):
        row = len(graph)
        col = len(graph[0])
        dist = [float("Inf")] * row
        parent = [-1] * row
        dist[src] = 0
        queue = []

        for i in range(row):
            queue.append(i)

        while queue:
            u = self.minimum_distance(dist, queue)
            queue.remove(u)
            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
        return dist, parent


def create_result(films, actors, years, destination):
    output = ''
    g = Graph()
    distance, parents = g.dijkstra(create_adjacency_matrix(actors), 0)
    output += "Path from %s to %s:\n" % (list(actors)[destination], list(actors)[0])
    result = create_path(parents, destination, output, actors, films, years)
    result += "%s`s Bacon number is %d." % (list(actors)[destination], distance[destination])
    return result


def create_path(parent, j, path, actors, films, years):
    if parent[j] == -1:
        return path
    film = get_common_film(list(actors)[parent[j]], list(actors)[j], films)
    year = years[film]
    path += "%s was in %s (%s) with %s \n" % (list(actors)[j], film, year, list(actors)[parent[j]])
    path = create_path(parent, parent[j], path, actors, films, years)
    return path


def create_adjacency_matrix(dictionary):
    keys = list(dictionary.keys())
    size = len(keys)

    matrix = [[0] * size for i in range(size)]

    for a, b in [(keys.index(a), keys.index(b)) for a, row in dictionary.items() for b in row]:
        matrix[a][b] = 2 if (a == b) else 1
    return matrix


def get_common_film(first_actor, second_actor, films):
    for film in films[first_actor]:
        if film in films[second_actor]:
            return film


def get_actors(read_json, films, ignore: str):
    actor_list = []
    for film in films:

        for item in read_json:
            if item['name'] == ignore:
                continue

            if film in item['films'] and not (item['name'] in actor_list):
                actor_list.append(item['name'])

    return actor_list
