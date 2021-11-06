import pandas as pd


def import_dataset(dataset_name):
    data = pd.read_csv(f'{dataset_name}/input.csv', header=None)
    with open(f'{dataset_name}/solution.txt') as f:
        solution = list(map(int, f.read().split(',')))

    return data, solution

if __name__ == '__main__':
    d, s = import_dataset('blobs-100')
    print(d, s)