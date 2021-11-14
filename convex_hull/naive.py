from itertools import combinations
from datasets.dataset_reader import Dataset
from algorithm import Algorithm

import sys 
import numpy as np

class Naive(Algorithm):
    '''
    For each pair of vertices (i,j) in the dataset, check if the edge (i,j) is in the hull by
    checking that all other vertices are on the same half-plane delimited by the given edge.
    complexity: O(n^3)
    '''

    def _compute(self):
        hull = {}
        for edge in combinations(self._vertices, 2):
            if self._is_in_hull(edge):
                self._add_to_hull(hull, edge)
        
        return Algorithm._to_deque(hull)

    def _is_in_hull(self, edge):
        '''
        Check that the cross product of the given edge with every other vertex in the dataset has
        the same sign.
        '''
        a, b = edge
        v = np.subtract(b, a)
        sign = None
        for c in self._vertices:
            w = np.subtract(c, a)
            cross = np.cross(v, w)
            current_sign = (cross > 0)
            if (cross == 0):
                continue # Skip vertices a, and b
            elif sign is None:
                sign = current_sign
            elif sign != current_sign:
                return False
        
        return True


if __name__ == '__main__':
    dataset = Dataset(sys.argv[1])
    algo = Naive(dataset.data)
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')
