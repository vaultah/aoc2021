import sys
from collections import Counter


def count_overlaps(lines, straight_only=True):
    intersections = Counter()

    for (x1, y1), (x2, y2) in lines:
        ix = -1 if x1 > x2 else 1 if x2 > x1 else 0
        iy = -1 if y1 > y2 else 1 if y2 > y1 else 0

        if straight_only and ix != 0 and iy != 0:
            continue

        while True:
            intersections[x1, y1] += 1
            if not (x1 != x2 or y1 != y2):
                break

            x1 += ix
            y1 += iy

    return sum(x > 1 for x in intersections.values())


if __name__ == '__main__':
    lines = [
        [tuple(map(int, y.split(','))) for y in x.split('->')]
        for x in sys.stdin.readlines()
    ]
    print(count_overlaps(lines))
    print(count_overlaps(lines, straight_only=False))
