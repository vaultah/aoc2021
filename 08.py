import sys


def first(entries):
    return sum(
        sum(x in {2, 3, 4, 7} for x in map(len, out))
        for _, out in entries
    )


def second(entries):
    total = 0

    for values, out in entries:
        mapping = {}
        wiring = {}
        unknown = []

        (
            mapping[8],
            *unknown,
            mapping[4],
            mapping[7],
            mapping[1],
        ) = sorted(map(frozenset, values), key=len, reverse=True)

        for value in unknown:
            if len(value) == 6:
                if len(g := value - mapping[4] - mapping[7]) == 1:
                    wiring['g'], = g
                    mapping[9] = value
                elif len(c := mapping[1] - value):
                    wiring['c'], = c
                    mapping[6] = value
                else:
                    mapping[0] = value

            elif len(value) == 5:
                if value > mapping[1]:
                    mapping[3] = value
                elif len(mapping[9] - value) == 1:
                    mapping[5] = value
                else:
                    mapping[2] = value

        wiring['a'], = mapping[7] - mapping[1]
        wiring['b'], = mapping[9] - mapping[3]
        wiring['d'], = mapping[8] - mapping[0]
        wiring['e'], = mapping[8] - mapping[9]
        wiring['f'], = mapping[1] & mapping[6] & mapping[3]

        reverse_mapping = {v: k for k, v in mapping.items()}
        integer_value = 0

        for i, value in enumerate(map(frozenset, out), start=1):
            total += reverse_mapping[value] * 10 ** (len(out) - i)

        total += integer_value

    return total


if __name__ == '__main__':
    entries = [tuple(y.split() for y in x.split('|')) for x in sys.stdin.readlines()]
    print(first(entries))
    print(second(entries))
