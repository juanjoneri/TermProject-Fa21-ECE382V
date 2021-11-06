from sklearn import datasets
from matplotlib import pyplot
from scipy.spatial import ConvexHull

import networkx as nx
import numpy as np

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

def _plot_graph(G, coordinates, output_file):
    fig = pyplot.figure()
    fig.add_subplot(1,1,1)
    pyplot.axes([0, 0, 1, 1])
    nx.draw(G, coordinates, with_labels=True)
    pyplot.savefig(output_file)


def _init_blobs(n_nodes, centers, std):
    nodes, _ = datasets.make_blobs(n_samples=n_nodes, centers=centers, cluster_std=std)
    edges = ConvexHull(nodes)

    coordinates = dict(list(enumerate(map(tuple, nodes))))
    return _build_graph(nodes, edges.vertices), coordinates

def _init_halfmoons(n_nodes, noise):
    nodes, _  = datasets.make_moons(n_samples=n_nodes, noise=noise)
    edges = ConvexHull(nodes)

    coordinates = dict(list(enumerate(map(tuple, nodes))))
    return _build_graph(nodes, edges.vertices), coordinates

if __name__ == '__main__':
    G, coordinates = _init_blobs(20, [(0,0), (1,1)], 0.2)
    _plot_graph(G, coordinates, 'blobs.png')

    G, coordinates = _init_halfmoons(20, 0.1)
    _plot_graph(G, coordinates, 'moon.png')