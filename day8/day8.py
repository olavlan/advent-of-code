import itertools
import math
from typing import Iterator

Node = tuple[int, int, int]
Edge = tuple[int, int]  # references indices in a list of nodes
WeightedEdge = tuple[Edge, float]
NeighborList = list[set[int]]


def parse_junction_box_file(file_path: str) -> Iterator[Node]:
    with open(file_path, "r") as file:
        for line in file:
            x, y, z = line.rstrip("\n").split(",")
            yield int(x), int(y), int(z)


def generate_sorted_edges(nodes: list[Node]) -> list[Edge]:
    n = len(nodes)
    edges: list[WeightedEdge] = []
    for i, j in itertools.combinations(range(n), 2):
        distance = math.dist(nodes[i], nodes[j])
        edges.append(((i, j), distance))
    edges.sort(key=lambda c: c[1])
    return [c[0] for c in edges]


class Graph:
    neighbor_list: NeighborList
    not_visited: list[int]
    current_component: set[int]

    def __init__(self, n_nodes: int, edges: list[Edge]) -> None:
        self.neighbor_list = [set() for i in range(n_nodes)]
        for e in edges:
            self.add_edge(e)
        self.not_visited = list(range(len(self.neighbor_list)))

    def add_edge(self, edge: Edge):
        self.neighbor_list[edge[0]].add(edge[1])
        self.neighbor_list[edge[1]].add(edge[0])

    def walk(self, node: int):
        self.not_visited.remove(node)
        self.current_component.add(node)
        for neighbor in self.neighbor_list[node]:
            if neighbor in self.not_visited:
                self.walk(neighbor)

    def connected_components(self) -> list[set[int]]:
        components = []
        while self.not_visited:
            self.current_component = set()
            node = self.not_visited[0]
            self.walk(node)
            components.append(self.current_component.copy())
        return components


def solve_part1(file_path: str, iterations: int) -> int:
    nodes = list(parse_junction_box_file(file_path))
    n = len(nodes)
    edges = generate_sorted_edges(nodes)[:iterations]
    graph = Graph(n, edges)
    circuits = graph.connected_components()
    circuits.sort(key=lambda c: len(c), reverse=True)
    c1, c2, c3 = circuits[:3]
    return len(c1) * len(c2) * len(c3)


def solve_part2(file_path: str) -> int:
    nodes = list(parse_junction_box_file(file_path))
    n = len(nodes)
    possible_edges = generate_sorted_edges(nodes)
    graph = Graph(n, [])
    edge = possible_edges[0]
    joined = {edge[0], edge[1]}
    while graph.not_visited:
        edge = possible_edges.pop(0)
        graph.add_edge(edge)
        missing_first_node = edge[0] not in joined
        missing_second_node = edge[1] not in joined
        if missing_first_node == missing_second_node:
            continue
        start = edge[0] if missing_first_node else edge[1]
        graph.current_component = set()
        graph.walk(start)
        joined |= graph.current_component

    node1, node2 = nodes[edge[0]], nodes[edge[1]]
    return node1[0] * node2[0]


# print(solve_part1("input-test.txt", 10))
print(solve_part2("input.txt"))
