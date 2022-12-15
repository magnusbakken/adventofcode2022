import re


class Grid:
    def __init__(self, pairs):
        self.pairs = pairs
        self.sensors = list(map(lambda x: x[0], pairs))
        self.beacons = list(map(lambda x: x[1], pairs))
        xs = list(map(lambda x: x[0], self.sensors))
        xs.extend(list(map(lambda x: x[0], self.beacons)))
        ys = list(map(lambda x: x[1], self.sensors))
        ys.extend(list(map(lambda x: x[1], self.beacons)))
        self.min_x, self.min_y = -8, -10
        self.max_x, self.max_y = 28, 26
        self.x_range = list(range(self.min_x, self.max_x + 1))
        self.y_range = list(range(self.min_y, self.max_y + 1))
        self.grid = [[0 for _ in self.x_range] for _ in self.y_range]

    def __str__(self):
        rows = []
        for y in self.y_range:
            row = [str(y).ljust(4)]
            for x in self.x_range:
                if (x, y) in self.sensors:
                    row.append('S')
                elif (x, y) in self.beacons:
                    row.append('B')
                elif self.grid[y][x] == 0:
                    row.append('.')
                else:
                    row.append('#')
            rows.append(''.join(row))
        return '\n'.join(rows)

    def scan_all(self):
        for sensor, nearest_beacon in self.pairs:
            max_distance = manhattan(sensor, nearest_beacon)
            self.scan_sensor(sensor, max_distance)

    def scan_sensor(self, sensor, max_distance):
        q = []
        visited = set()
        visited.add(sensor)
        q.insert(0, sensor)
        levels = dict()
        levels[sensor] = 0
        while q:
            item = q.pop()
            for neighbor in self._neighbors(*item):
                if not neighbor in visited:
                    levels[neighbor] = levels[item] + 1
                    if levels[neighbor] <= max_distance:
                        visited.add(neighbor)
                        q.insert(0, neighbor)
                        self.grid[neighbor[1]][neighbor[0]] = 1

    def _neighbors(self, x, y):
        yield (x - 1, y)
        yield (x + 1, y)
        yield (x, y - 1)
        yield (x, y + 1)


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


LINE_RE = re.compile(
    r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)')


def parse_data(lines):
    for line in lines:
        match = LINE_RE.match(line)
        if not match:
            raise Exception('Parsing failed on {}'.format(line))
        sensor = (int(match.group(1)), int(match.group(2)))
        beacon = (int(match.group(3)), int(match.group(4)))
        yield (sensor, beacon)


def manhattan(source, destination):
    return abs(source[0] - destination[0]) + abs(source[1] - destination[1])


def simulate(filename):
    data = list(parse_data(parse(filename)))
    grid = Grid(data)
    print(grid)
    print()
    grid.scan_all()
    print(grid)


def solve_part1(filename):
    result = simulate(filename)
    print(result)


def solve_part2(filename):
    result = simulate(filename)
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day15.txt')
    else:
        solve_part1('day15.txt')
