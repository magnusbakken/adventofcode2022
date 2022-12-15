def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def parse_range(r):
    start, end = r.split('-')
    return set(range(int(start), int(end) + 1))


def parse_line(line):
    first, last = line.split(',')
    return (parse_range(first), parse_range(last))


def is_fully_contained(range1, range2):
    intersection = range1.intersection(range2)
    return len(intersection) == len(range1) or len(intersection) == len(range2)


def has_overlap(range1, range2):
    intersection = range1.intersection(range2)
    return len(intersection) > 0


def run_line1(line):
    return is_fully_contained(*parse_line(line))


def run_line2(line):
    return has_overlap(*parse_line(line))


def solve_part1(filename):
    result = len(list(filter(run_line1, parse(filename))))
    print(result)


def solve_part2(filename):
    result = len(list(filter(run_line2, parse(filename))))
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day04.txt')
    else:
        solve_part1('day04.txt')
