from itertools import combinations
from datasets.dataset_reader import Dataset
from algorithm import Algorithm

import numpy as np

class NaiveAlgorithm(Algorithm):
    '''
    For each pair of points (i,j) in the dataset, check if the edge (i,j) is in the hull by
    checking that all other vertices are on the same half-plane delimited by the given edge.
    order = O(n^3)
    '''

    def __init__(self, vertices):
        self.vertices = vertices
        self._indices = {v: i  for i, v in enumerate(self.vertices)}

    def _compute(self):
        hull = set()
        for edge in combinations(self.vertices, 2):
            if self._is_in_hull(edge):
                a, b = edge
                hull.add((self._get_index(a), self._get_index(b)))
        
        return hull

    def _get_index(self, vertex):
        return self._indices[vertex]

    def _is_in_hull(self, edge):
        '''
        Check that the cross product of the given edge with every other vertex in the dataset has
        the same sign.
        '''
        a, b = edge
        v = np.subtract(b, a)
        sign = None
        for c in self.vertices:
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
    dataset = Dataset('datasets/blobs-10')
    algo = NaiveAlgorithm(dataset.data)
    solution = algo.compute()
    dataset.check_solution(solution)
    print(algo.runtime)
