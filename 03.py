import sys


def gamma_epsilon(numbers):
    counts = [0] * len(numbers[0])
    for number in numbers:
        for i, value in enumerate(number):
            counts[i] += int(value == '1')

    most_common_bits = ''.join('1' if 2 * x > len(numbers) else '0' for x in counts)
    least_common_bits = most_common_bits.translate(str.maketrans('10', '01'))
    return int(most_common_bits, 2), int(least_common_bits, 2)


def oxygen(numbers):
    prefix = ''

    while True:
        prefixes = {}
        count = 0

        for number in numbers:
            prefixes.setdefault(prefix + number[len(prefix)], []).append(number)
            count += number[len(prefix)] == '1'

        most_common_bit = '1' if 2 * count >= len(numbers) else '0'
        numbers = prefixes[prefix + most_common_bit]
        if len(numbers) == 1:
            break

        prefix += most_common_bit

    return int(numbers[0], 2)


def co2(numbers):
    prefix = ''

    while True:
        prefixes = {}
        count = 0

        for number in numbers:
            prefixes.setdefault(prefix + number[len(prefix)], []).append(number)
            count += number[len(prefix)] == '1'

        least_common_bit = '1' if 2 * count < len(numbers) else '0'
        numbers = prefixes[prefix + least_common_bit]
        if len(numbers) == 1:
            break

        prefix += least_common_bit

    return int(numbers[0], 2)


if __name__ == '__main__':
    numbers = [x.strip() for x in sys.stdin.readlines()]
    gamma, epsilon = gamma_epsilon(numbers)
    print(gamma * epsilon)
    print(oxygen(numbers) * co2(numbers))
