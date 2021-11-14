from algorithm import Algorithm
from datasets.dataset_reader import Dataset
import networkx as nx

import sys 

class QuickHull(Algorithm):
    
    def _compute(self):
        edge = (self._vertices[0], self._vertices[-1])
        up = QuickHull._divide_vertices(edge, self._vertices, 1)
        down = QuickHull._divide_vertices(edge, self._vertices, -1)
        hull = nx.Graph()
        self._quickhull(edge, up, hull)
        self._quickhull(edge, down, hull)
        print(hull.edges)
        return QuickHull._to_deque(hull)


    def _quickhull(self, edge, vertices, hull):
        if not any(vertices):
            return self._add_to_hull(hull, edge)
        
        furthest = QuickHull._find_futhest(edge, vertices)
        edge1 = furthest, edge[0]
        edge2 = furthest, edge[1]
        sign1 = -QuickHull._sign(QuickHull._distance(edge1, edge[1]))
        sign2 = -QuickHull._sign(QuickHull._distance(edge2, edge[0]))

        self._quickhull(edge1, QuickHull._divide_vertices(edge1, vertices, sign1), hull)
        self._quickhull(edge2, QuickHull._divide_vertices(edge2, vertices, sign2), hull)

        return hull
        
    @classmethod
    def _find_futhest(cls, edge, vertices):
        return max(vertices, key=lambda v: abs(cls._distance(edge, v)))


    @classmethod
    def _divide_vertices(cls, edge, vertices, side):
        sol = set()
        for vertex in vertices:
            distance = cls._distance(edge, vertex)
            if cls._sign(distance) == side: 
                sol.add(vertex)
                
        return sol


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
    def _sign(cls, x):
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