from algorithm import Algorithm
from collections import deque
from itertools import product
from datasets.dataset_reader import Dataset

import sys

class DivideAndConquer(Algorithm):
    '''
    Divide each dataset into two datasets of equal size (using the median of the x coordinates) until
    sub-problem has size < 3 and can be solved trivially. Merge back the datasets using the naive upper and 
    lower tangent algorithm
    order = O(n*log(n))
    '''

    def _compute(self):
        hull = self._compute_subproblem(0, len(self._vertices))
        return deque([self._get_index(vertex) for vertex in hull])
        
    
    def _compute_subproblem(self, start, end):
        if (end - start) == 2:
            a, b = self._vertices[start], self._vertices[start + 1]
            return deque([a, b])

        if (end - start) == 3:
            a = self._vertices[start]
            b, c = self._sort(self._vertices[start + 1], self._vertices[start + 2])
            return deque([a, b, c])
        
        mid = start + ((end - start) // 2)
        print(f'Iterating on {start}, {mid}, {end}')
        return self._merge(self._compute_subproblem(start, mid), self._compute_subproblem(mid, end))

    @classmethod
    def _sort(cls, a, b):
        '''
        Returns a and b in decreasing order of y and increasing order of x
        '''
        vertices = [a, b]
        vertices.sort(key=lambda x: (-x[1], x[0]))
        return tuple(vertices)


    @classmethod
    def _merge(cls, left, right):
        lower_tangent, upper_tangent = DivideAndConquer._get_lower_and_upper_tangents(left, right)
        hull = deque()
        for vertex in left:
            hull.append(vertex)
            if vertex == upper_tangent[0]:
                break
        for vertex in list(right)[right.index(upper_tangent[1]):]:
            hull.append(vertex)
            if vertex == lower_tangent[1]:
                break
        for vertex in list(left)[left.index(lower_tangent[0]):]:
            hull.append(vertex)
        return hull


    @classmethod
    def _get_lower_and_upper_tangents(cls, left, right):
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
