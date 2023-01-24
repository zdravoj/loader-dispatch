from itertools import permutations, combinations_with_replacement, chain


# creates an array of sub-arrays with sub-array values starting at 0
    # in which the sizes of the sub-arrays containing the values
    # are defined by the value in the array
    # ex. [1, 3, 1] returns [[0], [1, 2, 3], [4]]
def slicer(array):
    n = list(range(sum(array)))
    r = []
    j = 0
    for i in array:
        r.append(n[j:j+i])
        j += i
    return r


# returns loader assignment which minimizes OTEs
def minimize_ote(loader_dict, door_array):
    # calculate OTEs for one loader (in assignment)
    def calc_ote(loader, assignment):
        # calculate loader pph
        pph = loader_dict[loader] * efficiency[len(assignment)]
        # sum doors fph
        fph = sum([door_array[i] for i in assignment])
        # subtract doors fph from loader pph
        sub = pph - fph

        return sub

    # calculate OTEs for PD (all loaders in all assignments)
    def calc_pd_ote(loader_perm, door_perm):
        pd_otes = 0.0
        loader_otes = []
        for i in range(len(loader_perm)):
            # get loader name
            loader = loader_perm[i]
            # calculate loader OTE for assignment
            load_ote = calc_ote(loader, door_perm[i])
            # add individual loader OTE to loader OTE list
            loader_otes.append(load_ote)
            # add individual OTE to PD OTE if negative
            pd_otes += load_ote if load_ote < 0.0 else 0.0
        # overall OTEs
        return pd_otes, loader_otes

    # efficiency table for doors
    efficiency = {
        1 : 1.0,
        2 : 0.85,
        3 : 0.8,
        4 : 0.77
    }

    # for permutations
    k = len(loader_dict)
    n = len(door_array)
    # get sizes of sub-arrays for door permutations
    perm_array = list(chain(
        *[list(
            set(permutations(comb))) 
            for comb in 
                [
                    c for c
                    in combinations_with_replacement(range(1, 5), k)
                    if sum(c) == n
                ]
        ]
    ))
    # all permutations of PD assignments
    door_permutations = [slicer(door_list) for door_list in perm_array]
    # all permutations of loaders
    loader_permutations = list(
        permutations(loader_dict.keys(), len(loader_dict))
    )

    # initialize OTE (for maximizing)
    min_ote = -10000.0

    # initialize dispatch and individual loader OTEs
    loader_dispatch = dict()
    ind_loader_otes = list()

    # iterate through all possible combinations of loaders and door assignments
    for door_p in door_permutations:
        for loader_p in loader_permutations:
            # calculate PD OTE for loader/assignment combination
            pd_ote, loader_otes = calc_pd_ote(loader_p, door_p)
            # assign loader dispatch and minimized OTE
            if pd_ote > min_ote:
                loader_dispatch = {loader_p[i] : door_p[i] for i in range(len(loader_p))}
                min_ote = pd_ote
                ind_loader_otes = loader_otes

    return loader_dispatch, ind_loader_otes, min_ote
