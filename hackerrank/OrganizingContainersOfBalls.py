def organizingContainers(container):
    # Write your code here
    n = len(container)
    row_sums = [sum(row) for row in container]
    col_sums = [sum(container[i][j] for i in range(n)) for j in range(n)]
    
    if sorted(row_sums) == sorted(col_sums):
        return "Possible"
    else: return "Impossible"