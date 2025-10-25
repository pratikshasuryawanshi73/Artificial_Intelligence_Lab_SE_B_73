def alphabeta(node, depth, alpha, beta, maximizingPlayer, values, index=0):
    
    if depth == 0 or index >= len(values):
        return values[index]

    if maximizingPlayer:
        best = float('-inf')
        for i in range(2):  
            val = alphabeta(node*2+i, depth-1, alpha, beta, False, values, index*2+i)
            best = max(best, val)
            
            alpha = max(alpha, best)
            if beta <= alpha:
                break  
        return best
    else:
        best = float('inf')
        for i in range(2):
            val = alphabeta(node*2+i, depth-1, alpha, beta, True, values, index*2+i)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break  # Alpha cut-off
        return best



values = [2, 3, 5, 9, 0, 1, 7, 5] 
depth = 3
result = alphabeta(0, depth, float('-inf'), float('inf'), True, values)

print("Optimal value (with Alpha-Beta Pruning):", result)