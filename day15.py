from dataclasses import dataclass
import re
from typing import List, Tuple


@dataclass
class Point:
    x: int
    y: int


class Sensor:
    def __init__(self, point, dist_to_beacon: int) -> None:
        self.point = point
        self.dist_to_beacon = dist_to_beacon

    def __repr__(self):
        return f"point: {self.point} dist_to_beacon: {self.dist_to_beacon}"


class Beacon:
    def __init__(self, point) -> None:
        self.point = point


def manhattan_distance(p1: Point, p2: Point) -> int:
    return int(abs(p2.x - p1.x) + abs(p2.y - p1.y))


def parse_sensor_and_beacon(in_str: str) -> Tuple[Sensor, Beacon]:
    m = re.findall(r"-?\d+", in_str)

    sensor_x = int(m[0])
    sensor_y = int(m[1])

    beacon_x = int(m[2])
    beacon_y = int(m[3])

    sensor_point = Point(sensor_x, sensor_y)
    beacon_point = Point(beacon_x, beacon_y)

    distance = manhattan_distance(sensor_point, beacon_point)

    return Sensor(sensor_point, distance), Beacon(beacon_point)


def parse_input(in_str: str) -> Tuple[List[Sensor], List[Beacon]]:
    strs = in_str.split("\n")
    sensors, beacons = zip(
        *[parse_sensor_and_beacon(sensor_beacon_str) for sensor_beacon_str in strs]
    )

    return sensors, beacons


def find_one_sensor_coverage_on_line(
    sensor: Sensor, row_of_interest: int, min_coord: int, max_coord: int
) -> Tuple[int, int]:
    """At some row of interest in space, a sensor will have a certain
    coverage. Find this left and right extreme of coverage. Part 1 needs this
    value."""
    sensor_range = sensor.dist_to_beacon
    distance_to_row = abs(sensor.point.y - row_of_interest)

    if distance_to_row > sensor_range:
        return None
    else:
        left_intercept = sensor.point.x - (sensor_range - distance_to_row)
        right_intercept = sensor.point.x + (sensor_range - distance_to_row)

        if left_intercept < min_coord:
            left_intercept = 0

        if right_intercept > max_coord:
            right_intercept = max_coord

        return_interval = (left_intercept, right_intercept)

        return return_interval


def combine_intervals(intervals: List[Tuple]) -> List[Tuple]:
    """Combines tuples representing sensor coverage intervals, since many of them will overlap"""
    combined_intervals = []
    for begin, end in sorted(intervals):
        if combined_intervals and combined_intervals[-1][1] >= begin - 1:
            combined_intervals[-1][1] = max(combined_intervals[-1][1], end)
        else:
            combined_intervals.append([begin, end])

    return combined_intervals


def find_all_sensor_coverage_on_line(
    sensors: List[Sensor], row_of_interest: int, min_coord: int, max_coord: int
) -> List[Tuple]:
    """Finds all intervals of sensor coverage on this row"""
    covered_intervals = []

    for sensor in sensors:
        covered_interval = find_one_sensor_coverage_on_line(
            sensor, row_of_interest, min_coord, max_coord
        )
        if covered_interval is not None:
            covered_intervals.append(covered_interval)

    # Combine the intervals
    combined_intervals = combine_intervals(covered_intervals)

    return combined_intervals


def find_distress_beacon(sensors: List[Sensor], min_coord, max_coord) -> Point:
    for y in range(max_coord + 1):
        covered_intervals = find_all_sensor_coverage_on_line(
            sensors, y, min_coord, max_coord
        )

        if len(covered_intervals) != 1:
            x = covered_intervals[0][1] + 1  # The point after the first covered interval is the unconvered position
            return Point(x, y)

    print("No solution found to distress beacon position")
    exit()


if __name__ == "__main__":
    in_str = open("input/day15.txt").read().strip()
    sensors, beacons = parse_input(in_str)

    row_of_interest = 2000000
    # #row_of_interest = 10
    min_coord = -99999999999999
    max_coord = 999999999999999
    coverage_intervals = find_all_sensor_coverage_on_line(
        sensors, row_of_interest, min_coord, max_coord
    )

    # Count up how many positions are covered in the intervals
    covered_positions = 0
    for interval in coverage_intervals:
        covered_positions += interval[1] - interval[0]

    print(
        f"Part 1: {covered_positions} positions on row {row_of_interest} cannot contain a beacon"
    )

    min_coord = 0
    max_coord = 4000000
    distress_beacon_pt = find_distress_beacon(sensors, min_coord, max_coord)
    tuning_frequency = (4000000 * distress_beacon_pt.x) + distress_beacon_pt.y
    print(f"Part 2: The distress beacon tuning frequency is: {tuning_frequency}")

