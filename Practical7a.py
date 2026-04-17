from collections import deque

def bfs(maze, start, end):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    queue = deque([start])
    visited = set([start])
    
    parent = {}  
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse() 
            return path
        
        for dx, dy in directions:
            next_cell = (current[0] + dx, current[1] + dy)
            
            if (0 <= next_cell[0] < len(maze) and
                0 <= next_cell[1] < len(maze[0]) and
                maze[next_cell[0]][next_cell[1]] != '#' and
                next_cell not in visited):
                
                queue.append(next_cell)
                visited.add(next_cell)
                parent[next_cell] = current 
    
    return False  



maze = [
    ['S', '.', '.', '#', '.', '.', '.'],
    ['.', '#', '.', '#', '.', '#', '.'],
    ['.', '#', '.', '.', '.', '.', '.'],
    ['.', '.', '#', '#', '#', '.', '.'],
    ['.', '#', '.', '.', '.', '#', '.'],
    ['.', '#', '#', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.', '.', 'E'],
]

start = (0, 0)
end = (6, 6)

path = bfs(maze, start, end)
if path:
    print("Path found!")
    print(path)
else:
    print("No path exists.")