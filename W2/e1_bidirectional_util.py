def bfs_routine(src_queue, src_visited, src_parent, graph):
    current = src_queue.pop(0)
    connected_node = graph[current]

    while connected_node:
        vertex = connected_node.vertex
        if not src_visited[vertex]:
            src_queue.append(vertex)
            src_visited[vertex] = True
            src_parent[vertex] = current
        connected_node = connected_node.next

    return src_queue, src_visited, src_parent

def explore(path, graph, intersecting_node, src, dest):
    i = intersecting_node
    while i != src:
        path.append(graph.src_parent[i])
        i = graph.src_parent[i]
    path = path[::-1]
    i = intersecting_node
    while i != dest:
        path.append(graph.dest_parent[i])
        i = graph.dest_parent[i]
    return path