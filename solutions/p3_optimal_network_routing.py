import heapq
from typing import Dict, List, Set


def dijkstra_with_halving(
    graph: Dict,
    compression_nodes_set: Set[str],
    source: str,
    target: str,
):
    """
    Modified dijkstra algorithm that evaluates 2 possible paths if a compression node
    is the current evaluating node

    It works with a priority queue (min-heap) that stores (distance, node, halved)
    where halved is 0 (False) or 1 (True)

    Time complexity: O(E * log(V)) where E is the number of edges and V is the number of
    nodes
    """
    pq = []
    dist = {node: [float("inf"), float("inf")] for node in graph.keys()}

    dist[source][0] = 0
    heapq.heappush(pq, (0, source, 0))

    while pq:
        current_dist, node, halved = heapq.heappop(pq)
        if node == target:
            return current_dist
        if current_dist > dist[node][halved]:
            continue
        is_compression_node = node in compression_nodes_set
        for neighbor, weight in graph[node]:
            # Case 1: Move to neighbor without using halving
            if halved == 0 and current_dist + weight < dist[neighbor][0]:
                dist[neighbor][0] = current_dist + weight
                heapq.heappush(pq, (dist[neighbor][0], neighbor, 0))

            # Case 2: Move to neighbor using halved weight only if it is
            #         a compression node and we haven't halved yet
            if (
                halved == 0
                and is_compression_node
                and current_dist + weight / 2 < dist[neighbor][1]
            ):
                dist[neighbor][1] = current_dist + weight / 2
                heapq.heappush(pq, (dist[neighbor][1], neighbor, 1))

            # Case 3: Move to neighbor after already halving an edge
            if halved == 1 and current_dist + weight < dist[neighbor][1]:
                dist[neighbor][1] = current_dist + weight
                heapq.heappush(pq, (dist[neighbor][1], neighbor, 1))
    return -1


def find_minimum_latency_path(
    graph: Dict[str, List],
    compression_nodes: List[str],
    source: str,
    target: str,
):
    compression_nodes_set = set(compression_nodes)
    min_total_latency = dijkstra_with_halving(
        graph,
        compression_nodes_set,
        source,
        target,
    )
    if min_total_latency == -1:
        raise ValueError(f"Error: there is no path between {source} and {target}")
    return min_total_latency
