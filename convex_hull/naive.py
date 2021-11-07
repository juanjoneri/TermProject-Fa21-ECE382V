from itertools import combinations
from datasets.dataset_reader import DatasetReader

import numpy as np

class NaiveAlgorithm():

    def __init__(self, vertices):
        self.vertices = vertices
        self._indices = {v: i  for i, v in enumerate(self.vertices)}

    def compute(self):
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
        Check that the cross product of the given edge with all other vertices has the same sign
        '''
        a, b = edge
        v = np.subtract(b, a)
        sign = None
        for c in self.vertices:
            w = np.subtract(c, a)
            cross = np.cross(v, w)
            current_sign = (cross > 0)
            if (cross == 0):
                continue
            elif sign is None:
                sign = current_sign
            elif sign != current_sign:
                return False
        
        return True

if __name__ == '__main__':
    reader = DatasetReader('datasets/blobs-10')
    solution = NaiveAlgorithm(reader.data).compute()
    reader.check_solution(solution)
