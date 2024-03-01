from __future__ import annotations
import enum
import math
from time import time
class Tag(enum.Enum):
    PRIME = enum.auto()
    TRIANGLE = enum.auto()
    SQR = enum.auto()
    F60 = enum.auto()
    L20 = enum.auto()
    G20 = enum.auto()
    M3 = enum.auto()
    M5 = enum.auto()
    ODD = enum.auto()
    EVEN = enum.auto()
ALL_TRIANGULAR = {1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78}
ALL_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
VALID_NUMBERS: set[int] = {1, 2,3, 4, 5, 6, 7, 9, 10, 11, 12, 15, 16, 18, 20, 21, 23, 24, 25, 30, 35, 36, 45, 55, 60}

PNUMS: set[int] = ALL_PRIMES.intersection(VALID_NUMBERS)
TRIANGULAR_NUMBERS: set[int] = ALL_TRIANGULAR.intersection(VALID_NUMBERS)
SQR_NUMS: set[int] = {i for i in VALID_NUMBERS if i ** 0.5 % 1 == 0}
F60: set[int] = {i for i in VALID_NUMBERS if not 60 % i}
L20: set[int] = {i for i in VALID_NUMBERS if i < 20}
G20: set[int] = {i for i in VALID_NUMBERS if i > 20}
M3: set[int] = {i for i in VALID_NUMBERS if not i % 3}
M5: set[int] = {i for i in VALID_NUMBERS if not i % 5}
ODD: set[int] = {i for i in VALID_NUMBERS if i % 2}
EVEN: set[int] = {i for i in VALID_NUMBERS if not i % 2}

tag_to_set:dict[Tag, set[int]] = {
    Tag.PRIME: PNUMS,
    Tag.TRIANGLE: TRIANGULAR_NUMBERS,
    Tag.SQR: SQR_NUMS,
    Tag.F60: F60,
    Tag.L20: L20,
    Tag.G20: G20,
    Tag.M3: M3,
    Tag.M5: M5,
    Tag.ODD: ODD,
    Tag.EVEN: EVEN
    }
GROUPS: list[tuple[Tag, Tag]] = [(Tag.SQR, Tag.PRIME), (Tag.L20, Tag.G20), (Tag.ODD, Tag.EVEN)]
grouped: set[Tag] = {i for t in GROUPS for i in t}
Solution = list[list[set]]
__valid_square_return_list: Solution = [[set() for i in range(5)] for e in range(5)]
times = 0
def generate_valid_squares(vertical_tags: tuple[Tag], horizontal_tags: tuple[Tag]) -> Solution:
    """Returns a 2d-list. Sublists are rows(access would be list[rowno][columnno])"""
    global times
    times += 1
    for row_no, row_tag in enumerate(vertical_tags): #tags on the vertical span an entire row, row_no is zero-indexed row number
        for column_no, column_tag in enumerate(horizontal_tags):
            __valid_square_return_list[row_no][column_no] = (tag_to_set[row_tag]).intersection(tag_to_set[column_tag])
    return vertical_tags, horizontal_tags, __valid_square_return_list

def generate_all_valid_solutions(): #returns generator of tuple[vt, ht,solutions]
    for group in GROUPS:
        vertical_tags = []
        horizontal_tags = []
        #allocate groups(mirror image is not neccesary because you can't mirror)
        remaining_groups = [i for i in GROUPS if i != group]
        horizontal_tags += group
        for i in remaining_groups:
            vertical_tags += i
        #allocate remaining
        singular = [i for i in tag_to_set.keys() if not i in grouped]
        for tag in singular:
            local_vt = vertical_tags.copy()
            local_ht = horizontal_tags.copy()
            local_singular = singular.copy()
            local_singular.remove(tag)
            local_vt.append(tag)
            yield generate_valid_squares(local_vt, local_ht + local_singular)
# for i in generate_all_valid_solutions():
#     with open("output.txt", "a") as output:
#         print(i[0], file=output)
#         print(i[1], file=output)
#         print(file=output)
#         for k in range(5):
#             print(i[2][k], file=output)
#         print("\n..............\n", file=output)\
def permutate(base: list[int]):
    current_perm = base.copy()
    yield base
    reversed = list(base.__reversed__())
    while True:
        for i in range((length:=len(base))-2, 0 - 1, -1): #-2 to get the second-last slicer thing, 0-1 so i == 0 happens
            if not current_perm[i] < current_perm[i + 1]:
                continue
            smallest_larger_on_right = True
            for k in range(i+1, length):
                if current_perm[k] > current_perm[i] and (smallest_larger_on_right == True or current_perm[k] < current_perm[smallest_larger_on_right]):
                   smallest_larger_on_right = k
            current_perm[i], current_perm[smallest_larger_on_right] = current_perm[smallest_larger_on_right], current_perm[i] #swap
            current_perm[i+1:] = current_perm[i+1:].__reversed__()
            break
        yield current_perm
        if(current_perm == reversed): break

def check_permutation(asolution: Solution, permutation: list[int]) -> bool:
    """assume solution is a 2d array of uniform length"""
    _solution = asolution.copy()
    solution_length = len(_solution)
    def _2d_index_to_1d_index(i1, i2):
        """assume _solution is a 2d array of uniform length"""
        nonlocal solution_length
        return solution_length * i1 + i2

    unfillables: int = 0
    for i in range(len(_solution)):
        for j in range(len(_solution[0])):
            if permutation[_2d_index_to_1d_index(i, j)] in _solution[i][j]:
                solution[i][j] = permutation[_2d_index_to_1d_index(i, j)] 
            else: unfillables += 1
            if unfillables > 2: return False
    return True
    
def solve(asolution: Solution):
    flattened: list[list[int, list]] = [[0, list(i)] for row in asolution for i in row] #where the int is the next offset to be used
    current = 0
    bsolution = []
    used = set()
    while current < len(flattened):
        if len(flattened[current][1]) == 0: print(1); return None
        elif flattened[current][0] == len(flattened[current][1]): #equals, as the left is the index but the right is the length
            #if exceeded the end of the first cell, there is no solution
            if current == 0:
                print(flattened[current])
                return None
            #reset offset
            flattened[current][0] = 0
            used.remove(bsolution.pop())
            current -= 1
            flattened[current][0] += 1
            continue
        else:
            to_be_appended = flattened[current][1][flattened[current][0]]
            if to_be_appended in used: #if its used, try the next value(or backtrack, which is handled in the loop)
                flattened[current][0] += 1
                continue
            bsolution.append(to_be_appended) # append to the solution list the item at the listed index
            used.add(to_be_appended)
            current += 1
    else:
        return [bsolution[i: i + len(asolution)] for i in range(0, len(flattened), len(asolution[0]))]

# for solution in generate_all_valid_solutions():
#     x = solve(solution[2])
#     if x == None:
#         continue
#     with open("testOutput.txt", "a") as output:
#         print(solution[0], file=output)
#         print(solution[1], file=output)
#         print(file=output)
#         for k in range(5):
#             print(solution[2][k], file=output)
#         print(file=output)
#         for solution_row in x:
#             print(solution_row[0], file=output)
#         print("\n..............\n", file=output)

# print(solve(generate_all_valid_solutions().__next__()[2]))
generator = generate_all_valid_solutions()
real_start_time = time()
with open("testOutput.txt", "a") as output:
    for solution in generator:
        start_time = time()
        x = solve(solution[2])
        print(time() - start_time, file=output)
        print(solution[0], file=output)
        print(solution[1], file=output)
        print(file=output)
        for k in range(5):
            print(solution[2][k], file=output)
        print(file=output)
        if x != None:
            for solution_row in x:
                print(solution_row, file=output)
        else:
            print("There was no solution", file=output)
        print("\n..............\n", file=output)

    print(time() - real_start_time, file=output)
