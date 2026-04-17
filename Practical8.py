import heapq


graph = {
    'S': {'A': 1, 'B': 4},
    'A': {'B': 2, 'C': 5, 'D': 12},
    'B': {'C': 2},
    'C': {'D': 3, 'G': 7},
    'D': {'G': 2},
    'G': {}
}


heuristics = {
    'S': 7, 'A': 6, 'B': 4,
    'C': 2, 'D': 1, 'G': 0
}

def astar(graph, heuristics, start, goal):
   
    open_list = [(heuristics[start], 0, start, [start])]
    visited = {}

    while open_list:
        f, g, node, path = heapq.heappop(open_list)

        
        if node == goal:
            return path, g

        if node in visited and visited[node] <= g:
            continue
        visited[node] = g

       
        for neighbor, cost in graph[node].items():
            g_new = g + cost
            f_new = g_new + heuristics[neighbor]
            heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None, float("inf")


start, goal = 'S', 'G'
path, cost = astar(graph, heuristics, start, goal)
print("Shortest Path:", path)
print("Total Cost:", cost)