from itertools import combinations
from datasets.dataset_reader import import_dataset

def _is_in_hull(edge, vertices):
    return True

def compute(vertices):
    indices = {v: i  for i, v in enumerate(vertices)}
    hull = set()
    for edge in combinations(vertices, 2):
        if _is_in_hull(edge, vertices):
            a, b = edge
            hull.add((indices[a], indices[b]))
    
    print(hull)

if __name__ == '__main__':
    data, solution = import_dataset('datasets/blobs-10')
    compute(data)