CELL_EMPTY = -1
CELL_HEAD = 0
CELL_TAIL = 1

DIRECTION_LEFT = 'L'
DIRECTION_RIGHT = 'R'
DIRECTION_UP = 'U'
DIRECTION_DOWN = 'D'


class State:
    def __init__(self, tail_length, grid_size):
        self.tail_length = tail_length
        self.grid_size = grid_size
        self.grid = [[CELL_EMPTY] * grid_size for _ in range(grid_size)]
        x, y = grid_size // 2, grid_size // 2
        self.grid[y][x] = CELL_HEAD
        self.head = (x, y)
        self.tails = [(x, y)] * tail_length
        self.visited = set()
        self.visited.add(self.tails[-1])

    def __str__(self):
        lines = []
        for y in range(self.grid_size):
            line = []
            for x in range(self.grid_size):
                value = self.grid[y][x]
                if value == CELL_HEAD:
                    line.append('H')
                elif value >= CELL_TAIL and value <= CELL_TAIL + self.tail_length:
                    if self.tail_length == 1:
                        line.append('T')
                    else:
                        line.append(str(value - CELL_TAIL + 1))
                elif (x, y) in self.visited:
                    line.append('#')
                else:
                    line.append('.')
            lines.append(''.join(line))
        return '\n'.join(lines)

    def move(self, direction, amount):
        for _ in range(amount):
            self._move_once(direction)

    def _move_once(self, direction):
        old_head = self.head
        if direction == DIRECTION_LEFT:
            self.head = (self.head[0] - 1, self.head[1])
        elif direction == DIRECTION_RIGHT:
            self.head = (self.head[0] + 1, self.head[1])
        elif direction == DIRECTION_UP:
            self.head = (self.head[0], self.head[1] - 1)
        elif direction == DIRECTION_DOWN:
            self.head = (self.head[0], self.head[1] + 1)
        self._set_state(old_head[0], old_head[1], CELL_EMPTY)
        self._drag_tail()
        self._set_state(self.head[0], self.head[1], CELL_HEAD)

    def _drag_one_tail(self, tail_idx):
        tail = self.tails[tail_idx]
        leader = self.head if tail_idx == 0 else self.tails[tail_idx - 1]
        diff_x = abs(leader[0] - tail[0])
        diff_y = abs(leader[1] - tail[1])
        direction_x = 1 if leader[0] - tail[0] < 0 else -1
        direction_y = 1 if leader[1] - tail[1] < 0 else -1
        new_tail = tail
        if diff_x > 0 and diff_y > 0:
            if diff_x > diff_y:
                new_tail = (leader[0] + direction_x, leader[1])
            elif diff_x < diff_y:
                new_tail = (leader[0], leader[1] + direction_y)
            else:
                new_tail = (leader[0] + direction_x, leader[1] + direction_y)
        elif diff_x > 1:
            new_tail = (leader[0] + direction_x, leader[1])
        elif diff_y > 1:
            new_tail = (leader[0], leader[1] + direction_y)

        if tail != new_tail:
            self._set_state(tail[0], tail[1], CELL_EMPTY)

        current_state = self._get_state(new_tail[0], new_tail[1])
        if current_state == CELL_EMPTY or (current_state > CELL_HEAD and current_state > CELL_TAIL + tail_idx):
            self._set_state(new_tail[0], new_tail[1], CELL_TAIL + tail_idx)

        self.tails[tail_idx] = new_tail
        if tail_idx == self.tail_length - 1:
            self.visited.add(new_tail)

    def _drag_tail(self):
        for tail_idx in range(self.tail_length):
            self._drag_one_tail(tail_idx)

    def _get_state(self, x, y):
        return self.grid[y][x]

    def _set_state(self, x, y, state):
        self.grid[y][x] = state


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def read_move(line):
    direction, amount = line.split()
    return (direction, int(amount))


def solve(filename, tail_length, grid_size):
    state = State(tail_length, grid_size)
    moves = map(read_move, parse(filename))
    for direction, amount in moves:
        state.move(direction, amount)

    result = len(state.visited)
    print(result)


def solve_part1(filename):
    solve(filename, tail_length=1, grid_size=1000)


def solve_part2(filename):
    solve(filename, tail_length=9, grid_size=1000)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day09.txt')
    else:
        solve_part1('day09.txt')
