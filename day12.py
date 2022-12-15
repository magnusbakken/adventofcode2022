def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def find_target(lines, target):
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == target:
                return (x, y)
    raise Exception('{} not found'.format(target))


def find_start(lines):
    return find_target(lines, 'S')


def find_end(lines):
    return find_target(lines, 'E')


def find_neighbors(x, y, width, height):
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    if x < width - 1:
        yield (x + 1, y)
    if y < height - 1:
        yield (x, y + 1)


def is_eligible(source, destination, lines):
    source_letter = lines[source[1]][source[0]]
    destination_letter = lines[destination[1]][destination[0]]
    source_letter = 'a' if source_letter == 'S' else source_letter
    destination_letter = 'a' if destination_letter == 'S' else destination_letter
    if destination_letter == 'E':
        return source_letter == 'z'
    else:
        return ord(source_letter) >= ord(destination_letter) - 1


def find_eligible_neighbors(source, lines):
    for neighbor in find_neighbors(source[0], source[1], len(lines[0]), len(lines)):
        if is_eligible(source, neighbor, lines):
            yield neighbor


def search(start, end, lines):
    q = []
    visited = set()
    visited.add(start)
    q.insert(0, start)
    levels = dict()
    levels[start] = 0
    while q:
        item = q.pop()
        for neighbor in find_eligible_neighbors(item, lines):
            if not neighbor in visited:
                levels[neighbor] = levels[item] + 1
                visited.add(neighbor)
                q.insert(0, neighbor)

    return levels[end] if end in levels else float('inf')


def find_starting_positions(lines):
    for x in range(len(lines[0])):
        for y in range(len(lines)):
            if lines[y][x] == 'a':
                yield (x, y)


def find_best_hike(lines, end):
    best = float('inf')
    for start in find_starting_positions(lines):
        result = search(start, end, lines)
        if result < best:
            best = result
    return best


def solve_part1(filename):
    lines = list(parse(filename))
    start, end = find_start(lines), find_end(lines)
    result = search(start, end, lines)
    print(result)


def solve_part2(filename):
    lines = list(parse(filename))
    end = find_end(lines)
    result = find_best_hike(lines, end)
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day12.txt')
    else:
        solve_part1('day12.txt')
