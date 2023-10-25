from itertools import permutations, combinations_with_replacement, chain

class OverflowMinimizer:
    # efficiency table for loader PPH
    efficiency = {
        1 : 1.0,
        2 : 0.85,
        3 : 0.8,
        4 : 0.77
    }
    def __init__(self, loader_dict:dict, door_array:list):
        self.loader_dict = loader_dict
        self.door_array = door_array

    def __get_subarrays__(self):
        n_loaders = len(self.loader_dict)
        n_doors = len(self.door_array)
        # get sizes of sub-arrays for get_assignments
        return chain.from_iterable(
            [set(permutations(combination))
                for combination in 
                    [
                        comb for comb
                        in combinations_with_replacement(range(1, 5), n_loaders)
                        if sum(comb) == n_doors
                    ]
            ]
        )

    def __get_assignments__(self, input_array:list) -> list:
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
    
    # calculate overflow for one loader (in assignment)
    def __calc_ind_overflow__(self, loader_name:str, assignment:list):
        # calculate loader pph
        pph = self.loader_dict[loader_name] * self.efficiency[len(assignment)]
        # sum doors fph
        fph = sum([self.door_array[door] for door in assignment])
        # subtract doors fph from loader pph
        return pph - fph

    # calculate area overflow (all loaders in all assignments)
    def __calc_area_overflow__(self, loader_names:list, assignments:list):
        area_overflow = 0.0
        loader_overflow = []
        for i in range(len(loader_names)):
            # calculate loader overflow for assignment
            load_overflow = self.__calc_ind_overflow__(loader_names[i], assignments[i])
            # add individual loader overflow to loader overflow list
            loader_overflow.append(load_overflow)
            # add individual overflow to area overflow if negative
            area_overflow += load_overflow if load_overflow < 0.0 else 0.0
        # overall overflow
        return area_overflow, loader_overflow
    
    # returns loader assignment which minimizes overflow
    def minimize_overflow(self):
        # all permutations of area assignments
        door_permutations = [
            self.__get_assignments__(door_groups)
            for door_groups in self.__get_subarrays__()
        ]
        # all permutations of loaders
        loader_permutations = list(
            permutations(self.loader_dict.keys(), len(self.loader_dict))
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
                area_overflow, loader_overflow = self.__calc_area_overflow__(loader_perm, door_perm)
                # assign loader dispatch and minimized overflow
                if area_overflow > min_overflow:
                    loader_dispatch = {
                        loader_perm[i] : door_perm[i]
                        for i in range(len(loader_perm))
                    }
                    min_overflow = area_overflow
                    ind_loader_overflow = loader_overflow

        return loader_dispatch, ind_loader_overflow, min_overflow


if __name__ == "__main__":
    import time
    start = time.time()
    minimizer = OverflowMinimizer(
        loader_dict= {
            "Shar": 595,
            "Joe": 475,
            "Tom": 660,
            "Corwin": 420,
            "Dean": 550,
            "Mike": 580,
            "Jane": 430
        },
        door_array= [
            690,
            420,
            380,
            160,
            590,
            445,
            630,
            290,
            110,
            80
        ]
    )
    mid = time.time()
    loader_dispatch, ind_loader_overflow, min_overflow = minimizer.minimize_overflow()
    end = time.time()
    delta_init = mid - start
    delta_run = end - mid
    print(loader_dispatch)
    print(ind_loader_overflow)
    print(min_overflow)
    print("Initialize:", delta_init)
    print("Calculate:", delta_run)