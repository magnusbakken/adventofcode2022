def parse(filename):
    with open(filename, 'r') as f:
        return f.read().rstrip()


def is_marker(s, size):
    return len(set(s)) == size


def find_marker(s, size):
    for i in range(len(s)):
        if is_marker(s[i:i+size], size):
            return i + size
    return None


def solve_part1(filename):
    result = find_marker(parse(filename), 4)
    print(result)


def solve_part2(filename):
    result = find_marker(parse(filename), 14)
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day06.txt')
    else:
        solve_part1('day06.txt')
