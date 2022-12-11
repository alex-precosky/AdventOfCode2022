from io import StringIO
from typing import List

# Today is an exercise in building a tree then traversing it to add up file
# sizes in a directory tree


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str, parent_dir):
        self.name = name
        self.parent_dir = parent_dir
        self.directories = dict()
        self.files = dict()


class DirectoryFactory:
    def build_directory_from_str(self, in_str: str):
        self.root_dir = Directory(name="/", parent_dir=None)

        self.cur_dir = self.root_dir

        f = StringIO(in_str)
        lines = f.readlines()
        [self.parse_terminal_input(line.strip()) for line in lines]

        return self.root_dir

    def parse_terminal_input(self, line: str):
        if line[0] == "$":
            self.parse_command(line)
        elif line[0] == "d":  # dir
            pass
        elif line[0].isnumeric():
            self.parse_file(line)
        else:
            print(f"Unknown what this is: {line}")

    def parse_command(self, line: str):
        tok = line.split(" ")
        if tok[1] == "cd":
            if tok[2] == "/":
                self.cur_dir = self.root_dir
            elif tok[2] == "..":
                self.cur_dir = self.cur_dir.parent_dir
            else:
                # check if it exists under self.cur_dir. If not, create it
                target_dir = tok[2]
                if target_dir not in self.cur_dir.directories:
                    self.cur_dir.directories[target_dir] = Directory(
                        name=target_dir, parent_dir=self.cur_dir
                    )

                self.cur_dir = self.cur_dir.directories[target_dir]
        elif tok[1] == "ls":
            pass
        else:
            print(f"Unknown command token: {tok}")
            exit()

    def parse_file(self, line: str):
        tok = line.split(" ")
        size = int(tok[0])
        name = tok[1]
        self.cur_dir.files[name] = File(name, size)


def populate_dir_total_size_list(dir: Directory, size_list: List[int]) -> int:
    """Traverse directory structure and populate a list of total sizes
    Returns: The total size of dir"""
    total_size = 0

    for file in dir.files.values():
        total_size += file.size

    for sub_dir in dir.directories.values():
        total_size += populate_dir_total_size_list(sub_dir, size_list)

    size_list.append(total_size)

    return total_size


def find_sum_total_size_dirs_at_most_size_n(root_dir: Directory, n: int) -> int:
    """Returns how many directories in the directory tree provided have a
    Total size of at most n"""
    total_size_list = list()
    populate_dir_total_size_list(root_dir, total_size_list)

    acc = 0
    for total_size in total_size_list:
        if total_size <= n:
            acc += total_size

    return acc


def find_total_size_of_directory_to_delete(
    root_dir: Directory, disk_size: int, required_space: int
) -> int:
    total_size_list = list()
    populate_dir_total_size_list(root_dir, total_size_list)

    space_used = max(total_size_list)
    free_space = disk_size - space_used

    space_to_free = required_space - free_space

    # Find the smallest directory that will free up enough space if we were to
    # delete it
    min_candidate = 99999999999
    for total_size in total_size_list:
        if (total_size >= space_to_free) and (total_size < min_candidate):
            min_candidate = total_size

    return min_candidate


if __name__ == "__main__":
    in_str = open("input/day07.txt").read()
    df = DirectoryFactory()
    root_dir = df.build_directory_from_str(in_str)

    part1 = find_sum_total_size_dirs_at_most_size_n(root_dir, 100000)
    print(f"Part 1: The sum of the applicable total sizes is: {part1}")

    disk_size = 70000000
    required_space = 30000000
    part2 = find_total_size_of_directory_to_delete(root_dir, disk_size, required_space)
    print(f"Part 2: The size of the directory we should delete is: {part2}")
