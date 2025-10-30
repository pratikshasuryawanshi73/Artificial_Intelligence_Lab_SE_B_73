def dfs(maze, start, end):
    stack = [start]  
    visited = set([start])  
    parent = {start: None}  

    while stack:
        position = stack.pop()
        x, y = position

        
        if position == end:
            path = []
            while position is not None:
                path.append(position)
                position = parent[position]
            path.reverse()
            return path

       
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            new_pos = (new_x, new_y)

            
            if (0 <= new_x < len(maze) and
                0 <= new_y < len(maze[0]) and
                maze[new_x][new_y] != '#' and
                new_pos not in visited):
                stack.append(new_pos)
                visited.add(new_pos)
                parent[new_pos] = position

    return None  



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


path = dfs(maze, start, end)

if path:
    print("Path found:", path)
else:
    print("No path exists.")
