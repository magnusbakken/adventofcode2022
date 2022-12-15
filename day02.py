ROCK = 1
PAPER = 2
SCISSORS = 3

LOSS = 0
DRAW = 3
WIN = 6

OPPONENT_LOOKUP = dict([
    ('A', ROCK),
    ('B', PAPER),
    ('C', SCISSORS),
])

HERO_LOOKUP_1 = dict([
    ('X', ROCK),
    ('Y', PAPER),
    ('Z', SCISSORS),
])

RESULT_MATRIX = dict([
    (ROCK, dict([(ROCK, DRAW), (PAPER, LOSS), (SCISSORS, WIN)])),
    (PAPER, dict([(ROCK, WIN), (PAPER, DRAW), (SCISSORS, LOSS)])),
    (SCISSORS, dict([(ROCK, LOSS), (PAPER, WIN), (SCISSORS, DRAW)])),
])

DOMINATOR_LOOKUP = dict([
    (ROCK, PAPER),
    (PAPER, SCISSORS),
    (SCISSORS, ROCK),
])

DOMINATED_LOOKUP = dict([
    (ROCK, SCISSORS),
    (PAPER, ROCK),
    (SCISSORS, PAPER),
])


def get_hero_shape1(letter):
    return HERO_LOOKUP_1.get(letter)


def get_hero_shape2(letter, opponent_shape):
    if letter == 'X':
        return DOMINATED_LOOKUP.get(opponent_shape)
    elif letter == 'Y':
        return opponent_shape
    else:
        return DOMINATOR_LOOKUP.get(opponent_shape)


def get_result(opponent, hero):
    return RESULT_MATRIX.get(hero).get(opponent)


def calculate_score(opponent, hero):
    result = get_result(opponent, hero)
    return result + hero


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def run_line1(line):
    opponent_letter, hero_letter = line.split(' ')
    opponent = OPPONENT_LOOKUP.get(opponent_letter)
    hero = get_hero_shape1(hero_letter)
    return calculate_score(opponent, hero)


def run_line2(line):
    opponent_letter, hero_letter = line.split(' ')
    opponent = OPPONENT_LOOKUP.get(opponent_letter)
    hero = get_hero_shape2(hero_letter, opponent)
    return calculate_score(opponent, hero)


def solve_part1(filename):
    result = sum(map(run_line1, parse(filename)))
    print(result)


def solve_part2(filename):
    result = sum(map(run_line2, parse(filename)))
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day02.txt')
    else:
        solve_part1('day02.txt')
