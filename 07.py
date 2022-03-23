from statistics import median


def first(positions):
    mdn = int(median(positions))
    return sum(abs(mdn - x) for x in positions)


def second(positions):
    sorted_positions = sorted(positions)
    return min(
        sum((abs(x - p) + 1) * abs(x - p) // 2 for x in positions)
        for p in range(sorted_positions[0], sorted_positions[-1] + 1)
    )


if __name__ == '__main__':
    positions = [int(x) for x in input().split(',')]
    print(first(positions))
    print(second(positions))
