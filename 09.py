import math
import sys


def get_low_points(heightmap):
    for i in range(len(heightmap)):
        for j in range(len(heightmap[0])):
            value = heightmap[i][j]
            if (
                (i == 0 or heightmap[i - 1][j] > value) and
                (i == len(heightmap) - 1 or heightmap[i + 1][j] > value) and
                (j == 0 or heightmap[i][j - 1] > value) and
                (j == len(heightmap[0]) - 1 or heightmap[i][j + 1] > value)
            ):
                yield i, j


def get_basins(heightmap, low_points):
    for low_point in low_points:
        points = set()
        stack = [low_point]

        while stack:
            i, j = point = stack.pop()
            if point in points:
                continue

            points.add(point)

            if i != 0 and heightmap[i - 1][j] < 9:
                stack.append((i - 1, j))

            if j != 0 and heightmap[i][j - 1] < 9:
                stack.append((i, j - 1))

            if i != len(heightmap) - 1 and heightmap[i + 1][j] < 9:
                stack.append((i + 1, j))

            if j != len(heightmap[0]) - 1 and heightmap[i][j + 1] < 9:
                stack.append((i, j + 1))

        yield points


if __name__ == '__main__':
    heightmap = [[int(y) for y in x.strip()] for x in sys.stdin.readlines()]
    low_points = list(get_low_points(heightmap))
    print(sum(heightmap[i][j] + 1 for i, j in low_points))
    basins = get_basins(heightmap, low_points)
    print(math.prod(sorted(map(len, basins))[-3:]))
