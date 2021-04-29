# Panagiotis Tsiavos  A.M. 2396

import csv
import heapq
import time
import sys

db = list()
inv_file = dict()


def add_index(index, tags):
    for tag in tags:
        if tag not in inv_file:
            inv_file[tag] = [index]
            heapq.heapify(inv_file[tag])
        else:
            heapq.heappush(inv_file[tag], index)


# FIRST attempt of merge join ~ 10 times slower
# def merge_join_slow(heaps):
#     offsets = [0 for _ in heaps]
#
#     result = []
#     while all(off < len(ind) for off, ind in zip(offsets, heaps)):
#         elem = set(ind[off] for off, ind in zip(offsets, heaps))
#         if len(elem) == 1:
#             result.append(elem.pop())
#             offsets = [x + 1 for x in offsets]
#         else:
#             n = [h[o] for o, h in zip(offsets, heaps)]
#             m = n.index(min(n))
#             offsets[m] += 1
#
#     return result

# def kwSearchIF_slow(keywords):
#     start = time.perf_counter()
#
#     joins = merge_join([inv_file.get(i) for i in keywords])
#     end = time.perf_counter()
#
#     if joins is None:
#         print('kwSearchIF: Nothing found...')
#         print('Keywords: {}'.format(keywords))
#     else:
#         print('kwSearchIF: {} results, cost = {} sec.'.format(len(joins), end - start))
#         for index in joins:
#             print(db[index])

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


def kwSearchIF(keywords):
    start = time.perf_counter()
    heaps = [inv_file.get(i) for i in keywords]
    if None in heaps:
        print("No term with name {}".format(keywords[heaps.index(None)]))
        heaps = list(filter(None, heaps))

    mergeJoin(heaps, 0, len(heaps) - 1)
    end = time.perf_counter()

    print('kwSearchIF: {} results, cost = {} sec.'.format(len(heaps[0]), end - start))
    for index in heaps[0]:
        print(db[index])


# Searches Keywords (tags) in database
def kwSearchRAW(keywords):
    results = []
    start = time.perf_counter()
    for item in db:
        current_tags = item[2].split(',')
        if all(item in current_tags for item in keywords):
            results.append(item)
    end = time.perf_counter()

    print("kwSearchRAW: {} results, cost = {} sec.".format(len(results), end - start))
    for item in results:
        print(item)


def main():
    with open("Restaurants_London_England.tsv") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter='\t')
        for line, row in enumerate(read_tsv):
            row[1] = row[1].replace("location: ", "")
            row[2] = row[2].replace("tags: ", "")
            # Add to database
            db.append(row)
            # Add to inverted File
            add_index(line, row[2].split(','))

    sorted_inv_file = [len(v) for _, v in sorted(inv_file.items(), key=lambda item: len(item[1]))]
    print("#Keywords = {}".format(len(sorted_inv_file)))
    print("Frequencies: {}\n".format(sorted_inv_file))

    # Uncomment lines below to print tag names and its frequency
    # for k in sorted(inv_file, key=lambda el: len(inv_file[el])):
    #     print("Tag: {:22s} frequency: {:4d}".format(k, len(inv_file[k])))
    # print("\n#Keywords = {}".format(len(inv_file)))

    keywords = []
    for arg in sys.argv[1:]:
        if arg.endswith("'"):
            keywords[-1] = keywords[-1].lstrip("'") + ' ' + arg.rstrip("'")
        else:
            keywords.append(arg)

    kwSearchIF(keywords)
    print('\n')
    kwSearchRAW(keywords)


if __name__ == '__main__':
    main()
