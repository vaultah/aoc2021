import re


def count_shots(xmin, xmax, ymin, ymax):
    count = 0

    for vxi in range(1, xmax + 1):
        for vyi in range(ymin, abs(ymin) + 1):
            x, vx, y, vy = 0, vxi, 0, vyi

            while y >= ymin and x <= xmax:
                x += vx
                y += vy

                if xmin <= x <= xmax and ymin <= y <= ymax:
                    count += 1
                    break

                if vx > 0:
                    vx -= 1

                vy -= 1

    return count


if __name__ == '__main__':
    xmin, xmax, ymin, ymax = map(int, re.findall(r'-?\d+', input()))
    print((ymin + 1) * ymin // 2)
    print(count_shots(xmin, xmax, ymin, ymax))
