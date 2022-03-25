import sys
from statistics import median


invalid_scores = {
    ')': 3,
    ']': 57,
    '}': 1_197,
    '>': 25_137
}
completion_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
mapping = dict(['[]', '()', '{}', '<>'])
reverse_mapping = {v: k for k, v in mapping.items()}


def syntax_scoring(lines):
    invalid_total = 0
    completion_totals = []

    for line in lines:
        stack = []

        for char in line:
            if char in mapping:
                stack.append(char)
                continue

            if not stack or stack[-1] == reverse_mapping[char]:
                stack.pop()
            else:
                invalid_total += invalid_scores[char]
                break
        else:
            if not stack:
                continue

            completion_total = 0
            while stack:
                opening = stack.pop()
                completion_total *= 5
                completion_total += completion_scores[mapping[opening]]

            completion_totals.append(completion_total)

    return invalid_total, median(completion_totals)


if __name__ == '__main__':
    lines = [x.strip() for x in sys.stdin.readlines()]
    print(*syntax_scoring(lines))
