from datasets.dataset_reader import Dataset
from quickhull import QuickHull
from math import ceil

import sys 

class ApproxQuickHull(QuickHull):
    
    def _compute(self):
        # 1. Divide the x axis into buckets of size "error"
        (left, _), (right, _) = min(self._vertices), max(self._vertices)
        bucket_count = ceil((right - left) / self._error)
        buckets = [[(None, float('inf')), (None, float('-inf'))] for _ in range(bucket_count)]
        
        # 2. Keep track of the points in each bucket with largest and smallest y values
        for x, y in self._vertices:
            bucket_index = int((x - left) // self._error)
            if y > buckets[bucket_index][1][1]:
                buckets[bucket_index][1] = (x, y)
            if y < buckets[bucket_index][0][1]:
                buckets[bucket_index][0] = (x, y)
        
        # 3. Use the elements found in each bucket as the new vertices to solve quickhull
        self._vertices = list({ vertex for bucket in buckets for vertex in bucket if vertex[0] is not None })
        return super()._compute()

if __name__ == '__main__':
    error = float(sys.argv[1])
    dataset_name = sys.argv[2]
    dataset = Dataset(dataset_name)
    algo = ApproxQuickHull(dataset.data, error=error)
    solution = algo.compute()
    print(f'Solution: {solution}, \nRuntime: {algo.runtime}ms')