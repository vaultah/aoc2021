import sys


def first(moves):
    horizontal, vertical = 0, 0

    for direction, amount in moves:
        if direction == 'forward':
            horizontal += amount
        elif direction == 'up':
            vertical += amount
        elif direction == 'down':
            vertical -= amount

    return horizontal, vertical


def second(moves):
    horizontal, vertical, aim = 0, 0, 0

    for direction, amount in moves:
        if direction == 'forward':
            horizontal += amount
            vertical -= aim * amount
        elif direction == 'up':
            aim -= amount
        elif direction == 'down':
            aim += amount

    return horizontal, vertical


if __name__ == '__main__':
    moves = [
        (direction, int(amount))
        for direction, amount in map(str.split, sys.stdin.readlines())
    ]
    first_horizontal, first_vertical = first(moves)
    print(first_horizontal * -first_vertical)
    second_horizontal, second_vertical = second(moves)
    print(second_horizontal * -second_vertical)
