from algorithm import Algorithm

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
        def index_at(i):
            return self._get_index(self._vertices[i])

        if (end - start) == 2:
            # Only two vertices in this subproblem
            return [(index_at(start), index_at(end-1))]
        if (end - start) == 3:
            pass



    def _merge(self, left, right):
        pass


'''
[(0, 0), (1, 0), (1, 1)]
start = 0, end = 2
'''