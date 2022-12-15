class Grid:
    def __init__(self, min_x, max_x, max_y, rocks, include_floor=False):
        self.min_x = min_x - 200
        self.max_x = max_x + 200
        self.min_y = 0
        self.max_y = max_y + 2
        self.rocks = rocks
        self.sand = dict()
        self._valid_x = list(range(self.min_x, self.max_x + 1))
        self._valid_y = list(range(self.min_y, self.max_y + 1))
        if include_floor:
            for x in self._valid_x:
                self.rocks[(x, self.max_y)] = True

    def __str__(self):
        rows = []
        for y in range(self.min_y, self.max_y + 1):
            row = [str(y).ljust(3), ' ']
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.rocks:
                    row.append('#')
                elif (x, y) in self.sand:
                    row.append('o')
                else:
                    row.append('.')
            rows.append(''.join(row))
        return '\n'.join(rows)

    def drop_sand(self):
        prev_loc = (500, 0)
        next_loc = None
        while True:
            if prev_loc is None:
                break

            next_loc = self.fall(prev_loc)
            if prev_loc == next_loc:
                break

            prev_loc = next_loc

        if next_loc is None:
            return False
        else:
            self.sand[next_loc] = True
            return True

    def fall(self, loc):
        down = (loc[0], loc[1] + 1)
        down_left = (loc[0] - 1, loc[1] + 1)
        down_right = (loc[0] + 1, loc[1] + 1)
        if not self.is_valid(down) and not self.is_valid(down_left) and not self.is_valid(down_right):
            return None

        if self.is_blocked(down):
            if self.is_blocked(down_left):
                if self.is_blocked(down_right):
                    return loc
                else:
                    return down_right
            else:
                return down_left
        return down

    def is_valid(self, loc):
        return loc[0] in self._valid_x and loc[1] in self._valid_y

    def is_blocked(self, loc):
        return loc in self.rocks or loc in self.sand


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def parse_rocks(lines, include_floor):
    rocks = dict()
    min_x, max_x = float('inf'), 0
    min_y, max_y = float('inf'), 0
    for line in lines:
        prev_point = None
        points = line.split(' -> ')

        for point in points:
            x, y = list(map(int, point.split(',')))
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

            if prev_point is not None:
                if x == prev_point[0]:
                    if y > prev_point[1]:
                        r = range(prev_point[1], y + 1)
                    else:
                        r = range(y, prev_point[1] + 1)
                    for y_ in r:
                        rocks[(x, y_)] = True
                elif y == prev_point[1]:
                    if x > prev_point[0]:
                        r = range(prev_point[0], x + 1)
                    else:
                        r = range(x, prev_point[0] + 1)
                    for x_ in r:
                        rocks[(x_, y)] = True

            prev_point = (x, y)

    return Grid(min_x, max_x, max_y, rocks, include_floor)


def simulate(filename, include_floor):
    state = parse_rocks(parse(filename), include_floor)
    rounds = 0
    while True:
        if rounds % 100 == 0:
            print(state)
            print()
        if not state.drop_sand() or (include_floor and (500, 0) in state.sand):
            if include_floor and (500, 0) in state.sand:
                print(state)
                print()
            break
        rounds += 1
    return rounds


def solve_part1(filename):
    result = simulate(filename, False)
    print(result)


def solve_part2(filename):
    result = simulate(filename, True) + 1
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day14.txt')
    else:
        solve_part1('day14.txt')
