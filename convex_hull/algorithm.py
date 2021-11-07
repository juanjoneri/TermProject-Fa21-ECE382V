from abc import ABC, abstractmethod
from math import ceil

import time


class Algorithm(ABC):

    def __init__(self, vertices):
        self._vertices = sorted(vertices)
        self._indices = {v: i  for i, v in enumerate(vertices)}

    def compute(self):
        start = time.time()
        solution = self._compute()
        self._runtime = (time.time() - start) * 1000
        return solution

    @property
    def runtime(self):
        '''
        Runtime in ms
        '''
        return ceil(self._runtime)

    @abstractmethod
    def _compute(self):
        pass

    def _get_index(self, vertex):
        return self._indices[vertex]