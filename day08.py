class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

    def __getitem__(self, idx):
        return self.grid[idx]


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def read_grid(lines):
    return Grid([[int(c) for c in line] for line in lines])


def is_on_edge(grid, x, y):
    return x == 0 or y == 0 or x == grid.width - 1 or y == grid.height - 1


def is_visible_from_edge(grid, x, y):
    if is_on_edge(grid, x, y):
        return True

    tree = grid[y][x]

    for idx in reversed(range(0, x)):
        if tree <= grid[y][idx]:
            break
    else:
        return True

    for idx in range(x+1, grid.width):
        if tree <= grid[y][idx]:
            break
    else:
        return True

    for idx in reversed(range(0, y)):
        if tree <= grid[idx][x]:
            break
    else:
        return True

    for idx in range(y+1, grid.height):
        if tree <= grid[idx][x]:
            break
    else:
        return True

    return False


def calculate_scenic_score(grid, x, y):
    if is_on_edge(grid, x, y):
        return 0

    tree = grid[y][x]
    left, right, up, down = 0, 0, 0, 0

    for idx in reversed(range(0, x)):
        left += 1
        if tree <= grid[y][idx]:
            break

    for idx in range(x+1, grid.width):
        right += 1
        if tree <= grid[y][idx]:
            break

    for idx in reversed(range(0, y)):
        up += 1
        if tree <= grid[idx][x]:
            break

    for idx in range(y+1, grid.height):
        down += 1
        if tree <= grid[idx][x]:
            break

    return left * right * up * down


def count_all_visible_trees(grid):
    total = 0
    for x in range(grid.width):
        for y in range(grid.height):
            if is_visible_from_edge(grid, x, y):
                total += 1
    return total


def find_most_scenic_tree(grid):
    most_scenic_score = 0
    for x in range(grid.width):
        for y in range(grid.height):
            scenic_score = calculate_scenic_score(grid, x, y)
            if scenic_score > most_scenic_score:
                most_scenic_score = scenic_score
    return most_scenic_score


def solve_part1(filename):
    result = count_all_visible_trees(read_grid(parse(filename)))
    print(result)


def solve_part2(filename):
    result = find_most_scenic_tree(read_grid(parse(filename)))
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day08.txt')
    else:
        solve_part1('day08.txt')
