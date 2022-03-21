import sys
from itertools import islice


def f(measurements, k=1):
    it = map(sum, zip(*(islice(measurements, i, None) for i in range(k))))
    prev = None
    count = 0

    for value in it:
        if prev is not None:
            count += int(prev < value)
        prev = value

    return count


if __name__ == '__main__':
    measurements = list(map(int, sys.stdin.readlines()))
    print(f(measurements))
    print(f(measurements, k=3))
