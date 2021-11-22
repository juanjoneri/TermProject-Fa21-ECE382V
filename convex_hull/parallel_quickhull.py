from algorithm import Algorithm
from quickhull import QuickHull
from datasets.dataset_reader import Dataset
from math import log
from multiprocessing import Process, Queue
import networkx as nx

import sys 

class ParallelQuickHull(QuickHull):
    
    def _compute(self):
        edge = (min(self._vertices), max(self._vertices))

        q = Queue()
        if self._cores >= 2:
            t1 = Process(target=self._quickhull, args=(edge, 1, q))
            t2 = Process(target=self._quickhull, args=(edge, -1, q))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            self._quickhull(edge, 1, q)
            self._quickhull(edge, -1, q)
        
        hull = nx.compose(q.get(), q.get())
        return Algorithm._to_deque(hull)


    def _quickhull(self, edge, side, q, depth=2):
        furthest = self._find_futhest(edge, side)

        if furthest is None:
            hull = nx.Graph()
            self._add_to_hull(hull, edge)
            q.put(hull)
            return
        
        edge1 = furthest, edge[0]
        edge2 = furthest, edge[1]
        side1 = -QuickHull._sign(edge1, edge[1])
        side2 = -QuickHull._sign(edge2, edge[0])

        new_q = Queue()
        if (log(self._cores, 2) >= depth):
            t1 = Process(target=self._quickhull, args=(edge1, side1, new_q, depth+1))
            t2 = Process(target=self._quickhull, args=(edge2, side2, new_q, depth+1))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            self._quickhull(edge1, side1, new_q, depth+1)
            self._quickhull(edge2, side2, new_q, depth+1)
        
        hull = nx.compose(new_q.get(), new_q.get())
        q.put(hull)

if __name__ == '__main__':
    cores = int(sys.argv[1])
    dataset_name = sys.argv[2]
    dataset = Dataset(dataset_name)
    algo = ParallelQuickHull(dataset.data, cores=cores)
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')