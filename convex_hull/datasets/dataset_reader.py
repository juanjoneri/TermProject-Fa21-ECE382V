import pandas as pd

from functools import cached_property

class Dataset():

    def __init__(self, dataset):
        self._dataset = dataset

    def check_solution(self, edges):
        actual = {tuple(sorted(edge)) for edge in edges}
        expected = {tuple(sorted(edge)) for edge in self.solution}
        assert(actual == expected)

    @cached_property
    def data(self):
        df = pd.read_csv(f'{self._dataset}/input.csv', header=None)
        data = list(df.itertuples(index=False, name=None))
        return data
    
    @cached_property
    def solution(self):
        solution = []
        with open(f'{self._dataset}/solution.txt') as f:
            solution_nodes = list(map(int, f.read().split(',')))
            for edge in zip(solution_nodes, solution_nodes[1:]):
                solution.append(edge)
            solution.append((solution_nodes[-1], solution_nodes[0]))
        return solution


if __name__ == '__main__':
    dataset = Dataset('blobs-10')
    d = dataset.data
    s = dataset.solution
    print(d, s)