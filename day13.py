import functools


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def parse_packets(lines):
    pairs = []
    for idx in range(len(lines) // 3 + 1):
        left = eval(lines[idx*3])
        right = eval(lines[idx*3 + 1])
        pairs.append((left, right))
    return pairs


def printif(debug, s):
    if debug:
        print(s)


def compare_pair(left, right, debug=False, indent_level=0):
    indent = ' ' * (indent_level * 2)
    printif(debug, '{}- Compare {} vs {}'.format(indent, left, right))
    for idx in range(len(left)):
        if idx >= len(right):
            printif(debug,
                    '{}  - Right side ran out of items, so inputs are not in the right order'.format(indent))
            return False

        if isinstance(left[idx], list):
            if isinstance(right[idx], list):
                inner_result = compare_pair(
                    left[idx], right[idx], indent_level=indent_level+1)
                if inner_result is not None:
                    return inner_result
            else:
                printif(debug, '{}  - Compare {} vs {}'.format(indent,
                                                               left[idx], right[idx]))
                printif(debug,
                        '{}    - Mixed types; convert right to {} and retry comparison'.format(indent, [right[idx]]))
                inner_result = compare_pair(
                    left[idx], [right[idx]], indent_level=indent_level+2)
                if inner_result is not None:
                    return inner_result
        elif isinstance(right[idx], list):
            printif(debug, '{}  - Compare {} vs {}'.format(indent,
                                                           left[idx], right[idx]))
            printif(debug,
                    '{}    - Mixed types; convert left to {} and retry comparison'.format(indent, [left[idx]]))
            inner_result = compare_pair(
                [left[idx]], right[idx], indent_level=indent_level+2)
            if inner_result is not None:
                return inner_result
        else:
            printif(debug, '{}  - Compare {} vs {}'.format(indent,
                                                           left[idx], right[idx]))
            if left[idx] < right[idx]:
                printif(debug,
                        '{}    - Left side is smaller, so inputs are in the right order'.format(indent))
                return True
            elif left[idx] > right[idx]:
                printif(debug,
                        '{}    - Right side is smaller, so inputs are not in the right order'.format(indent))
                return False

    if len(left) < len(right):
        printif(
            debug, '{}  - Left side ran out of items, so inputs are in the right order'.format(indent))
        return True

    return None


def compare_sort(left, right):
    result = compare_pair(left, right)
    return -1 if result else 1 if not result else 0


def compare_all(pairs):
    correct = []
    for idx, (left, right) in enumerate(pairs):
        print('== Pair {} =='.format(idx + 1))
        if compare_pair(left, right, debug=True):
            correct.append(idx + 1)
        print()
    print(correct)
    return sum(correct)


def sort_all(pairs):
    key = functools.cmp_to_key(compare_sort)
    return sorted(pairs, key=key)


def solve_part1(filename):
    result = compare_all(parse_packets(list(parse(filename))))
    print(result)


def solve_part2(filename):
    pairs = parse_packets(list(parse(filename)))
    packets = []
    for left, right in pairs:
        packets.extend([left, right])
    start, end = [[2]], [[6]]
    packets.extend([start, end])
    result = sort_all(packets)
    start_idx, end_idx = result.index(start), result.index(end)
    print((start_idx + 1) * (end_idx + 1))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day13.txt')
    else:
        solve_part1('day13.txt')
