import math
import sys


def fold_paper(dots, instructions):
    grid = set(dots)

    for axis, num in instructions:
        index = int(axis == 'y')

        for point in list(grid):
            if point[index] > num:
                *new_point, = point
                new_point[index] = 2 * num - new_point[index]
                grid.remove(point)
                grid.add((*new_point,))

    return grid


if __name__ == '__main__':
    dots = []
    instructions = []

    for line in sys.stdin:
        if not line.strip():
            break
        x, y = map(int, line.split(','))
        dots.append((x, y))

    for line in sys.stdin:
        axis, num = line.split('=')
        instructions.append((axis.rsplit(' ', 1)[-1], int(num)))

    grid = fold_paper(dots, [instructions[0]])
    print('Points after the first fold:', len(grid))

    grid = fold_paper(dots, instructions)
    xs, ys = zip(*grid)

    print('Final code:')
    for y in range(max(ys) + 1):
        for x in range(max(xs) + 1):
            print('#' if (x, y) in grid else ' ', end='')
        print()
