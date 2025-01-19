import pytest

from solutions.p3_optimal_network_routing import find_minimum_latency_path


def test_minimun_latency():
    graph = {
        "A": [("B", 10), ("C", 20)],
        "B": [("D", 15)],
        "C": [("D", 30)],
        "D": [],
    }
    compression_nodes = ["B", "C"]
    source = "A"
    target = "D"
    returned_min_latency = find_minimum_latency_path(
        graph, compression_nodes, source, target
    )
    expected_min_latency = 17.5
    assert expected_min_latency == returned_min_latency


def test_large_graphs():
    n_nodes = 100000
    graph = {}
    for i in range(n_nodes):
        node = str(i)
        next_node = str(i + 1)
        graph[node] = [(next_node, 10)]

    last_node = str(n_nodes)
    graph[last_node] = []

    compression_nodes = [str(i) for i in range(n_nodes)]
    source = "0"
    target = last_node
    returned_min_latency = find_minimum_latency_path(
        graph, compression_nodes, source, target
    )
    assert returned_min_latency == n_nodes * 10 - 5


def test_path_not_found():
    graph = {
        "A": [("B", 10), ("C", 20)],
        "B": [("D", 15)],
        "C": [("D", 30)],
        "D": [],
        "E": [],
    }
    source = "A"
    target = "E"
    compression_nodes = ["A", "C"]
    with pytest.raises(
        ValueError, match=f"Error: there is no path between {source} and {target}"
    ):
        find_minimum_latency_path(graph, compression_nodes, source, target)
