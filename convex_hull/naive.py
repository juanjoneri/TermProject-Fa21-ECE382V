from itertools import combinations
from datasets.dataset_reader import DatasetReader

import numpy as np

def _is_in_hull(edge, vertices):
    '''
    Check that the cross product of the given edge with all other vertices has the same sign
    '''
    a, b = edge
    v = np.subtract(b, a)
    sign = None
    for c in vertices:
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



def compute(vertices):
    indices = {v: i  for i, v in enumerate(vertices)}
    hull = set()
    for edge in combinations(vertices, 2):
        if _is_in_hull(edge, vertices):
            a, b = edge
            hull.add((indices[a], indices[b]))
    
    return hull

if __name__ == '__main__':
    reader = DatasetReader('datasets/blobs-10')
    solution = compute(reader.data)
    print(reader.check_solution(solution))