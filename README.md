# Loader Dispatch

Loader Dispatch is currently deployed in a basic web application. Contact me for the URL and login if you want to try it out!

## About
Loader Dispatch was designed for use in the outbounds area of a package distribution hub. Packages are unloaded from trailers in the inbound, sorted in the hub, and distributed to the outbounds to be loaded into outbound trailers.

Each loader has a minimum consistent number of packages they can load per hour (packages-per-hour, or PPH) and every trailer (door) has a maximum number of packages distributed to it in an hour (flow-per-hour, or FPH). Should a door's FPH exceed a loader's PPH, packages will accumulate in that door's chute and cause packages to build up (overflow).

Loader Dispatch creates an optimal assignment of loaders to doors by minimizing overflow.

## Inputs and Outputs
Loader Dispatch takes:
1. Loader names and PPH for each loader
2. A set of adjacent doors (area) and FPH for each door

and returns an optimized assignment, including:
1. total expected overflow per hour for each loader's assignment
2. Total expected overflow per hour for the area

## Assumptions
Loader Dispatch makes the following assumptions:
1. All loaders must be given an assignment.
2. No more than one loader can be assigned to each door.
3. All doors must have a loader assigned.
4. Per assumptions 1 through 3, the number of loaders must always be less than or equal to the number of doors.
5. A loader may be assigned a maximum of four doors, where the loader's PPH efficiency is affected
according to the following table:

| Doors | Efficiency |
| ----- | ---------- |
| 1     | x100%      |
| 2     | x85%       |
| 3     | x80%       |
| 4     | x78%       |

6. Per assumption 5, the total number of doors cannot exceed four times the number of loaders.
7. For any loaders assigned to more than one door, all doors within the assignment must be adjacent
(ex. A loader cannot be assigned to doors 2 and 4 without also being assigned to door 3).

## Limitations
Loader Dispatch is primitive in its current state and is unable to account for many variables, including:
- The possibility of assigning more than one loader to a door
- The possibility of assigning loaders to non-adjacent doors
- Excluding doors from assignment (such as doors with zero FPH)
- Changes in FPH throughout the day
- Changes in loader PPH throughout the day
- Loader work breaks

As of now, Loader Dispatch should not be used as anything more than a recommendation.

## Potential Improvements
### Immediate Improvements
Possible immediate improvements include:
- Algorithm optimization (currently brute forcing all door-loader permutations)
- The possibility of assigning more than one loader to a door
- The possibility of assigning loaders to non-adjacent doors
- Excluding doors from assignment

### Future Improvements
Loader Dispatch has the capacity to be extremely useful, and could be used in real-time throughout a sort, but would need access to more data, such as:
- Real-time package flow data (to adjust assignments throughout the day based on flow changes, trailer replacements, etc.)
- Historical loader PPH data (account for decreases in loader PPH throughout the day, or week)
- Historical flow data (to make intra-day flow predictions)
- Real-time input of loader temperament (unhappy loaders generally have decreased PPH)

### Penalizing Excess Reassignment
Given this data, Loader Dispatch would likely "play musical doors" with loaders, losing efficiency by constantly making reassignments. A penalty to reassignment would prevent loaders from being moved around too much. This would need to be decided and adjusted based on the data available.

### Potential for Inbound Use
With some adjustments, Loader Dispatch could also be used in the inbound to maximize efficiency of unloading trailers.
