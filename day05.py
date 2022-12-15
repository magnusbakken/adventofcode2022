from collections import namedtuple
import re

Move = namedtuple('Move', ['amount', 'source', 'destination'])

CRATE_RE = re.compile('\[([A-Z])\]')
MOVE_RE = re.compile('move (\d+) from (\d+) to (\d+)')


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def parse_crates(lines):
    stacks = []
    for line in lines:
        if len(line) == 0:
            break

        idx = 0
        while idx <= len(line) // 4:
            if idx >= len(stacks):
                stacks.append([])
            offset = idx * 4
            match = CRATE_RE.match(line[offset:offset+4])
            if match:
                stacks[idx].insert(0, match.group(1))
            idx += 1

    return stacks


def parse_move(line):
    match = MOVE_RE.match(line)
    if not match:
        return None
    groups = match.groups()
    return Move(int(groups[0]), int(groups[1]), int(groups[2]))


def parse_moves(lines):
    idx = 0
    for line in lines:
        if parse_move(line) is not None:
            break
        idx += 1
    return map(parse_move, lines[idx:])


def perform_move1(move, stacks):
    source = stacks[move.source - 1]
    destination = stacks[move.destination - 1]
    for _ in range(move.amount):
        destination.append(source.pop())


def perform_move2(move, stacks):
    source = stacks[move.source - 1]
    destination = stacks[move.destination - 1]
    destination.extend(source[-move.amount:])
    del source[-move.amount:]


def perform_moves(filename, perform_move):
    lines = list(parse(filename))
    stacks = parse_crates(lines)
    moves = parse_moves(lines)
    for move in moves:
        perform_move(move, stacks)
    return stacks


def solve_part1(filename):
    result = ''.join(
        map(lambda stack: stack[-1], perform_moves(filename, perform_move1)))
    print(result)


def solve_part2(filename):
    result = ''.join(
        map(lambda stack: stack[-1], perform_moves(filename, perform_move2)))
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day05.txt')
    else:
        solve_part1('day05.txt')
