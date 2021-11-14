from algorithm import Algorithm
from datasets.dataset_reader import Dataset

import sys 

class QuickHull(Algorithm):
    
    def _compute():
        pass


if __name__ == '__main__':
    dataset = Dataset(sys.argv[1])
    algo = QuickHull(dataset.data)
    solution = algo.compute()
    check = dataset.check_solution(solution)
    print(f'Check: {check} \nSolution: {solution}, \nRuntime: {algo.runtime}ms')