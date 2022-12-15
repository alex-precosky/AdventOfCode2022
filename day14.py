# https://adventofcode.com/2022/day/14
from dataclasses import dataclass
from enum import auto, Enum, IntEnum
import numpy as np
from typing import List


# This is an exercise in simulating the piling up of falling grains of sand


@dataclass
class Point:
    row: int
    col: int

    @classmethod
    def from_str(cls, in_str: str) -> "Point":
        """Parses a pair like 123,345"""
        coordinate_strs = in_str.split(",")
        col = int(coordinate_strs[0])
        row = int(coordinate_strs[1])

        return Point(row=row, col=col)


class Orientation(Enum):
    """Rock structures that block sand grains are either a horizontal or veritcal line"""

    HORIZONTAL = auto()
    VERTICAL = auto()


class LineSegment:
    """Represents a rock structure that can block sand grains"""

    def __init__(self, start_pt: Point, length: int, orientation: Orientation) -> None:
        self.start_pt = start_pt

        # negative if length extends in the negative row or column direction
        self.length = length

        self.orientation = orientation

    def max_col(self) -> int:
        """Whats the biggest column this line segment occupies"""
        max_col = -1

        if self.orientation == Orientation.HORIZONTAL:
            max_col = self.start_pt.col
        else:
            max_col = self.start_pt.col + self.length

        return max_col

    def max_row(self) -> int:
        """Whats the biggest row this line segment occupies"""
        max_row = -1

        if self.orientation == Orientation.VERTICAL:
            max_row = self.start_pt.row + self.length - 1
        else:
            max_row = self.start_pt.row

        return max_row

    def __repr__(self) -> str:
        return f"start_pt: {self.start_pt} length: {self.length} orientation: {self.orientation}\n"


def line_segments_from_str(in_str: str) -> List[LineSegment]:
    """The top level parsing function. Take one line of problem input, which
    will contain a series of points. Returns some LineSegment instances that
    joins those points"""
    point_strs = in_str.split("->")
    points = [Point.from_str(point_str) for point_str in point_strs]

    # Start with a single pixel point line segment based on the first point
    line_segments = [
        LineSegment(start_pt=points[0], length=1, orientation=Orientation.HORIZONTAL)
    ]

    # Then add the rest of the points
    for point in points[1:]:
        if point.row == line_segments[-1].start_pt.row:
            orientation = Orientation.HORIZONTAL
            length = point.col - line_segments[-1].start_pt.col
        else:
            orientation = Orientation.VERTICAL
            length = point.row - line_segments[-1].start_pt.row

        if length > 0:
            length += 1
        elif length < 0:
            length -= 1

        line_segments[-1].orientation = orientation
        line_segments[-1].length = length

        line_segments.append(
            LineSegment(start_pt=point, length=1, orientation=Orientation.HORIZONTAL)
        )

    return line_segments


class Tile(IntEnum):
    AIR = 0
    ROCK = 1
    SAND = 2


class CaveMap:
    def __init__(self, line_segments: List[LineSegment]) -> None:

        # rows extend positive downwards
        # columns extend positive rightwards
        self.grid = np.zeros((0, 0))

        # How big of a grid to allocate?
        max_row, max_col = max_row_and_col(line_segments)

        # +1 to give space for the infinite floor (Part 1) or the abyss (Part 2)
        self.abyss_row = max_row
        max_row += 1

        # + some space to let sand pile up to the right, which was found to be necessary
        max_col += 1000

        self.grid = np.zeros((max_row, max_col))
        
        # Using the line segments, populate the grid with rocks
        for line_segment in line_segments:
            if line_segment.length >= 0:
                step = 1
            else:
                step = -1

            if line_segment.orientation == Orientation.HORIZONTAL:
                row = line_segment.start_pt.row

                for col in range(
                    line_segment.start_pt.col,
                    line_segment.start_pt.col + line_segment.length,
                    step,
                ):
                    self.set_tile(Point(row, col), Tile.ROCK)

            else:
                col = line_segment.start_pt.col

                for row in range(
                    line_segment.start_pt.row,
                    line_segment.start_pt.row + line_segment.length,
                    step,
                ):

                    self.set_tile(Point(row, col), Tile.ROCK)

    def get_tile(self, point: Point):
        return self.grid[point.row, point.col]

    def set_tile(self, point: Point, value: Tile):
        self.grid[point.row, point.col] = value

    def visualize(self):
        """Useful for visualizing the example data as it plots just in the area interesting to that data"""
        for row in range(10):
            row_str = []
            for col in range(490, 510):
                tile = self.get_tile(Point(row, col))
                if tile == Tile.AIR:
                    ch = "."
                elif tile == Tile.ROCK:
                    ch = "#"
                elif tile == Tile.SAND:
                    ch = "o"
                else:
                    print(f"Invalid tile: {tile}")
                    exit()

                row_str.append(ch)
            print("".join(row_str))


def max_row_and_col(line_segments: List[LineSegment]):
    max_row = 0
    max_col = 0

    for line_segment in line_segments:
        row = line_segment.max_row()
        col = line_segment.max_col()

        if row > max_row:
            max_row = row

        if col > max_col:
            max_col = col

    return max_row, max_col


def parse_line_segments_from_input(input_str: str) -> List[LineSegment]:
    line_segments = list()

    input_lines = input_str.split("\n")

    for input_line in input_lines:
        line_segments.extend(line_segments_from_str(input_line))

    return line_segments


def simulate_one_sand_grain(cave_map: CaveMap):
    """Returns True if simulation is not done"""
    spawn_pt = Point(0, 500)

    abyss_row = cave_map.abyss_row

    sand_pt = spawn_pt
    while (sand_pt.row < abyss_row) and (
        cave_map.get_tile(spawn_pt) != Tile.SAND
    ):
        under_tile = cave_map.get_tile(Point(sand_pt.row + 1, sand_pt.col))
        under_left_tile = cave_map.get_tile(Point(sand_pt.row + 1, sand_pt.col - 1))
        under_right_tile = cave_map.get_tile(Point(sand_pt.row + 1, sand_pt.col + 1))

        if under_tile == Tile.AIR:
            sand_pt.row += 1
        else:
            if under_left_tile == Tile.AIR:
                sand_pt.row += 1
                sand_pt.col -= 1
            elif under_right_tile == Tile.AIR:
                sand_pt.row += 1
                sand_pt.col += 1
            else:
                # No diagonal place to go. Just pile upwards
                break
    else:
        return False

    cave_map.set_tile(sand_pt, Tile.SAND)
    return True


if __name__ == "__main__":
    input_str = open("input/day14.txt").read().strip()

    line_segments = parse_line_segments_from_input(input_str)
    cave_map = CaveMap(line_segments)

    steps = 0
    while simulate_one_sand_grain(cave_map):
        steps += 1
    print(f"Part 1: Steps until sand falls into infinity: {steps}")


    # Add a big floor to the line segments to simulate the infinite floor for Part 2
    max_row, max_col = max_row_and_col(line_segments)
    floor_row = max_row + 2
    big_floor = LineSegment(
        Point(row=floor_row, col=0), length=900, orientation=Orientation.HORIZONTAL
    )
    line_segments.append(big_floor)

    # Regenerate the map for part 2 now that the infinite floor is added. Removes the sand as well.
    cave_map = CaveMap(line_segments)

    steps = 0
    while simulate_one_sand_grain(cave_map):
        steps += 1
    print(f"Part 2: Steps until the sand source clogs: {steps}")
