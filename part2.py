# Panagiotis Tsiavos  A.M. 2396
import csv
import math
import time
from collections import namedtuple
import sys
Bound = namedtuple('Bound', 'low high')
RangeQuery = namedtuple('RangeQuery', 'x_low x_high y_low y_high')

x_bound = None
y_bound = None
x_step = y_step = None

bins = 50
db = list()
grid = [[[] for _ in range(bins)] for _ in range(bins)]


def print_grid():
    for i in range(bins):
        for j in range(bins):
            if grid[i][j]:
                print("{} {} {}".format(i, j, len(grid[i][j])))
    print()


def check_bounds(pos):
    return pos - 1 if pos == bins else pos


# Checks if a database location tag is inside a given range query
def is_inside(loc, query):
    return query.x_low < loc[0] < query.x_high and query.y_low < loc[1] < query.y_high


# Fills database items into the grid based on their location
def fill_grid():
    for item in db:
        loc = tuple(float(i) for i in item[1].split(','))
        x_pos = check_bounds(int((loc[0] - x_bound.low) // x_step))
        y_pos = check_bounds(int((loc[1] - y_bound.low) // y_step))

        grid[x_pos][y_pos].append(db.index(item))


def spaSearchGrid(query):
    result = []
    start = time.perf_counter()

    # Find the range of grid cell indexes
    x_pos_low = int((query.x_low - x_bound.low) // x_step)
    x_pos_high = check_bounds(int((query.x_high - x_bound.low) // x_step))

    y_pos_low = int((query.y_low - y_bound.low) // y_step)
    y_pos_high = check_bounds(int((query.y_high - y_bound.low) // y_step))

    # Iterate through those cells and check if these location are inside the given range query
    for i in range(x_pos_low, x_pos_high + 1):
        for j in range(y_pos_low, y_pos_high + 1):
            # Grid cell is not empty
            if grid[i][j]:
                for index in grid[i][j]:
                    item = db[index]
                    loc = tuple(float(i) for i in item[1].split(','))
                    if is_inside(loc, query):
                        result.append(item)

    end = time.perf_counter()

    print("spaSearchGrid: {} results, cost = {:.10f} seconds".format(len(result), end - start))
    for item in result:
        print(item)


def spaSearchRaw(query):
    result = []
    start = time.perf_counter()
    # Iterate through the whole database and check for valid locations
    for item in db:
        loc = tuple(float(i) for i in item[1].split(','))
        if is_inside(loc, query):
            result.append(item)
    end = time.perf_counter()

    print("spaSearchRaw: {} results, cost = {:.10f} seconds".format(len(result), end - start))
    for res in result:
        print(res)


def main():
    global x_step, y_step, x_bound, y_bound

    # Bounds of data location tag
    x_low_bound = y_low_bound = math.inf
    x_high_bound = y_high_bound = -math.inf

    with open("Restaurants_London_England.tsv") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter='\t')
        for line, row in enumerate(read_tsv):
            row[1] = row[1].replace("location: ", "")
            row[2] = row[2].replace("tags: ", "")
            db.append(row)
            locations = tuple(float(i) for i in row[1].split(','))
            x_low_bound = min(x_low_bound, locations[0])
            x_high_bound = max(x_high_bound, locations[0])

            y_low_bound = min(y_low_bound, locations[1])
            y_high_bound = max(y_high_bound, locations[1])

    x_bound = Bound(x_low_bound, x_high_bound)
    y_bound = Bound(y_low_bound, y_high_bound)

    print("X-Bound: ", x_bound)
    print("Y-Bound: ", y_bound)
    print("Widths: {} {}".format(x_bound.high - x_bound.low, y_bound.high - y_bound.low))

    x_step = (x_bound.high - x_bound.low) / bins
    y_step = (y_bound.high - y_bound.low) / bins
    print("Steps: ", x_step, y_step)

    # After we read our file and instantiated axis bounds, steps we can fill the grid
    fill_grid()

    # Print non-empty cells
    print_grid()

    query = RangeQuery(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))

    spaSearchGrid(query)
    print('\n')
    spaSearchRaw(query)


if __name__ == '__main__':
    main()
