import sys


def next_step(grid):
    total_flashes = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j] += 1

    flashed = set()
    stack = []

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] > 9:
                stack.append((i, j))

    while stack:
        i, j = stack.pop(0)
        if (i, j) in flashed:
            continue

        if grid[i][j] < 9:
            grid[i][j] += 1
            continue

        grid[i][j] = 0
        total_flashes += 1
        flashed.add((i, j))

        for ni in range(i - 1, i + 2):
            for nj in range(j - 1, j + 2):
                if ni == i and nj == j:
                    continue

                if ni < 0 or nj < 0 or ni > len(grid) - 1 or nj > len(grid) - 1:
                    continue

                stack.append((ni, nj))

    return total_flashes


if __name__ == '__main__':
    grid = [[int(y) for y in x.strip()] for x in sys.stdin.readlines()]

    step = 1
    total_flashes = 0
    flashes_at_step = {}
    all_flashed = False

    while not all_flashed or step <= 100:
        total_flashes += next_step(grid)
        flashes_at_step[step] = total_flashes

        if step == 100:
            print('Flashes after step 100:', total_flashes)

        if not all_flashed and not any(map(any, grid)):
            all_flashed = True
            print(f'All octopuses flashed at step {step}')

        step += 1
