def biggerIsGreater(w):
    # Write your code here
    i = len(w) - 1
    if "".join(sorted(w, reverse=True)) == w:
        return "no answer"

    while w[i - 1] >= w[i]:
        i -= 1
        if i == 0:
            break

    tail = w[i:]
    x = len(tail) - 1
    while tail[x] <= w[i-1]:
        x -= 1
    
    w_new = w[:i-1] + tail[x] + "".join(sorted(tail[:x] + tail[x+1:] + w[i-1]))
    return w_new