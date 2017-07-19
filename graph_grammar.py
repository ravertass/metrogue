#!/usr/bin/python2

# TODO: Make graph-based
class Rule(object):
    _temp_no = 0
    _temp_string = "%temp$%"

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

        temp_no = self.__class__._temp_no
        self.__class__._temp_no += 1
        self._temp_string = self.__class__._temp_string.replace("$", str(temp_no))

    def pre_eval(self, string):
        return string.replace(self._lhs, self._temp_string)

    def post_eval(self, string):
        return string.replace(self._temp_string, self._rhs)

# TODO: Make graph-based
class Grammar(object):
    def __init__(self, rules):
        self._rules = rules

    def expand(self, string):
        for rule in self._rules:
            string = rule.pre_eval(string)
        for rule in self._rules:
            string = rule.post_eval(string)

        return string

class Node(object):
    _next_id = 0

    def __init__(self, value, edges = None):
        if edges is None:
            edges = []

        self.value = value
        self.edges = edges

        self.id = self.__class__._next_id
        self.__class__._next_id += 1

    def add_edge(self, other):
        self.edges.append(other)

    def is_tree_construction(self, tree):
        if self.value == tree.value:
            if not tree.edges:
                return True
            else:
                edge_combinations = [(this_edge, tree_edge)
                                     for this_edge in self.edges
                                     for tree_edge in tree.edges]
                for (this_edge, tree_edge) in edge_combinations:
                    if this_edge.is_tree_construction(tree_edge):
                        return True

        return False

    def get_tree_nodes(self, ids = None):
        if ids is None:
            ids = []

        if self.id not in ids:
            yield self
            ids.append(self.id)
            for node in self.edges:
                for tree_node in node.get_tree_nodes(ids):
                    yield tree_node

    def __str__(self):
        return "(value: {0}; id: {1})".format(self.value, self.id)

    def __repr__(self):
        return self.__str__()

def old_main():
    rules = [Rule("A", "AB"), Rule("B", "A")]
    grammar = Grammar(rules)
    string = "A"
    print string

    for _ in range(10):
        string = grammar.expand(string)
        print string

def main():
    tree = Node(0)
    tree.add_edge(Node(1, [tree]))
    node2 = Node(2)
    tree.add_edge(Node(3, [tree, node2]))
    tree.add_edge(Node(4, [node2]))
    tree.add_edge(Node(5))

    tree_con = Node(1, [Node(0)])

    for node in tree.get_tree_nodes():
        if node.is_tree_construction(tree_con):
            print "foobar"

if __name__ == "__main__":
    main()
