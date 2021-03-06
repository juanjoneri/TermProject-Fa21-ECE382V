from algorithm import Algorithm
from collections import deque
from itertools import product, islice, cycle
from datasets.dataset_reader import Dataset

import sys

class DivideAndConquer(Algorithm):
    '''
    Divide each dataset into two datasets of equal size (using the median of the x coordinates) until
    sub-problem has size == 1 and can be solved trivially. Merge back the datasets using the naive upper and 
    lower tangent algorithm (listing all n^2/4 combinations of vertices between the left and right sides)
    complexity:  T(n) = 2 * T(n/2) + n^2 => O(n^2)
    '''

    def _compute(self):
        hull = self._compute_subproblem(0, len(self._vertices))
        return deque([self._get_index(vertex) for vertex in hull])
        
    
    def _compute_subproblem(self, start, end):
        if (end - start) == 1:
            a = self._vertices[start]
            return deque([a])
        
        mid = start + ((end - start) // 2)
        return self._merge(self._compute_subproblem(start, mid), self._compute_subproblem(mid, end))

    def _merge(self, left, right):
        lower_tangent, upper_tangent = self._get_lower_and_upper_tangents(left, right)
        hull = deque()
        for vertex in left:
            hull.append(vertex)
            if vertex == upper_tangent[0]:
                break
        
        for vertex in islice(cycle(right), right.index(upper_tangent[1]), None):
            hull.append(vertex)
            if vertex == lower_tangent[1]:
                break
        
        for vertex in islice(cycle(left), left.index(lower_tangent[0]), None):
            if vertex == left[0]:
                break
            hull.append(vertex)
        return hull


    def _get_lower_and_upper_tangents(self, left, right):
        x = (max([v[0] for v in left]) + min([v[0] for v in right])) / 2
        lower_tangent = float('inf'), None
        upper_tangent = float('-inf'), None
        for edge in product(left, right):
            intersection = DivideAndConquer._intersect(edge, x)            
            if intersection < lower_tangent[0]:
                lower_tangent = (intersection, edge)
            if intersection > upper_tangent[0]:
                upper_tangent = (intersection, edge)
        return lower_tangent[1], upper_tangent[1]    
    
    @classmethod
    def _intersect(cls, edge, x):
        dx = edge[1][0] - edge[0][0]
        dy = edge[1][1] - edge[0][1]
        return edge[0][1] + (dy * ((x - edge[0][0]) / dx))

if __name__ == '__main__':
    dataset = Dataset(sys.argv[1])
    algo = DivideAndConquer(dataset.data)
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')
