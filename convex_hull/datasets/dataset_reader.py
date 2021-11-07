import pandas as pd

from functools import cached_property
from collections import deque

class Dataset():

    def __init__(self, dataset):
        self._dataset = dataset

    def check_solution(self, hull):
        head = self.solution[0]

        if (len(hull) != len(self.solution)) or (head not in hull):
            return False

        while hull[0] != head:
            hull.rotate()
        
        if (self.solution == hull):
            return True
        
        # Its possible the solutions was reversed
        hull.reverse()
        hull.rotate()
        return self.solution == hull

    @cached_property
    def data(self):
        df = pd.read_csv(f'{self._dataset}/input.csv', header=None)
        data = list(df.itertuples(index=False, name=None))
        return data
    
    @cached_property
    def solution(self):
        with open(f'{self._dataset}/solution.txt') as f:
            sol = deque(map(int, f.read().split(',')))
        return sol


if __name__ == '__main__':
    dataset = Dataset('blobs-10')
    d = dataset.data
    s = dataset.solution
    print(d, s)