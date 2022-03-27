import sys
from collections import Counter


def step(state, rules):
    for pair, count in list(state.items()):
        if count < 1:
            continue

        try:
            repl = rules[pair]
        except KeyError:
            continue
        else:
            state[pair] -= count
            state[pair[0] + repl] += count
            state[repl + pair[1]] += count


def state_diff(state):
    counts = Counter()
    for pair, count in state.items():
        counts[pair[0]] += count
        counts[pair[1]] += count

    common = counts.most_common()
    return (common[0][1] + 1) // 2 - (common[-1][1] + 1) // 2


if __name__ == '__main__':
    template = input()
    rules = dict(line.split(' -> ') for line in map(str.strip, sys.stdin) if line)
    state = Counter(template[i:i+2] for i in range(len(template) - 1))

    for _ in range(1, 11):
        step(state, rules)

    print(state_diff(state))

    for _ in range(11, 41):
        step(state, rules)

    print(state_diff(state))
