# Panagiotis Tsiavos  A.M. 2396

import csv
import heapq
import math
import time
import sys
from collections import namedtuple

Bound = namedtuple('Bound', 'low high')
RangeQuery = namedtuple('RangeQuery', 'x_low x_high y_low y_high')

x_bound = None
y_bound = None
x_step = y_step = None
bins = 50

db = list()
inv_file = dict()
grid = [[[] for _ in range(bins)] for _ in range(bins)]


# Add database item index to inv_file based on tags:
def add_index(index, tags):
    for tag in tags:
        if tag not in inv_file:
            inv_file[tag] = [index]
            heapq.heapify(inv_file[tag])
        else:
            heapq.heappush(inv_file[tag], index)


# Merge Join alg.
def merge(arr, l, m, r):
    # create temp generators
    L = (i for i in arr[l])
    R = (i for i in arr[r])

    left = next(L, None)
    right = next(R, None)
    res = []
    while left is not None and right is not None:
        if left == right:
            res.append(left)
            left = next(L, None)
            right = next(R, None)
        elif left < right:
            left = next(L, None)
        else:
            right = next(R, None)

    arr[l] = res
    arr[r] = res


# Merge Join Divide-and-Conquer style
def mergeJoin(arr, l, r):
    if l < r:
        m = (l + (r - 1)) // 2

        # Divide into first and second halves
        mergeJoin(arr, l, m)
        mergeJoin(arr, m + 1, r)
        merge(arr, l, m, r)


def check_bounds(pos):
    return pos - 1 if pos == bins else pos


# Checks if a database location tag is inside a given range query
def is_inside(loc, query):
    return query.x_low < loc[0] < query.x_high and query.y_low < loc[1] < query.y_high


# Fill grid based on database items location
def fill_grid():
    for item in db:
        loc = tuple(float(i) for i in item[1].split(','))
        x_pos = check_bounds(int((loc[0] - x_bound.low) // x_step))
        y_pos = check_bounds(int((loc[1] - y_bound.low) // y_step))

        grid[x_pos][y_pos].append(db.index(item))


def kwSpaSearchIF(query_range, keywords):
    result = []
    start = time.perf_counter()
    heaps = [inv_file.get(i) for i in keywords]
    mergeJoin(heaps, 0, len(heaps) - 1)

    for index in heaps[0]:
        item = db[index]
        loc = tuple(float(i) for i in item[1].split(','))
        if is_inside(loc, query_range):
            result.append(item)
    end = time.perf_counter()

    print('kwSpaSearchIF: {} results, cost = {:.10f} seconds'.format(len(result), end - start))
    for item in result:
        print(item)


def kwSpaSearchGrid(query_range, keywords):
    result = []
    start = time.perf_counter()

    # Find the range of grid cell indexes
    x_pos_low = int((query_range.x_low - x_bound.low) // x_step)
    x_pos_high = check_bounds(int((query_range.x_high - x_bound.low) // x_step))

    y_pos_low = int((query_range.y_low - y_bound.low) // y_step)
    y_pos_high = check_bounds(int((query_range.y_high - y_bound.low) // y_step))

    # Iterate through those cells and check if these location are inside the given range query
    for i in range(x_pos_low, x_pos_high + 1):
        for j in range(y_pos_low, y_pos_high + 1):
            # Grid cell is not empty
            if grid[i][j]:
                for index in grid[i][j]:
                    item = db[index]
                    current_tags = item[2].split(',')
                    loc = tuple(float(i) for i in item[1].split(','))
                    if is_inside(loc, query_range) and all(tag in current_tags for tag in keywords):
                        result.append(item)

    end = time.perf_counter()

    print("kwSpaSearchGrid: {} results, cost = {:.10f} seconds".format(len(result), end - start))
    for item in result:
        print(item)


def kwSpaSearchRaw(query_range, keywords):
    results = []
    start = time.perf_counter()
    for item in db:
        current_tags = item[2].split(',')
        loc = tuple(float(i) for i in item[1].split(','))
        if is_inside(loc, query_range) and all(item in current_tags for item in keywords):
            results.append(item)
    end = time.perf_counter()

    print("kwSpaSearchRAW: {} results, cost = {:.10f} seconds".format(len(results), end - start))
    for item in results:
        print(item)


# Create queries based on user arguments
def get_args():
    try:
        query_range = RangeQuery(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
        keywords = []
        for arg in sys.argv[5:]:
            if arg.endswith("'"):
                keywords[-1] = keywords[-1].lstrip("'") + ' ' + arg.rstrip("'")
            else:
                keywords.append(arg)
    except:
        print("False arguments given")
        print("Error:", sys.exc_info()[0])
        raise

    return query_range, keywords


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
            # Add to database
            db.append(row)
            # Add to inverted File
            add_index(line, row[2].split(','))

            # Update bounds of grid
            locations = tuple(float(i) for i in row[1].split(','))
            x_low_bound = min(x_low_bound, locations[0])
            x_high_bound = max(x_high_bound, locations[0])

            y_low_bound = min(y_low_bound, locations[1])
            y_high_bound = max(y_high_bound, locations[1])

    # Create 'final' bound of grid
    x_bound = Bound(x_low_bound, x_high_bound)
    y_bound = Bound(y_low_bound, y_high_bound)

    # Calculate step of grid cells
    x_step = (x_bound.high - x_bound.low) / bins
    y_step = (y_bound.high - y_bound.low) / bins

    # After we read our file and instantiated axis bounds, steps we can fill the grid
    fill_grid()

    # Get arguments
    query_range, keywords = get_args()

    kwSpaSearchRaw(query_range, keywords)
    print()
    kwSpaSearchIF(query_range, keywords)
    print()
    kwSpaSearchGrid(query_range, keywords)


if __name__ == '__main__':
    main()
