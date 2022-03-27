import math
import sys
from collections import defaultdict


def a_star(grid, *, r=1):
    n = len(grid)
    gscore = defaultdict(lambda: math.inf)
    fscore = defaultdict(lambda: math.inf)
    gscore[0, 0] = fscore[0, 0] = 0
    remaining = {(0, 0)}

    while remaining:
        i, j = min(remaining, key=fscore.__getitem__)
        if i == j == n * r - 1:
            break

        remaining.remove((i, j))

        for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if ni < 0 or nj < 0 or ni >= n * r or nj >= n * r:
                continue

            ti, pi = divmod(ni, n)
            tj, pj = divmod(nj, n)
            risk = gscore[i, j] + (grid[pi][pj] + ti + tj - 1) % 9 + 1

            if risk < gscore[ni, nj]:
                gscore[ni, nj] = risk
                fscore[ni, nj] = risk + abs(ni - i) - abs(nj - j)
                remaining.add((ni, nj))

    return gscore[n * r - 1, n * r - 1]


if __name__ == '__main__':
    grid = [[int(x) for x in line] for line in map(str.strip, sys.stdin) if line]
    print('r = 1:', a_star(grid))
    print('r = 5:', a_star(grid, r=5))
