from algorithm import Algorithm
from collections import deque

class DivideAndConquer(Algorithm):
    '''
    Divide each dataset into two datasets of equal size (using the median of the x coordinates) until
    sub-problem has size < 3 and can be solved trivially. Merge back the datasets using the naive upper and 
    lower tangent algorithm
    order = O(n*log(n))
    '''

    def _compute(self):
        return self._compute_subproblem(0, len(self._vertices))
    
    def _compute_subproblem(self, start, end):
        if (end - start) == 2:
            a, b = self._vertices[start], self._vertices[start + 1]
            return deque([self._get_index(a), self._get_index(b)])

        if (end - start) == 3:
            a = self._vertices[start]
            b, c = self._sort(self._vertices[start + 1], self._vertices[start + 2])
            return deque([self._get_index(a), self._get_index(b), self._get_index(c)])
        
        mid = start + ((end - start) // 2)
        return self._merge(self._compute_subproblem(start, mid), self._compute_subproblem(mid, end))


    def _sort(self, a, b):
        '''
        Returns a and b in decreasing order of y and increasing order of x
        '''
        vertices = [a, b]
        vertices.sort(key=lambda x: (-x[1], x[0]))
        return tuple(vertices)


    @classmethod
    def _merge(cls, left, right):
        pass


'''
[(0, 0), (1, 0), (1, 1)]
start = 0, end = 2
'''