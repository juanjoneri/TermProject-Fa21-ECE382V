import pandas as pd

class DatasetReader():

    def __init__(self, dataset):
        self.data = DatasetReader._read_data(dataset)
        self.solution = DatasetReader._read_solution(dataset)

    def check_solution(self, edges):
        actual = {tuple(sorted(edge)) for edge in edges}
        expected = {tuple(sorted(edge)) for edge in self.solution}
        assert(actual == expected)

    def _read_data(dataset):
        df = pd.read_csv(f'{dataset}/input.csv', header=None)
        data = list(df.itertuples(index=False, name=None))
        return data
    
    def _read_solution(dataset):
        solution = []
        with open(f'{dataset}/solution.txt') as f:
            solution_nodes = list(map(int, f.read().split(',')))
            for edge in zip(solution_nodes, solution_nodes[1:]):
                solution.append(edge)
            solution.append((solution_nodes[-1], solution_nodes[0]))
        return solution


if __name__ == '__main__':
    dataset_reader = DatasetReader('blobs-10')
    d = dataset_reader.data
    s = dataset_reader.solution
    print(d, s)