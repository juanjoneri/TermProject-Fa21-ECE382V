from algorithm import Algorithm
from datasets.dataset_reader import Dataset
import networkx as nx

import sys 

class QuickHull(Algorithm):
    
    def _compute(self):
        edge = (min(self._vertices), max(self._vertices))
        hull = nx.Graph()
        self._quickhull(edge, 1, hull) # Upper hull
        self._quickhull(edge, -1, hull) # Lower hull
        return Algorithm._to_deque(hull)


    def _quickhull(self, edge, side, hull):
        furthest = self._find_futhest(edge, side)

        if furthest is None:
            return self._add_to_hull(hull, edge)

        # Iterate on each side of the triangle
        for i in (0, 1):
            new_edge = furthest, edge[i]
            new_side = -QuickHull._sign(new_edge, edge[i-1])
            self._quickhull(new_edge, new_side, hull)
        
    def _find_futhest(self, edge, side):
        furthest = None, 0
        for v in self._vertices:
            if QuickHull._sign(edge, v) == side:
                distance = abs(QuickHull._distance(edge, v))
                if distance > furthest[1]:
                    furthest = v, distance
        
        return furthest[0]

    @classmethod
    def _distance(cls, edge, vertex):
        """
        Returns a value proportional to the distance between the vertex and the line given by the edge
        """
        x0, y0 = vertex
        x1, y1 = edge[0]
        x2, y2 = edge[1]
        return (x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)

    @classmethod
    def _sign(cls, edge, vertex):
        x = cls._distance(edge, vertex)
        if x == 0:
            return 0
        if x > 0:
            return 1
        return -1

if __name__ == '__main__':
    dataset = Dataset(sys.argv[1])
    algo = QuickHull(dataset.data)
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')