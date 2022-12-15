from collections import namedtuple


class State:
    def __init__(self):
        self.root = Dir('/', None)
        self.cwd = self.root

    def __repr__(self):
        return 'State({}, {})'.format(self.root, self.cwd)

    def navigate_root(self):
        self.cwd = self.root

    def navigate_up(self):
        if self.cwd.parent is None:
            raise Exception('Cannot navigate up from root')

        self.cwd = self.cwd.parent

    def navigate(self, dirname):
        child = [d for d in self.cwd.dirs if d.name == dirname]
        if len(child) == 0:
            raise Exception(
                'Cannot navigate to non-existent child dir {} in {}'.format(dirname, self.cwd))

        self.cwd = child[0]

    def add_file(self, file):
        self.cwd.files.append(file)

    def add_dir(self, dir_):
        self.cwd.dirs.append(dir_)


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.dirs = []
        self.files = []

    def __repr__(self):
        return 'Dir({}, {}, {})'.format(self.name, self.dirs, self.files)

    def enumerate_all(self):
        yield self
        for child in self.dirs:
            yield from child.enumerate_all()

    def calculate_size(self):
        total = sum(file.size for file in self.files)
        for childdir in self.dirs:
            total += childdir.calculate_size()
        return total

    def full_path(self):
        path = [self.name]
        parent = self.parent
        while parent is not None:
            path.append(parent.name)
            parent = parent.parent

        return '/'.join(path)


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return 'File({}, {})'.format(self.name, self.size)


def parse(filename):
    with open(filename, 'r') as f:
        return map(lambda s: s.rstrip(), f.readlines())


def handle_line(line, state):
    tokens = line.split(' ')
    if tokens[0] == '$':
        if tokens[1] == 'cd':
            if tokens[2] == '/':
                state.navigate_root()
            elif tokens[2] == '..':
                state.navigate_up()
            else:
                state.navigate(tokens[2])
    elif tokens[0] == 'dir':
        dir_ = Dir(tokens[1], state.cwd)
        state.add_dir(dir_)
    else:
        file = File(tokens[1], int(tokens[0]))
        state.add_file(file)


def find_small_dirs_size(state):
    total = 0
    for d in state.root.enumerate_all():
        size = d.calculate_size()
        if size < 100000:
            total += size
    return total


def find_largest_problematic_dir(state):
    dirs = []
    for d in state.root.enumerate_all():
        size = d.calculate_size()
        dirs.append((d, size))
    dirs = sorted(dirs, key=lambda x: x[1])
    used_space = next(filter(lambda d: d[0].name == '/', dirs))[1]
    total_space = 70000000
    needed_space = 30000000
    space_to_free_up = needed_space - (total_space - used_space)
    dir_ = next(filter(lambda d: d[1] >= space_to_free_up, dirs))
    return dir_[1]


def get_state(filename):
    state = State()
    for line in parse(filename):
        handle_line(line, state)

    return state


def solve_part1(filename):
    result = find_small_dirs_size(get_state(filename))
    print(result)


def solve_part2(filename):
    result = find_largest_problematic_dir(get_state(filename))
    print(result)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        solve_part2('day07.txt')
    else:
        solve_part1('day07.txt')
