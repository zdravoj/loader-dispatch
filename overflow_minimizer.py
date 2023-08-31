from itertools import permutations, combinations_with_replacement, chain


# creates an array of sub-arrays 
    # with sub-array values starting at 0 and incrementing by 1
    # in which the lengths of the sub-arrays containing the values
    # are defined by the value in the input array
    # ex. [1, 3, 1] returns [[0], [1, 2, 3], [4]]
def get_assignments(input_array:list) -> list:
    # sub-list values
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


# returns loader assignment which minimizes overflow
def minimize_overflow(loader_dict: dict, door_array: list):

    # efficiency table for loader PPH
    efficiency = {
        1 : 1.0,
        2 : 0.85,
        3 : 0.8,
        4 : 0.77
    }

    # calculate overflow for one loader (in assignment)
    def calc_ind_overflow(loader_name:str, assignment:list):
        # calculate loader pph
        pph = loader_dict[loader_name] * efficiency[len(assignment)]
        # sum doors fph
        fph = sum([door_array[door] for door in assignment])
        # subtract doors fph from loader pph
        return pph - fph

    # calculate area overflow (all loaders in all assignments)
    def calc_area_overflow(loader_names:list, assignments:list):
        area_overflow = 0.0
        loader_overflow = []
        for i in range(len(loader_names)):
            # calculate loader overflow for assignment
            load_overflow = calc_ind_overflow(loader_names[i], assignments[i])
            # add individual loader overflow to loader overflow list
            loader_overflow.append(load_overflow)
            # add individual overflow to area overflow if negative
            area_overflow += load_overflow if load_overflow < 0.0 else 0.0
        # overall overflow
        return area_overflow, loader_overflow

    # for permutations
    n_loaders = len(loader_dict)
    n_doors = len(door_array)
    # get sizes of sub-arrays for get_assignments
    perm_array = chain.from_iterable(
        [set(permutations(combination))
            for combination in 
                [
                    comb for comb
                    in combinations_with_replacement(range(1, 5), n_loaders)
                    if sum(comb) == n_doors
                ]
        ]
    )
    # all permutations of area assignments
    door_permutations = [
        get_assignments(door_groups)
        for door_groups in perm_array
    ]
    # all permutations of loaders
    loader_permutations = list(
        permutations(loader_dict.keys(), len(loader_dict))
    )

    # initialize overflow (for maximizing)
    min_overflow = -10000.0
    # initialize dispatch and individual loader overflow
    loader_dispatch = dict()
    ind_loader_overflow = list()

    # iterate through all possible combinations of loaders and door assignments
    for door_perm in door_permutations:
        for loader_perm in loader_permutations:
            # calculate area overflow for loader/assignment combination
            area_overflow, loader_overflow = calc_area_overflow(loader_perm, door_perm)
            # assign loader dispatch and minimized overflow
            if area_overflow > min_overflow:
                loader_dispatch = {
                    loader_perm[i] : door_perm[i]
                    for i in range(len(loader_perm))
                }
                min_overflow = area_overflow
                ind_loader_overflow = loader_overflow

    return loader_dispatch, ind_loader_overflow, min_overflow
