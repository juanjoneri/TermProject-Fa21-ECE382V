from abc import ABC, abstractmethod

import time

class Algorithm(ABC):

    @property
    def runtime(self):
        '''
        Runtime in ms
        '''
        return self._runtime

    def compute(self):
        start = time.time()
        solution = self._compute()
        self._runtime = (time.time() - start) / 1000
        return solution

    @abstractmethod
    def _compute(self):
        pass