from collections import namedtuple
import operator
import re

BinOp = namedtuple('BinOp', ['left', 'operator', 'right'])


def get_divisors(n):
    divisors = []
    for i in range(2, n // 2):
        if n % i == 0:
            divisors.append(i)
    divisors.append(n)
    return divisors


class Monkey:
    def __init__(self, idx, starting_items, op, test, if_true, if_false):
        self.idx = idx
        self.items = starting_items
        self.op = op
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspections = 0

    def set_mod_factor(self, mod_factor):
        self.mod_factor = mod_factor

    def test_item(self, item):
        self.inspections += 1
        return item % self.test == 0

    def receive_item(self, item):
        if self.mod_factor is not None:
            self.items.append(item % self.mod_factor)
        else:
            self.items.append(item)

    def throw_item(self):
        del self.items[0]


MONKEY_RE = re.compile(r'Monkey (\d+)')
STARTING_ITEMS_RE = re.compile(r'\s+Starting items: ([\d,\s]+)')
OPERATION_RE = re.compile(r'\s+Operation: new = (old|\d+) (\*|\+) (old|\d+)')
TEST_RE = re.compile(r'\s+Test: divisible by (\d+)')
IF_TRUE_RE = re.compile(r'\s+If true: throw to monkey (\d+)')
IF_FALSE_RE = re.compile(r'\s+If false: throw to monkey (\d+)')


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def parse_monkey(lines):
    monkey_match = MONKEY_RE.match(lines[0])
    starting_items_match = STARTING_ITEMS_RE.match(lines[1])
    operation_match = OPERATION_RE.match(lines[2])
    test_match = TEST_RE.match(lines[3])
    if_true_match = IF_TRUE_RE.match(lines[4])
    if_false_match = IF_FALSE_RE.match(lines[5])
    return Monkey(
        idx=int(monkey_match.group(1)),
        starting_items=list(
            map(int, starting_items_match.group(1).split(', '))),
        op=BinOp(operation_match.group(1), operation_match.group(
            2), operation_match.group(3)),
        test=int(test_match.group(1)),
        if_true=int(if_true_match.group(1)),
        if_false=int(if_false_match.group(1))
    )


def parse_monkeys(lines, discard):
    idx = 0
    monkeys = []
    while idx * 7 < len(lines):
        monkeys.append(parse_monkey(lines[idx*7:]))
        idx += 1
    if discard:
        mod_factor = 1
        for monkey in monkeys:
            mod_factor *= monkey.test
        for monkey in monkeys:
            monkey.set_mod_factor(mod_factor)
    return monkeys


def describe_binop(binop, result):
    right = 'itself' if binop.right == 'old' else str(binop.right)
    if binop.operator == '+':
        return '    Worry level increases by {} to {}.'.format(right, result)
    else:
        return '    Worry level is multiplied by {} to {}.'.format(right, result)


def run_binop(binop, old):
    left = old if binop.left == 'old' else int(binop.left)
    right = old if binop.right == 'old' else int(binop.right)
    op = operator.add if binop.operator == '+' else operator.mul
    return op(left, right)


def printif(debug, s):
    if debug:
        print(s)


def run_round(monkeys, divide_worry_level, debug=False):
    for monkey in monkeys:
        printif(debug, 'Monkey {}:'.format(monkey.idx))
        for item in [item for item in monkey.items]:
            printif(
                debug, '  Monkey inspects an item with a worry level of {}.'.format(item))
            worry_level = item
            worry_level = run_binop(monkey.op, worry_level)
            printif(debug, describe_binop(monkey.op, worry_level))

            if divide_worry_level:
                worry_level = worry_level // 3
                printif(debug, '    Monkey gets bored with item. Worry level is divided by 3 to {}.'.format(
                    worry_level))
            else:
                printif(debug, '    Monkey gets bored with item.')

            if monkey.test_item(worry_level):
                printif(
                    debug, '    Current worry level is divisible by {}.'.format(monkey.test))
                dest_idx = monkey.if_true
            else:
                printif(debug, '    Current worry level is not divisible by {}.'.format(
                    monkey.test))
                dest_idx = monkey.if_false
            printif(debug, '    Item with worry level {} is thrown to monkey {}.'.format(
                worry_level, dest_idx))
            monkey.throw_item()
            monkeys[dest_idx].receive_item(worry_level)


def write_state(monkeys, round):
    print('After round {}, the monkeys are holding items with these worry levels:'.format(round))
    for monkey in monkeys:
        print('Monkey {}: {}'.format(monkey.idx,
              ', '.join(map(str, monkey.items))))
    print()


def run_rounds(monkeys, divide_worry_level, round_count, debug=False):
    for round in range(1, round_count + 1):
        run_round(monkeys, divide_worry_level, debug)
        if debug:
            write_state(monkeys, round)
        if round == 1 or round == 20 or round % 1000 == 0:
            print('== After round {} =='.format(round))
            for monkey in monkeys:
                print('Monkey {} inspected items {} times.'.format(
                    monkey.idx, monkey.inspections))
            print()


def solve(filename, divide_worry_level, round_count):
    monkeys = parse_monkeys(list(parse(filename)), not divide_worry_level)
    run_rounds(monkeys, divide_worry_level, round_count)
    sorted_monkeys = list(
        sorted(monkeys, key=lambda monkey: monkey.inspections, reverse=True))
    top_two = sorted_monkeys[:2]
    return top_two[0].inspections * top_two[1].inspections


def solve_part1(filename):
    monkey_business = solve(filename, divide_worry_level=True, round_count=20)
    print(monkey_business)


def solve_part2(filename):
    monkey_business = solve(
        filename, divide_worry_level=False, round_count=10000)
    print(monkey_business)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day11.txt')
    else:
        solve_part1('day11.txt')
