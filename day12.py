from queue import Queue
from dataclasses import dataclass
import numpy as np
import string
from typing import List, Optional


@dataclass
class Point:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return f"Row:{self.row} Col:{self.col}"


class Map:
    start: Point
    end: Point
    height_array: np.ndarray

    def get_height(self, point: Point) -> int:
        return int(self.height_array[point.row, point.col])


def parse_input_str(input_str: str) -> Map:
    input_lines = input_str.strip().split("\n")

    num_rows = len(input_lines)
    num_cols = len(input_lines[0])

    height_array = np.zeros((num_rows, num_cols))
    start = Point(-1, -1)
    end = Point(-1, -1)

    for row_num, input_line in enumerate(input_lines):
        for col_num, ch in enumerate(input_line.strip()):
            if ch == "S":
                height_array[row_num, col_num] = string.ascii_lowercase.index("a")
                start = Point(row_num, col_num)
            elif ch == "E":
                height_array[row_num, col_num] = string.ascii_lowercase.index("z")
                end = Point(row_num, col_num)
            else:
                height_array[row_num, col_num] = string.ascii_lowercase.index(ch)

    area_map = Map()
    area_map.start = start
    area_map.end = end
    area_map.height_array = height_array

    return area_map


def bfs_solution(area_map: Map) -> Optional[int]:
    """Find how many steps for the shortest path from area_map.start to area_map.end"""
    num_rows, num_cols = area_map.height_array.shape

    @dataclass
    class QueueItem:
        """Item for our BFS queue"""

        point: Point
        steps_so_far: int

    q = Queue()

    visited = {area_map.start}
    q.put(QueueItem(point=area_map.start, steps_so_far=0))

    while not q.empty():
        q_item = q.get()
        point = q_item.point
        point_height = area_map.get_height(point)
        point_steps_so_far = q_item.steps_so_far

        # At the end?
        if point == area_map.end:
            return point_steps_so_far

        # Find our neighbours
        neigh_pts = list()

        # Neighbour above us
        if point.row > 0:
            neigh_pts.append(Point(point.row - 1, point.col))

        # Neighbour below us
        if point.row < num_rows - 1:
            neigh_pts.append(Point(point.row + 1, point.col))

        # Neighbour to the left
        if point.col > 0:
            neigh_pts.append(Point(point.row, point.col - 1))

        # Neighbour to the right
        if point.col < num_cols - 1:
            neigh_pts.append(Point(point.row, point.col + 1))

        for neigh_pt in neigh_pts:
            neigh_height = area_map.get_height(neigh_pt)

            if (neigh_height <= point_height + 1) and (neigh_pt not in visited):
                visited.add(neigh_pt)
                enqueue_item = QueueItem(neigh_pt, point_steps_so_far + 1)
                q.put(enqueue_item)

    # No solution found!
    return None


def get_zero_elevation_points(area_map: Map) -> List[Point]:
    """Find all points in area_map's height map that are at elevation zero"""
    zero_elevation_points = list()

    for row_num, row in enumerate(area_map.height_array):
        for col_num, height in enumerate(row):
            if height == 0:
                zero_elevation_points.append(Point(row_num, col_num))

    return zero_elevation_points


def find_min_steps_from_any_0_elevation_start(area_map: Map) -> int:
    """For part 2, we have to consider all of the elevation=0 points as a starting
    point, and find the one of these that has the shortest possible path to the end"""
    starting_locations = get_zero_elevation_points(area_map)

    min_of_all_solutions = 9999999

    for starting_location in starting_locations:
        area_map.start = starting_location
        min_num_steps = bfs_solution(area_map)
        if (min_num_steps is not None) and (min_num_steps < min_of_all_solutions):
            min_of_all_solutions = min_num_steps

    return min_of_all_solutions


if __name__ == "__main__":
    input_str = open("input/day12.txt").read()
    area_map = parse_input_str(input_str)

    min_num_steps = bfs_solution(area_map)
    print(f"Part 1: The optimal path requires {min_num_steps} steps")

    # For part 2, we have to try every location of elevation 0 as the start
    # location
    min_num_steps_any_start_position = find_min_steps_from_any_0_elevation_start(
        area_map
    )
    print(
        f"Part 2: The optimal path from the best starting position requires {min_num_steps_any_start_position} steps"
    )
