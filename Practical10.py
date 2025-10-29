def alphabeta(node, depth, alpha, beta, maximizingPlayer, tree, values):
    
    if node not in tree:
        return values[node]
    
    if maximizingPlayer:
        maxEval = float('-inf')
        for child in tree[node]:
            eval = alphabeta(child, depth + 1, alpha, beta, False, tree, values)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                print(f"Pruned at node {child} (α={alpha}, β={beta})")
                break
        return maxEval
    else:
        minEval = float('inf')
        for child in tree[node]:
            eval = alphabeta(child, depth + 1, alpha, beta, True, tree, values)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                print(f"Pruned at node {child} (α={alpha}, β={beta})")
                break
        return minEval



tree = {
    'A': ['B', 'C', 'D'],
    'B': ['M', 'E', 'F'],
    'C': ['H', 'G', 'I'],
    'D': ['J', 'K', 'L']
}


values = {
    'M': 3,
    'E': 12,
    'F': 8,
    'H': 2,
    'G': 6,
    'I': 4,
    'J': 14,
    'K': 5,
    'L': 2
}


optimal_value = alphabeta('A', 0, float('-inf'), float('inf'), True, tree, values)
print("\nOptimal value (with Alpha-Beta Pruning):", optimal_value)
