def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def read_elves(L):
    elves = []
    current_elf = []
    for line in L:
        if len(line) == 0:
            if len(current_elf) > 0:
                elves.append(current_elf)
            current_elf = []
        else:
            current_elf.append(int(line))
    if len(current_elf) > 0:
        elves.append(current_elf)
    return elves


def find_biggest_elf(elves):
    return max(elves, key=sum)


def sort_elves(elves):
    return sorted(elves, key=sum, reverse=True)


def solve_part1(filename):
    result = sum(find_biggest_elf(read_elves(parse(filename))))
    print(result)


def solve_part2(filename):
    sorted_elves = list(sort_elves(read_elves(parse(filename))))
    result = 0
    for i in range(3):
        result += sum(sorted_elves[i])
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day01.txt')
    else:
        solve_part1('day01.txt')
