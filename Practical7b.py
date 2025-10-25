def dfs(maze, start, end):
    stack = [start] 
    visited = set() 

    while stack:
        position = stack.pop() 
        x, y = position

        
        if position == end:
            return True

        
        visited.add((x, y))

        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy

            
            if (0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and
                    maze[new_x][new_y] == 0 and (new_x, new_y) not in visited):
                stack.append((new_x, new_y))

    return False 


maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]


start = (0, 0)
end = (4, 4)


print(dfs(maze, start, end)) 