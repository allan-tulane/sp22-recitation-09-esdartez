from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """

    dist = {node: -1 for node in graph}
    weight = {node: -1 for node in graph}

    dist[source] = 0
    weight[source] = 0
    heap = [(0, source)]  
    while heap:
        d, top = heappop(heap)  
        for node, w in graph[top]:  
            if dist[node] == -1 or dist[node] > d + 1:
                dist[node] = d + 1
                weight[node] = weight[top] + w
                heappush(heap, (d + 1, node))
    return {node: (dist[node], weight[node]) for node in graph}
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
que = deque()
    que.append(source)
    parent = {source: None}
    while que:
        leftmost = que.popleft()
        for node in graph[leftmost]:
            if node not in parent:  
                parent[node] = leftmost 
                que.append(node)
    del parent[source]  
    return parent

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    path = []
    while destination in parents:
        path.append(parents[destination])
        destination = parents[destination]
    return "".join(path[::-1])

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'
