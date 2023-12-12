"""
--- Day 11: Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

    Between galaxy 1 and galaxy 7: 15
    Between galaxy 3 and galaxy 6: 17
    Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""
from itertools import combinations
import numpy as np


def construct_array(lines, expansion_size=1):
    array = None
    for line in lines:
        if not type(array) is np.ndarray:
            array = np.array([list(line)])
        else:
            array = np.append(array, [list(line)], axis=0)
        if '#' not in set(line):
            array = np.append(array, [np.repeat(expansion_size, len(list(line))).tolist()], axis=0)
    return array


with open('input/day_11.txt', 'r') as f:
    lines = f.read().splitlines()

array = construct_array(lines)
array_t = construct_array(array.T.tolist())
array = array_t.T


def distance(a, b):
    dx = abs(b[1] - a[1])
    dy = abs(b[0] - a[0])
    return dx + dy


test_pair = ((6, 1), (11, 5))
assert distance(*test_pair) == 9


def find_nodes(array):
    nodes = {}
    galaxy_id = 1
    for idx, row in enumerate(array):
        for jdx, point in enumerate(list(row)):
            if point == "#":
                expansions_row = [int(p) for p in array[idx][:jdx] if p.isdigit()]
                expansions_col = [int(p) for p in array.T[jdx][:idx] if p.isdigit()]
                nodes[galaxy_id] = (idx + sum(expansions_col) - len(expansions_col),
                                    jdx + sum(expansions_row) - len(expansions_row))
                galaxy_id += 1
    return nodes


nodes = find_nodes(array)
distance_sum = 0
for pair in combinations(nodes.values(), 2):
    distance_sum += distance(*pair)
print(distance_sum)


"""
--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""

test_data = \
    """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

# lines = test_data.splitlines()

array = construct_array(lines, expansion_size=1000000 - 1)
array_t = construct_array(array.T.tolist(), expansion_size=1000000 - 1)
array = array_t.T

nodes = find_nodes(array)
distance_sum = 0
for pair in combinations(nodes.values(), 2):
    distance_sum += distance(*pair)
print(distance_sum)
