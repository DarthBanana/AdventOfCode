TEST_INPUT = ".^^.^.^^^^"
REAL_INPUT = ".^^..^...^..^^.^^^.^^^.^^^^^^.^.^^^^.^^.^^^^^^.^...^......^...^^^..^^^.....^^^^^^^^^....^^...^^^^..^"


def is_tile_trap(index, prev_row):
    left_index = index - 1
    center_index = index
    right_index = index + 1
    if left_index < 0:
        left = False
    else:
        left = prev_row[left_index] == "^"
    center = prev_row[center_index] == "^"

    if right_index >= len(prev_row):
        right = False
    else:
        right = prev_row[right_index] == "^"
    if (left and center and not right):
        return True
    if (center and right and not left):
        return True
    if (left and not center and not right):
        return True
    if (not left and not center and right):
        return True
    return False


def get_next_row(prev_row):
    next_row = ""
    safe_tile_count = 0
    for i in range(len(prev_row)):
        if is_tile_trap(i, prev_row):
            next_row += "^"
        else:
            next_row += "."
            safe_tile_count += 1

    return (next_row, safe_tile_count)


def count_safe_tiles(first_row, row_count, return_rows=False):
    if return_rows:
        rows = first_row
        rows += '\n'

    row_0_safe_count = 0
    row = first_row
    for c in first_row:
        if c == '.':
            row_0_safe_count += 1
    safe_count = row_0_safe_count
    for i in range(1, row_count):
        row, safe = get_next_row(row)
        safe_count += safe
        if return_rows:
            rows += row
            rows += "\n"

    if return_rows:
        return safe_count, rows
    return safe_count


def test(input, count, expected):
    result, rows = count_safe_tiles(input, count, True)
    print(rows)
    print(result)
    assert (result == expected)


test(TEST_INPUT, 10, 38)

print("Part 1 result : ", count_safe_tiles(REAL_INPUT, 40))

print("Part 2 result : ", count_safe_tiles(REAL_INPUT, 400000))
