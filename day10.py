from dataclasses import dataclass
from enum import auto, Enum
import numpy as np
from typing import Dict, List


class Opcode(Enum):
    ADDX = auto()
    NOOP = auto()


@dataclass
class Instruction:
    opcode: Opcode
    operand: int


class CPU:
    def __init__(self, instructions: List[Instruction]):
        self.reg_x = 1
        self.tick_rem = 0
        self.pc = 0
        self.instructions = instructions

        self.instr = self.instructions[0]

        if self.instr.opcode == Opcode.NOOP:
            self.instr_tick_left = 0
        else:
            self.instr_tick_left = 1

    def tick(self) -> bool:
        """Tick the CPU once. Returns False is there are no more instructions to run"""
        if self.instr_tick_left == 0:
            self.pc += 1

            if self.instr.opcode == Opcode.ADDX:
                self.reg_x += self.instr.operand

            self.instr = self.instructions[self.pc]

            if self.instr.opcode == Opcode.ADDX:
                self.instr_tick_left = 1
            else:
                self.instr_tick_left = 0
        else:
            self.instr_tick_left -= 1

        if self.pc >= len(self.instructions) - 1:
            # No more instructions to run!
            return False
        else:
            return True

    def get_reg_x(self):
        return self.reg_x

    def __str__(self):
        return f"X: {self.reg_x} instr: {self.instr} instr_tick_left: {self.instr_tick_left}"


class CRT:
    def __init__(self, cpu: CPU):
        self.cpu = cpu
        self.pixel_x = 0
        self.pixel_y = 0

        self.ROWS = 6
        self.COLS = 40

        self.display = np.zeros([self.ROWS, self.COLS])

    def tick(self) -> None:
        """Tick the CRT once, drawing on the display buffer in memory"""

        reg_x = cpu.get_reg_x()
        sprite_set = set(range(reg_x - 1, reg_x + 2))

        if self.pixel_x in sprite_set:
            self.display[self.pixel_y, self.pixel_x] = 1
        else:
            self.display[self.pixel_y, self.pixel_x] = 0

        self.pixel_x = (self.pixel_x + 1) % 40
        if self.pixel_x == 0:
            self.pixel_y += 1

    def draw(self):
        """Print the display to the console so that we can see the picture"""
        for row in self.display:
            row_chars = list()
            for pix_val in row:
                if pix_val == 1:
                    row_chars.append("#")
                else:
                    row_chars.append(".")
            print("".join(row_chars))


def parse_instruction(input_line: str) -> Instruction:
    parts = input_line.split(" ")

    if parts[0] == "addx":
        opcode = Opcode.ADDX
    elif parts[0] == "noop":
        opcode = Opcode.NOOP
    else:
        print("Invalid opcode: {parts[0]}")
        exit(-1)

    if opcode == Opcode.ADDX:
        operand = int(parts[1])
    else:
        operand = None

    return Instruction(opcode=opcode, operand=operand)


def parse_instructions(input_str: str) -> List[Instruction]:
    input_lines = input_str.strip().split("\n")
    instructions = [parse_instruction(input_line) for input_line in input_lines]

    return instructions


def calc_sig_strength_sum(reg_x_history: Dict[int, int]) -> int:
    sig_strength_measurement_ticks = [20, 60, 100, 140, 180, 220]
    sig_strength_sum = sum(
        [tick * reg_x_history[tick] for tick in sig_strength_measurement_ticks]
    )

    return sig_strength_sum


if __name__ == "__main__":
    input_str = open("input/day10.txt").read()
    instructions = parse_instructions(input_str)

    cpu = CPU(instructions)
    crt = CRT(cpu)

    reg_x_history = dict()

    for i in range(240):
        crt.tick()
        running = cpu.tick()
        tick_num = i + 2
        reg_x_history[tick_num] = cpu.get_reg_x()
        print(f"After tick {tick_num}: {cpu}")
        if running is False:
            print(f"Program completed at tick {i}")
            break

    sig_strength_sum = calc_sig_strength_sum(reg_x_history)
    print(f"Part 1: Signal Strength Sum: {sig_strength_sum}")

    print("Part 2. CRT display:")
    crt.draw()
