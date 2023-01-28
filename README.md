# Loader Dispatch

## About
Loader Dispatch was designed for use in the outbounds area of a package distribution hub. 
Packages are unloaded from trailers in the inbound, sorted in the hub, and distributed 
to the outbounds to be loaded into outbound trailers. 
Packages are distributed on conveyor belts which divert packages to outbound trailers via chutes. 
Loaders remove the packages from the chutes and load them into trailers.

Each loader is unique in the number of packages they can consistently load per hour (packages-per-hour, or PPH)
and every trailer (door) is unique in the number of packages distibuted to it (flow-per-hour, or FPH) on any given day.
Should a door's FPH exceed a loader's PPH, packages will accumulate in that door's chute, and cause a chute backup.
A backed-up chute cannot have any more packages delivered to it until packages are removed from the chute.
Packages that cannot be delivered to a chute due to a backup must recirculate on the belt until space is available in
the chute. Every instance of a recirculated package is considered an off-the-end (OTE).

Loader Dispatch creates an optimal assignment of loaders to doors by minimizing OTEs.

## Inputs and Outputs
Loader Dispatch takes:
1. Loader names and PPH for each loader
2. A set of adjacent doors and FPH for each door

and returns a list of loaders and their optimized assignment, including:
1. OTEs expected per hour for each loader's assignment
2. Total OTEs expected per hour for the set of doors

## Assumptions
Loader Dispatch makes the following assumptions:
1. All loaders must be given an assignment.
2. No more than 1 loader can be assigned to each door.
3. Per assumptions 1 and 2, the number of loaders must always be less than or equal to the number of doors.
4. All doors must have a loader assigned.
5. A loader may be assigned a maximum of 4 doors, where the loader's PPH efficiency is affected
according to the following table:

| Doors | Efficiency |
| ----- | ---------- |
| 1     | x100%      |
| 2     | x85%       |
| 3     | x80%       |
| 4     | x78%       |

6. Per assumption 5, the total number of doors cannot exceed the number of loaders times 4.
7. For any loaders assigned to more than 1 door, all doors within the assignment must be adjacent
(ex. A loader cannot be assigned to doors 2 and 4 without also being assigned to door 3).

## Limitations
Loader Dispatch is primitive in its current state, and unable to account for many variables, including:
- The possibility of assigning more than one loader to a door
- The possibility of assigning loaders to non-adjacent doors
- Excluding doors from assignment (such as doors with 0 FPH)
- Changes to FPH throughout the day
- Changes in loader PPH throughout the day
- Loaders needing breaks

As of now, Loader Dispatch should not be used as anything more than a recommendation.

## Potential Improvements
### Immediate Improvements
Possible immediate improvements include:
- The possibility of assigning more than one loader to a door
- The possibility of assigning loaders to non-adjacent doors
- Excluding doors from assignment

### Future Improvements
Loader Dispatch has the capacity to be extremely useful, and could be used in real-time throughout a sort,
but would need access to more data, such as:
- Real-time package flow data (to adjust assignments throughout the day based on flow changes, trailer replacements, etc.)
- Historical loader PPH data (account for decreases in loader PPH throughout the day, or week)
- Historical flow data (to make intra-day flow predictions)
- Real-time input of loader temperament (unhappy loaders generally have decreased PPH)

### Penalizing Excess Reassignment
Given this data, Loader Dispatch would likely "play musical doors" with loaders, losing efficiency by constantly making reassignments.
A penalty to reassignment would prevent loaders from being moved around too much. This would need to be decided and adjusted
based on the data available.

### Potential for Inbound Use
With some adjustments, Loader Dispatch could also be used in the inbound to maximize efficiency of unloading trailers.
