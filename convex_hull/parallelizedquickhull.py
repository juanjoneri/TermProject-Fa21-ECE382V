from algorithm import Algorithm
from datasets.dataset_reader import Dataset
from math import log
from multiprocessing import Process, Queue
import networkx as nx

import sys 

class ParallelizedQuickHull(Algorithm):
    
    def _compute(self):
        edge = (min(self._vertices), max(self._vertices))
        upper = ParallelizedQuickHull._divide_vertices(edge, self._vertices, 1)
        lower = ParallelizedQuickHull._divide_vertices(edge, self._vertices, -1)

        q1, q2 = Queue(), Queue()
        if self.cores >= 2:
            t1 = Process(target=self._quickhull, args=(edge, upper, q1))
            t2 = Process(target=self._quickhull, args=(edge, lower, q2))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            hull1 = hull2 = nx.Graph()
            self._quickhull(edge, upper, q1)
            self._quickhull(edge, lower, q2)
        
        hull = nx.compose(q1.get(), q2.get())
        return Algorithm._to_deque(hull)


    def _quickhull(self, edge, vertices, q, depth=2):
        hull = nx.Graph()
        if not any(vertices):
            self._add_to_hull(hull, edge)
            q.put(hull)
            return
        
        furthest = ParallelizedQuickHull._find_futhest(edge, vertices)
        edge1 = furthest, edge[0]
        edge2 = furthest, edge[1]
        sign1 = -ParallelizedQuickHull._sign(ParallelizedQuickHull._distance(edge1, edge[1]))
        sign2 = -ParallelizedQuickHull._sign(ParallelizedQuickHull._distance(edge2, edge[0]))
        vertices1 = ParallelizedQuickHull._divide_vertices(edge1, vertices, sign1)
        vertices2 = ParallelizedQuickHull._divide_vertices(edge2, vertices, sign2)

        q1, q2 = Queue(), Queue()
        if (log(self.cores, 2) >= depth):
            t1 = Process(target=self._quickhull, args=(edge1, vertices1, q1, depth+1))
            t2 = Process(target=self._quickhull, args=(edge2, vertices2, q2, depth+1))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            self._quickhull(edge1, vertices1, q1, depth+1)
            self._quickhull(edge2, vertices2, q2, depth+1)
        
        hull1, hull2 = q1.get(), q2.get()
        hull.update(hull1.edges(), hull1.nodes())
        hull.update(hull2.edges(), hull2.nodes())
        q.put(hull)

        
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
    dataset = Dataset(sys.argv[2])
    algo = ParallelizedQuickHull(dataset.data, cores=int(sys.argv[1]))
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')