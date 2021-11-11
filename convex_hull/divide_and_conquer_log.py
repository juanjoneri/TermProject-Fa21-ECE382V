from divide_and_conquer import DivideAndConquer
from datasets.dataset_reader import Dataset

import sys

class DivideAndConquerLog(DivideAndConquer):
    '''
    Divide each dataset into two datasets of equal size (using the median of the x coordinates) until
    sub-problem has size == 1 and can be solved trivially. Merge back the datasets using the linear upper and 
    lower tangent algorithm.
    complexity:  T(n) = 2 * T(n/2) + n => O(n log n)
    '''

    def _get_lower_and_upper_tangents(self, left, right):
        x = (max([v[0] for v in left]) + min([v[0] for v in right])) / 2
        return DivideAndConquerLog._get_lower_tangent(x, left, right), DivideAndConquerLog._get_upper_tangent(x, left, right)

    @classmethod
    def _get_lower_tangent(cls, x, left, right):
        i, j = left.index(max(left)), 0
        edge = (left[i], right[j])
        lower_tangent = DivideAndConquer._intersect(edge, x), edge
        next_i, next_j = (i + 1) % len(left), (j - 1) % len(right)

        while DivideAndConquer._intersect((left[i], right[next_j]), x) < lower_tangent[0] or \
              DivideAndConquer._intersect((left[next_i], right[j]), x) < lower_tangent[0]:

            if DivideAndConquer._intersect((left[i], right[next_j]), x) < lower_tangent[0]:
                j = next_j
                next_j = (j - 1) % len(right)
            else:
                i = next_i
                next_i = (i + 1) % len(left)

            edge = (left[i], right[j])
            lower_tangent = DivideAndConquer._intersect(edge, x), edge
        
        return lower_tangent[1]

    @classmethod
    def _get_upper_tangent(cls, x, left, right):
        i, j = left.index(max(left)), 0
        edge = (left[i], right[j])
        upper_tangent = DivideAndConquer._intersect(edge, x), edge
        next_i, next_j = (i - 1) % len(left), (j + 1) % len(right)

        while DivideAndConquer._intersect((left[i], right[next_j]), x) > upper_tangent[0] or \
              DivideAndConquer._intersect((left[next_i], right[j]), x) > upper_tangent[0]:

            if DivideAndConquer._intersect((left[i], right[next_j]), x) > upper_tangent[0]:
                j = next_j
                next_j = (j + 1) % len(right)
            else:
                i = next_i
                next_i = (i - 1) % len(left)

            edge = (left[i], right[j])
            upper_tangent = DivideAndConquer._intersect(edge, x), edge

        return upper_tangent[1]


if __name__ == '__main__':
    dataset = Dataset(sys.argv[1])
    algo = DivideAndConquerLog(dataset.data)
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')
