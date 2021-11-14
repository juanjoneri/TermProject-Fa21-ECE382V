from abc import ABC, abstractmethod
from bidict import bidict
from collections import deque
from math import ceil

import time


class Algorithm(ABC):

    def __init__(self, vertices):
        self._vertices = sorted(vertices) # [(x1, y1), (x2, y2), ...]
        self._index_to_vertex = bidict(enumerate(vertices)) # (x1, y1) <-> 1

    def compute(self):
        '''
        Returns the solution obtained by running the algorithms as a double ended queue
        '''
        start = time.time()
        solution = self._compute()
        self._runtime = (time.time() - start)
        return solution

    @property
    def runtime(self):
        '''
        Returns the runtime in ms
        '''
        return ceil(self._runtime * 1000)

    @abstractmethod
    def _compute(self):
        pass

    def _get_index(self, vertex):
        return self._index_to_vertex.inv[vertex]

    def _get_vertex(self, index):
        return self._index_to_vertex[index]

    def _add_to_hull(self, hull, edge):
        a, b = tuple(map(self._get_index, edge))
        if a not in hull:
            hull[a] = b
        else:
            hull[b] = a
        return hull

    @classmethod
    def _to_deque(cls, hull):
        d = deque()
        d.append(next(iter(hull)))
        while(True):
            source = d[-1]
            target = hull[source]
            if target == d[0]:
                break
            d.append(target)
        return d