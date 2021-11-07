from algorithm import Algorithm

class DivideAndConquer(Algorithm):
    '''
    Divide each dataset into two datasets of equal size (using the median of the x coordinates) until
    sub-problem has size 3 and can be solved trivially. Merge back the datasets using the upper and 
    lower tangent algorithm
    order = O(n*log(n))
    '''

    def _compute(self):
        pass