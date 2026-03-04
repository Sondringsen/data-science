def gridSearch(G, P):
    # Write your code here
    t_r = len(G)
    t_c = len(G[0])
    p_r = len(P)
    p_c = len(P[0])
    for n in range(t_r - p_r + 1):
        for x in range(t_c - p_c + 1):
            is_sub = True
            for i in range(p_r):
                if G[n + i][x: x+p_c] != P[i]:
                    is_sub = False
                    break
            if is_sub: return "YES"
                      
    return "NO"