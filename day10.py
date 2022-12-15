class State:
    def __init__(self, check_cycles):
        self.x = 1
        self.commands = []
        self.current_cycle = 1
        self.check_cycles = check_cycles
        self.results = []
        self.rows = []
        self.last_sprite_position = ''
        self._write_sprite_position()
        print()

    def execute(self, cycles, n):
        first_cycle = True
        last_cycle = False
        original_cycle = self.current_cycle
        for cycle in range(self.current_cycle, self.current_cycle + cycles):
            if first_cycle:
                if n == 0:
                    print('Start cycle {}: begin executing noop'.format(
                        str(self.current_cycle).rjust(3)))
                else:
                    print('Start cycle {}: begin executing addx {}'.format(
                        str(self.current_cycle).rjust(3), n))

            print('During cycle {}: CRT draws pixel in position {}'.format(
                str(self.current_cycle).rjust(2), (self.current_cycle - 1) % 40))

            if cycle in self.check_cycles:
                self.results.append(self.x * self.current_cycle)
            if self.current_cycle % 40 == 1:
                self.rows.append([])
            if abs((self.current_cycle % 40) - self.x - 1) <= 1:
                self.rows[-1].append('#')
            else:
                self.rows[-1].append('.')
            last_cycle = cycle == original_cycle + cycles - 1
            if not last_cycle:
                print('Current CRT row: {}'.format(''.join(self.rows[-1])))
                self._write_sprite_position()
                print()
            self.current_cycle += 1
            first_cycle = False
        self.x += n
        if n == 0:
            print('End of cycle {}: finish executing noop'.format(
                str(self.current_cycle - 1).rjust(2)))
        else:
            print('End of cycle {}: finish executing addx {} (Register X is now {})'.format(
                str(self.current_cycle - 1).rjust(2), n, self.x))
        print('Current CRT row: {}'.format(''.join(self.rows[-1])))
        self._write_sprite_position()
        print()

    def _write_sprite_position(self):
        sprite_position = ['.'] * 40
        sprite_position[self.x-1:self.x+2] = '###'
        s = ''.join(sprite_position)
        if s != self.last_sprite_position:
            print('Sprite position: {}'.format(s))
            self.last_sprite_position = s


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def read_command(line):
    if line == 'noop':
        return (1, 0)
    instr, n = line.split(' ')
    if instr == 'addx':
        return (2, int(n))
    else:
        raise Exception('Unknown instruction {}'.format(instr))


def read_commands(lines):
    return [read_command(line) for line in lines]


def solve_part1(filename):
    check_cycles = [20, 60, 100, 140, 180, 220]
    state = State(check_cycles)
    commands = read_commands(parse(filename))
    for command in commands:
        state.execute(*command)
    print(sum(state.results))


def solve_part2(filename):
    check_cycles = [20, 60, 100, 140, 180, 220]
    state = State(check_cycles)
    commands = read_commands(parse(filename))
    for command in commands:
        state.execute(*command)
    print('\n'.join(''.join(row) for row in state.rows))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day10.txt')
    else:
        solve_part1('day10.txt')
