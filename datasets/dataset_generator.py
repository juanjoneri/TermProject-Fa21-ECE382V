from sklearn import datasets
from matplotlib import pyplot
from scipy.spatial import ConvexHull

import os
import networkx as nx

def _build_graph(nodes, edges=[]):
    '''
    nodes: coordinates of the nodes asa n np array
    edges: ordered list of nodes in the convex hull
    '''
    n = nodes.shape[0]
    G = nx.Graph()
    G.add_nodes_from(list(range(n)))
    for x, y in zip(edges, edges[1:]):
        G.add_edge(x, y)
    if any(edges):
        G.add_edge(edges[-1], edges[0])
    return G

def _init_blobs(n_nodes, centers, std):
    nodes, _ = datasets.make_blobs(n_samples=n_nodes, centers=centers, cluster_std=std)
    edges = ConvexHull(nodes).vertices

    coordinates = dict(list(enumerate(map(tuple, nodes))))
    return _build_graph(nodes, edges), coordinates, edges

def _init_halfmoons(n_nodes, noise):
    nodes, _  = datasets.make_moons(n_samples=n_nodes, noise=noise)
    edges = ConvexHull(nodes).vertices

    coordinates = dict(list(enumerate(map(tuple, nodes))))
    return _build_graph(nodes, edges), coordinates, edges

def _plot_graph(G, coordinates, output_file):
    os.makedirs(output_file, exist_ok=True)

    fig = pyplot.figure()
    fig.add_subplot(1,1,1)
    pyplot.axes([0, 0, 1, 1])
    nx.draw(G, coordinates, with_labels=True)
    pyplot.savefig(f'{output_file}/plot.png')

def _save_data(coordinates, edges, output_file):
    os.makedirs(output_file, exist_ok=True)

    input = open(f'{output_file}/input.csv', 'w')
    for x, y in coordinates.values():
        input.write(f'{x}, {y}\n')
    input.close()

    output = open(f'{output_file}/solution.txt', 'w')
    output.write(','.join(map(str, edges)))
    output.close()

def _save_dataset(G, coordinates, edges, output_file):
    _save_data(coordinates, edges, output_file)
    _plot_graph(G, coordinates, output_file)

if __name__ == '__main__':

    for size in (10, 100, 1000, 5000, 10000):
        # Cluster
        G, coordinates, edges = _init_blobs(size, [(5,5)], 0.2)
        _save_dataset(G, coordinates, edges, f'cluster-{size}')

        # Blob
        G, coordinates, edges = _init_blobs(size, [(0,0), (1,1)], 0.3)
        _save_dataset(G, coordinates, edges, f'blobs-{size}')

        # Moon
        G, coordinates, edges = _init_halfmoons(size, 0.1)
        _save_dataset(G, coordinates, edges, f'moons-{size}')