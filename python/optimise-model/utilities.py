"""
Normalise a set of intervals so that they become delimited, in other words,
gets rid of any values from intervals where no probability distributions
exist for it.
"""
def normalise(intervals):
    min_sum = 0
    max_sum = 0
    for i in intervals:
        min_sum += intervals[i][0]
        max_sum += intervals[i][1]
    for i in intervals:
        if intervals[i][0] == intervals[i][1]:
            continue
        x = intervals[i][0]
        y = intervals[i][1]
        intervals[i][0] = max(intervals[i][0], 1 -
                              max_sum + y)
        intervals[i][1] = min(intervals[i][1], 1 -
                              min_sum + x)


"""
Create a probability distribution given the probability intervals
and surrogate values, and returns it"""
def choose_probabilities(intervals, parameters):
    probs = []
    assert(len(intervals) == len(parameters)+1), "length mismatch found"

    for i in range(0, len(intervals)):
        s = 's_'+str(i+1)
        if i == len(intervals)-1:
            prob = 1 - sum(probs)
        else:
            prob = intervals[s][0] + \
                (intervals[s][1] - intervals[s][0])*parameters[i]
        intervals[s][0] = prob
        intervals[s][1] = prob
        probs.append(prob)
        normalise(intervals)

    return probs

if __name__ == '__main__':
    type_1 = {
            's_1': [0.33438219267483904, 0.33438219267483904],
            's_2': [0.2068075423816448, 0.2068075423816448],
            's_3': [0.02, 0.2],
            's_4': [0.2774021413473147, 0.2774021413473147],
            's_5': [0.07, 0.15]
        }
    normalise(type_1)
    print(type_1)
