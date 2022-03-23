from collections import Counter


def f(ages, days):
    state = Counter(ages)

    for _ in range(days):
        new_state = Counter()
        for age, count in state.items():
            if age > 0:
                new_state[age - 1] += state[age]
            else:
                new_state[6] += state[0]
                new_state[8] += state[0]

        state = new_state

    return sum(state.values())


if __name__ == '__main__':
    ages = [int(x) for x in input().split(',')]
    print('13:', f(ages, 13))
    print('18:', f(ages, 18))
    print('80:', f(ages, 80))
    print('256:', f(ages, 256))
