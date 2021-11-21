from algorithm import Algorithm
from datasets.dataset_reader import Dataset
import networkx as nx
from quickhull import QuickHull
from bidict import bidict
from math import ceil

import sys 

class ApproxQuickHull(QuickHull):
    
    def _compute(self):
        # remove some points
        brange = (min(self._vertices), max(self._vertices))
        bucketCount = ceil((brange[1][0] - brange[0][0])/self.error)
        buckets = [[(None, float('inf')), (None, float('-inf'))] for _ in range(bucketCount)]
        for vertex in self._vertices:
                bucketIndex = int((vertex[0]-brange[0][0])//self.error)
                if vertex[1] > buckets[bucketIndex][1][1]:
                    buckets[bucketIndex][1] = vertex
                if vertex[1] < buckets[bucketIndex][0][1]:
                    buckets[bucketIndex][0] = vertex
        vertices = set()
        for bucket in buckets:
            for ele in bucket:
                    if ele[0] != None:
                        vertices.add(ele)
        print([self._get_index(v) for v in vertices])
        self._vertices = list(vertices)
        self._vertices = sorted(vertices)
        #self._index_to_vertex = bidict(enumerate(self._vertices)) # (x1, y1) <-> 1
        print(self._vertices)
        return super()._compute()

if __name__ == '__main__':
    dataset = Dataset(sys.argv[1])
    algo = ApproxQuickHull(dataset.data, error = 0.2)
    solution = algo.compute()
    #check = dataset.check_solution(solution)
    print(f'Solution: {solution}, \nRuntime: {algo.runtime}ms')