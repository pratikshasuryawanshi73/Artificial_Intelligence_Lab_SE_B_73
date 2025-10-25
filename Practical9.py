def minimax(node, depth, player, game_tree, values):
    if depth == 0 or node not in game_tree:
        return values[node]

    if player == "MAX":
        alpha = float("-inf")
        for child in game_tree[node]:
            value = minimax(child, depth - 1, "MIN", game_tree, values)
            alpha = max(alpha, value)
        return alpha
    else:  
        alpha = float("inf")
        for child in game_tree[node]:
            value = minimax(child, depth - 1, "MAX", game_tree, values)
            alpha = min(alpha, value)
        return alpha


game_tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G']
}

values = { 
    'D': 3,
    'E': 5,
    'F': 6,
    'G': 9
}


result = minimax('A', 2, "MAX", game_tree, values)
print(result)