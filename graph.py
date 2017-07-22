#!/usr/bin/python2

class Graph(object):
    def  __init__(self):
        self.nodes = []
        self.edges = {}

    def node(self, value):
        node = Node(value)
        self.nodes.append(node)
        self.edges[node] = []

        return node

    def edge(self, node_a, node_b):
        self.edges[node_a].append(node_b)

    def contains_pattern(self, pattern):
        node_combos = [(self_node, pattern_node)
                       for self_node in self.nodes
                       for pattern_node in pattern.nodes]

        for self_node, pattern_node in node_combos:
            if self.has_pattern(self_node, pattern_node, pattern):
                return True

        return False

    def has_pattern(self, node, pattern_node, pattern, processed_pattern_nodes = None):
        if processed_pattern_nodes == None:
            processed_pattern_nodes = []

        self_edges = self.edges[node]
        pattern_edges = pattern.edges[pattern_node]

        if node.matches(pattern_node):
            processed_pattern_nodes.append(pattern_node)
            if not pattern_edges or len(pattern.nodes) == len(processed_pattern_nodes):
                return True

            edge_combos = [(self_edge, pattern_edge)
                           for self_edge in self_edges
                           for pattern_edge in pattern_edges]

            for self_edge, pattern_edge in edge_combos:
                if self.has_pattern(self_edge, pattern_edge, pattern,
                                    list(processed_pattern_nodes)):
                    return True

        return False

    def replace_pattern(self, pattern, replacement):
        pass

class Node(object):
    def __init__(self, value):
        self.value = value

    def matches(self, other):
        return self.value == other.value or "*" in (self.value, other.value)

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not (self == other)

def main():
    graph = Graph()
    node0 = graph.node("A")
    node1 = graph.node("B")
    node2 = graph.node("C")
    node3 = graph.node("d")
    graph.edge(node0, node1)
    graph.edge(node1, node2)
    graph.edge(node1, node3)

    pattern = Graph()
    pattern_node0 = pattern.node("B")
    pattern_node1 = pattern.node("C")
    pattern_node2 = pattern.node("D")
    pattern.edge(pattern_node0, pattern_node1)
    pattern.edge(pattern_node0, pattern_node2)

    print graph.contains_pattern(pattern)

if __name__ == "__main__":
    main()
