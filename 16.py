import math


type_ops = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda x: int(x[0] > x[1]),
    6: lambda x: int(x[0] < x[1]),
    7: lambda x: int(x[0] == x[1]),
}


def to_int(bits):
    return int(bits, 2)


def decode(transmission):
    version = to_int(transmission[:3])
    type_id = to_int(transmission[3:6])

    if type_id == 4:
        offset = 6
        value = 0

        for i in range(offset + 5, len(transmission) - offset, 5):
            group_value = to_int(transmission[i - 5:i])
            group_flag = group_value >> 4 & 0b1
            value <<= 4
            value |= group_value & 0b1111
            if not group_flag:
                break

        return version, value, i

    else:
        op = type_ops[type_id]
        if to_int(transmission[6]):
            count = to_int(transmission[7:18])
            offset = 18
            values = []

            for _ in range(count):
                vrsn, value, i = decode(transmission[offset:])
                version += vrsn
                values.append(value)
                offset += i

            return version, op(values), offset

        else:
            length = to_int(transmission[7:22])
            offset = 22
            values = []
            processed = 0

            while processed < length:
                vrsn, value, i = decode(transmission[offset:])
                version += vrsn
                values.append(value)
                offset += i
                processed += i

            return version, op(values), offset


if __name__ == '__main__':
    transmission = ''.join(f'{int(x, 16):04b}' for x in input())
    version_sum, value, _ = decode(transmission)
    print(version_sum)
    print(value)
