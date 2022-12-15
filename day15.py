import re


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


def generate_manhattan(x, y, distance, check_row):
    s = set()
    for row in range(y - distance, y + distance + 1):
        if row == check_row:
            length = distance - abs(row - y)
            if length == 0:
                s.add((x, row))
            else:
                for column in range(x - length, x + length + 1):
                    s.add((column, row))
    return s


def simulate(filename, check_row):
    data = list(parse_data(parse(filename)))
    all_sensors = set(map(lambda d: d[0], data))
    all_beacons = set(map(lambda d: d[1], data))
    s = set()

    for sensor, beacon in data:
        print('checking sensor {}'.format(sensor))
        distance = manhattan(sensor, beacon)
        sensor_cells = set()
        for cell in generate_manhattan(sensor[0], sensor[1], distance, check_row):
            if not cell in all_sensors and not cell in all_beacons:
                sensor_cells.add(cell)
                s.add(cell)
        print('checked sensor {}'.format(sensor))
        if len(sensor_cells) > 0:
            print('sensor blocks {} locations from {} to {}'.format(
                len(sensor_cells), min(sensor_cells), max(sensor_cells)))
        else:
            print('sensor blocks no locations')

    return len(s)


def solve_part1(filename):
    result = simulate(filename, 2000000)
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
