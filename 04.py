import sys


def f(number, data, k):
    M = len(data) // k
    N = k * k

    def _t(col_index):
        return k * (col_index % M) + col_index // M

    for j, x in enumerate(data):
        if number == x:
            data[j] = None

    for j in range(0, len(data), k):
        if all(data[j + l] is None for l in range(k)):
            start = j - j % N
            board = j // N
        elif all(data[_t(j + l)] is None for l in range(k)):
            row_index = _t(j)
            board = row_index // N
            start = row_index - row_index % N
        else:
            continue

        yield board, sum(x for x in data[start:start + N] if x is not None)


if __name__ == '__main__':
    k = 5
    scores = {}
    lines_it = iter(sys.stdin.readlines())
    numbers = [int(x) for x in next(lines_it).split(',')]
    data = [y for x in lines_it if x.strip() for y in map(int, x.split())]

    for number in numbers:
        for board, unmarked in f(number, data, k):
            if board not in scores:
                scores[board] = number * unmarked

    winners = list(scores.items())
    print('First won:', *winners[0])
    print('Last won:', *winners[-1])
