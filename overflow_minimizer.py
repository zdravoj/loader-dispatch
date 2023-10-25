from itertools import permutations, combinations_with_replacement, chain

def get_assignments(input_array:list) -> list:
    values = list(range(sum(input_array)))
    return_array = []
    subarray_start_value = 0

    for subarray_length in input_array:
        return_array.append(
            values[
                subarray_start_value:subarray_start_value+subarray_length
            ]
        )
        subarray_start_value += subarray_length
    return return_array

def calc_assign(door_split, loader_dict, doors):
    EFFICIENCY = [1.0, 0.85, 0.8, 0.78]
    loader_table = [
        [k]+[round(v*x, 2) for x in EFFICIENCY] for k,v in loader_dict.items()
    ]
    loader_table_sorted = loader_table.copy()
    loader_table_sorted.sort(key= lambda x: x[1], reverse= True)
    assignment_structure = get_assignments(door_split)
    doors_assigned = [[doors[i]for i in assignment] for assignment in assignment_structure]
    assignment_sums = [sum(l) for l in doors_assigned]
    assignment_structure_tups = [tuple(assignment) for assignment in assignment_structure]
    assignment_groups = list(zip(assignment_sums, assignment_structure_tups))
    assignment_groups_sorted = assignment_groups.copy()
    assignment_groups_sorted.sort(key=lambda x: x[0], reverse=True)
    dispatch = {k: v for k, v in zip(
        [list(i) for i in zip(*loader_table_sorted)][0],
        [list(i) for i in zip(*assignment_groups_sorted)][1]
    )
    }
    n_td_pph = [(i[0], x, i[x]) for i, x in zip(loader_table_sorted, [len(t[1]) for t in assignment_groups_sorted])]
    new_ind_of = [x - y for x, y in zip([x[2] for x in n_td_pph], [y[0] for y in assignment_groups_sorted])]
    new_ind_of = [-x if x < 0.0 else 0.0 for x in new_ind_of]
    tot_of = sum(new_ind_of)
    return dispatch, new_ind_of, tot_of


def minimize_overflow(loader_dict, doors):
    perm_array = chain.from_iterable(
        [set(permutations(combination))
            for combination in 
                [
                    comb for comb
                    in combinations_with_replacement(range(1, 5), len(loader_dict))
                    if sum(comb) == len(doors)
                ]
        ]
    )
    dispatch, individual_overflow, total_overflow = dict(), list(), 10000.0
    for door_assign in perm_array:
        d, nio, to = calc_assign(door_assign, loader_dict, doors)
        if to < total_overflow:
            dispatch, individual_overflow, total_overflow = d, nio, to
    return dispatch, individual_overflow, total_overflow


if __name__ == "__main__":
    import time
    start = time.time()
    loader_dispatch, ind_loader_overflow, min_overflow = minimize_overflow(
        loader_dict = {
            "A": 810,
            "B": 660,
            "C": 595,
            "D": 580,
            "E": 550,
            "F": 475,
            "G": 430,
            "H": 420,
            "I": 300
        },
        doors = [
            690,
            420,
            380,
            160,
            590,
            445,
            630,
            290,
            790,
            120,
            110,
            80
        ]
    )
    end = time.time()
    delta = end - start
    print(loader_dispatch)
    print(ind_loader_overflow)
    print(min_overflow)
    print(delta)