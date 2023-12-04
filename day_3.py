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

with open('input/day_3', 'r') as f:
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
