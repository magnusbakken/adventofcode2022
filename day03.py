import sys
import itertools


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def get_priority(letter):
    c = ord(letter)
    if c >= ord('a') and c <= ord('z'):
        return c - ord('a') + 1
    else:
        return c - ord('A') + 27


def parse_line(line):
    pivot = len(line) // 2
    return line[:pivot], line[pivot:]


def find_shared_letters(left, right):
    l, r = set(left), set(right)
    return tuple(l.intersection(r))


def find_badge(elves):
    elf1, elf2, elf3 = elves
    elf1_items = set(elf1)
    elf2_items = set(elf2)
    elf3_items = set(elf3)
    result = list(elf1_items.intersection(elf2_items).intersection(elf3_items))
    if len(result) != 1:
        print('Wrong set of elves')
        sys.exit(1)
    return result[0]


def run_line(line):
    left, right = parse_line(line)
    shared_letters = find_shared_letters(left, right)
    return sum(map(get_priority, shared_letters))


def chunk_elves(lines):
    iterator = iter(lines)
    return iter(lambda: tuple(itertools.islice(iterator, 3)), ())


def solve_part1(filename):
    result = sum(map(run_line, parse(filename)))
    print(result)


def solve_part2(filename):
    result = sum(map(get_priority, map(
        find_badge, chunk_elves(parse(filename)))))
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day03.txt')
    else:
        solve_part1('day03.txt')
