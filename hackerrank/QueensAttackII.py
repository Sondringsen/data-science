def queensAttack(n, k, r_q, c_q, obstacles):
    """
    For each of 8 directions, find the closest obstacle (or board edge).
    Only the closest obstacle in each direction matters - it blocks the rest.
    """
    # Track closest blocker in each direction (closest = minimum distance from queen)
    # We use infinity to mean "no obstacle in this direction"
    up = n - r_q
    down = r_q - 1
    right = n - c_q
    left = c_q - 1
    up_right = min(n - r_q, n - c_q)
    up_left = min(n - r_q, c_q - 1)
    down_right = min(r_q - 1, n - c_q)
    down_left = min(r_q - 1, c_q - 1)

    for r_o, c_o in obstacles:
        # Same column - up or down
        if c_o == c_q:
            if r_o > r_q:
                up = min(up, r_o - r_q - 1)
            elif r_o < r_q:
                down = min(down, r_q - r_o - 1)

        # Same row - left or right
        elif r_o == r_q:
            if c_o > c_q:
                right = min(right, c_o - c_q - 1)
            elif c_o < c_q:
                left = min(left, c_q - c_o - 1)

        # Diagonal
        elif abs(r_o - r_q) == abs(c_o - c_q):
            dist = abs(r_o - r_q) - 1
            if r_o > r_q and c_o > c_q:
                up_right = min(up_right, dist)
            elif r_o > r_q and c_o < c_q:
                up_left = min(up_left, dist)
            elif r_o < r_q and c_o > c_q:
                down_right = min(down_right, dist)
            elif r_o < r_q and c_o < c_q:
                down_left = min(down_left, dist)

    return up + down + left + right + up_right + up_left + down_right + down_left
