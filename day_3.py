"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""
import re
from string import punctuation

special = frozenset(punctuation.replace('.', ''))

with open('input/day_3.txt', 'r') as f:
    data = f.read().splitlines()

test_data = \
    """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

# data = test_data.splitlines()


class Capture:
    def __init__(self, line_num, char_num):
        self.line_num = line_num
        self.char_num = char_num
        self.line = data[line_num]
        self.start_idx = char_num - 1
        self.end_idx = char_num + 2
        self.part_numbers = {}

    @property
    def has_digits(self):
        return any([c for c in self.capture_window if c.isdigit()])

    @property
    def capture_window(self):
        return self.line[self.start_idx: self.end_idx]

    def find_start(self):
        while list(self.capture_window)[0].isdigit() and self.start_idx > 0:
            self.start_idx -= 1

    def find_end(self):
        while list(self.capture_window)[-1].isdigit() and self.end_idx < 140:
            self.end_idx += 1

    def part_loc_str(self, char):
        return '{}-{}'.format(self.line_num, char)

    def get_part_numbers(self):
        self.find_start()
        self.find_end()
        numbers = re.findall(r'\d+', self.capture_window)
        if self.start_idx == 0:
            char_num = 0 if self.capture_window[0].isdigit() else 1
        else:
            char_num = self.start_idx + 1
        for number in numbers:
            self.part_numbers[self.part_loc_str(char_num)] = int(number)
            char_num += len(number) + 1
        return self.part_numbers


part_numbers = {}
for idx, line in enumerate(data):
    if bool(set(line) & special):
        for jdx, c in enumerate(line):
            if c in special:
                for line_offset in range(0, 3):
                    capture = Capture(line_num=idx - 1 + line_offset, char_num=jdx)
                    if capture.has_digits:
                        part_numbers.update(capture.get_part_numbers())
print(sum(part_numbers.values()))


"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""
import math

all_gear_ratios = {}
total_sum = 0
for idx, line in enumerate(data):
    if '*' in line:
        for jdx, c in enumerate(line):
            if c == "*":
                gear_ratios = {}
                for line_offset in range(0, 3):
                    capture = Capture(line_num=idx - 1 + line_offset, char_num=jdx)
                    if capture.has_digits:
                        gear_ratios.update(capture.get_part_numbers())
                if len(gear_ratios) == 2:
                    all_gear_ratios.update(gear_ratios)
                    total_sum += math.prod(gear_ratios.values())
print(total_sum)
