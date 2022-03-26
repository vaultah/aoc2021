import sys
from collections import Counter


def first(mapping):
    total_paths = 0
    stack = [('start', frozenset())]

    while stack:
        cave, small_visited = stack.pop()

        for nxt in mapping[cave]:
            if nxt == 'start' or nxt in small_visited:
                continue
            elif nxt == 'end':
                total_paths += 1
                continue

            if nxt.islower():
                temp = small_visited | {nxt}
            else:
                temp = small_visited

            stack.append((nxt, temp))

    return total_paths


def second(mapping):
    total_paths = 0
    stack = [('start', Counter())]

    while stack:
        cave, small_visited = stack.pop()

        for nxt in mapping[cave]:
            if nxt == 'start':
                continue

            if nxt == 'end':
                total_paths += 1
                continue

            if small_visited[nxt] and any(v > 1 for v in small_visited.values()):
                continue

            if nxt.islower():
                temp = small_visited.copy()
                temp[nxt] += 1
            else:
                temp = small_visited

            stack.append((nxt, temp))

    return total_paths


if __name__ == '__main__':
    lines = [x.strip() for x in sys.stdin.readlines()]
    mapping = {}

    for line in lines:
        source, destination = line.split('-')
        mapping.setdefault(source, []).append(destination)
        mapping.setdefault(destination, []).append(source)

    print(first(mapping))
    print(second(mapping))
