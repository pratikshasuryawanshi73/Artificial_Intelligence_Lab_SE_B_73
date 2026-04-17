def minimax(node, depth, player, game_tree, values):
   
    if node not in game_tree or depth == 0:
        return values[node]

    if player == "MAX":
        best = float("-inf")
        for child in game_tree[node]:
            val = minimax(child, depth - 1, "MIN", game_tree, values)
            best = max(best, val)
        return best
    else:  
        best = float("inf")
        for child in game_tree[node]:
            val = minimax(child, depth - 1, "MAX", game_tree, values)
            best = min(best, val)
        return best


game_tree = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': ['G', 'H'],
    'D': ['I'], 
    'E': ['J', 'K'],
    'F': ['L'],
    'G': ['M', 'N'],
    'H': ['O']
}


values = {
    'J': -6,
    'K': -1,
    'L': 2,
    'M': 9,
    'N': -9,
    'O': -8,
    'I': 9   
}


result = minimax('A', 3, "MAX", game_tree, values)
print("Optimal value using Minimax:", result)

