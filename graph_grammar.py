#!/usr/bin/python2

import graphviz
import copy
import random
import itertools

#TODO: is_tree_construction should not work return True if
#      two nodes in the tree_construction are connected in the tree
#      in a way they are not in the tree_construction

class Rule(object):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def eval(self, graph, pre_eval=False):
        for node in graph.get_tree_nodes():
            if node.is_tree_construction(self._lhs):
                node.replace_tree_construction(self._lhs, self._rhs, pre_eval=pre_eval)
                break

    def pre_eval(self, graph):
        self.eval(graph, pre_eval=True)

    def post_eval(self, graph):
        for node in graph.get_tree_nodes():
            node.just_replaced = False

    def is_applicable(self, graph):
        for node in graph.get_tree_nodes():
            if node.is_tree_construction(self._lhs):
                return True
        return False

    def __str__(self):
        return "LHS: {0}; RHS: {1}".format(self._lhs.list(), self._rhs.list())

class Grammar(object):
    def __init__(self, rules):
        self._rules = rules

    def expand(self, graph):
        for rule in self._rules:
            rule.pre_eval(graph)
        for rule in self._rules:
            rule.post_eval(graph)

class RandomGrammar(object):
    def __init__(self, rules_with_weights):
        self._rules_with_weights = rules_with_weights

    def expand(self, graph):
        applicable_rules_with_weights = self._applicable_rules(graph)
        rule = self._choose_rule(applicable_rules_with_weights)
        if rule is not None:
            rule.eval(graph)

    def _applicable_rules(self, graph):
        rules = []
        for rule, weight in self._rules_with_weights:
            if rule.is_applicable(graph):
                rules.append((rule, weight))
        return rules

    def _choose_rule(self, rules_with_weights):
        total = sum(weight for _, weight in rules_with_weights)
        r = random.uniform(0, total)

        weight_acc = 0
        for rule, weight in rules_with_weights:
            if weight_acc + weight >= r:
                return rule
            weight_acc += weight

        return None

class Node(object):
    _next_id = itertools.count(0)
    def set_next_id(self):
        self.id = next(self._next_id)

    def __init__(self, value, children = None, tag = None):
        if children is None:
            children = []

        for child in children:
            child.parents.append(self)

        self.value = value
        self.children = children
        self.parents = []
        self.tag = tag

        self.just_replaced = False

        self.set_next_id()

    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)

    def add_parent(self, parent):
        self.parents.append(parent)
        parent.children.append(self)

    def remove_child(self, child):
        self.children.remove(child)
        child.parents.remove(self)

    def remove_parent(self, parent):
        self.parents.remove(parent)
        parent.children.remove(self)

    def replace(self, new):
        for child in new.children:
            self.add_child(child)
        for parent in new.parents:
            self.add_parent(parent)
        self.value = new.value
#TODO: Old 'replace()', which should probably be removed...
#        for child in self.children:
#            new.add_child(child)
#            self.remove_child(child)
#        for parent in self.parents:
#            new.add_parent(parent)
#            self.remove_parent(parent)

    def is_tree_construction(self, tree):
        if self.just_replaced:
            return False

        if self.value == tree.value or tree.value == "*":
            if not tree.children:
                return True
            else:
                edge_combinations = [(this_edge, tree_edge)
                                     for this_edge in self.children
                                     for tree_edge in tree.children]
                for (this_edge, tree_edge) in edge_combinations:
                    if this_edge.is_tree_construction(tree_edge):
                        return True

        return False

    def replace_tree_construction(self, tree_con, new_tree_con, pre_eval=False):
        tree = copy.deepcopy(tree_con)
        new_tree = copy.deepcopy(new_tree_con)

        new_nodes = new_tree.list()
        for new_node in new_nodes:
            new_node.set_next_id()

#        tree_node_tags = [node.tag for node in tree.get_tree_nodes()]

#        tag_to_node = {}
#        for node in self._get_tree_construction_nodes(tree):
#            tag_to_node[node.tag] = node
#
#        for new_node in new_nodes:
#            new_node.just_replaced = pre_eval
#            if new_node.tag in tree_node_tags:
#                old_node = tag_to_node[tag]
#                for child in old_node.children:
#                    if child.tag is None:
#                        new_node.add_child(child)
#                        old_node.remove_child(child)
#                for parent in old_node.parent:
#                    if parent.tag is None:
#                        new_node.add_parent(parent)
#                        old_node.remove_child(parent)

        old_nodes = self._get_tree_construction_nodes(tree)

        print "new_nodes: " + str(new_nodes)
        print "old_nodes: " + str(old_nodes)

        tag_to_new_node = {}
        for new_node in new_nodes:
            tag_to_new_node[new_node.tag] = new_node
        print "tag_to_new_node: " + str(tag_to_new_node)

        new_tags = [new_node.tag for new_node in new_nodes if new_node.tag not in
                   [old_node.tag for old_node in old_nodes]]

        print "new_tags: " + str(new_tags)

        print ""

        for node in old_nodes:
            node.just_replaced = pre_eval
            print "node: " + str(node)
            new_node = tag_to_new_node[node.tag]
            print "new_node: " + str(new_node)
            print ""
            node.value = new_node.value if new_node.value != "*" else node.value

            children_to_remove = []
            for child in new_node.children:
                if child.tag in new_tags:
                    node.add_child(child)
                    print "adding child {0} to node {1}".format(child, node)
                    children_to_remove.append(child)
            for child in children_to_remove:
                print "REMOVING CHILD {0} FROM NEW_NODE {1}".format(child, new_node)
                new_node.remove_child(child)

            parents_to_remove = []
            for parent in new_node.parents:
                if parent.tag in new_tags:
                    node.add_parent(parent)
                    print "adding parent {0} to node {1}".format(parent, node)
                    parents_to_remove.append(parent)
            for parent in parents_to_remove:
                print "REMOVING PARENT {0} FROM NEW_NODE {1}".format(parent, new_node)
                new_node.remove_parent(parent)

            print "node.list(): " + str(node.list())
            print ""

            for child in node.children:
                if child.tag is not None and child.tag not in new_tags:
                    child_found = False
                    for new_node_child in new_node.children:
                        if child.tag == new_node_child.tag:
                            child_found = True
                            break
                    if not child_found:
                        print "REMOVING CHILD {0} FROM NODE {1}".format(child, node)
                        node.remove_child(child)
            for parent in node.parents:
                if parent.tag is not None and parent.tag not in new_tags:
                    parent_found = False
                    for new_node_parent in new_node.parents:
                        if parent.tag == new_node_parent.tag:
                            parent_found = True
                            break
                    if not parent_found:
                        print "REMOVING PARENT {0} FROM NODE {1}".format(parent, node)
                        node.remove_parent(parent)

        for node in self.get_tree_nodes():
            node.tag = None

    def _get_tree_construction_nodes(self, tree, nodes = None):
        if tree.tag is None:
            raise RuntimeError("Tree nodes must be tagged!")

        if nodes is None:
            nodes = []

        if self.value == tree.value or tree.value == "*":
            self.tag = tree.tag
            nodes.append(self)
            if not tree.children:
                return nodes
            else:
                edge_combinations = [(this_edge, tree_edge)
                                     for this_edge in self.children
                                     for tree_edge in tree.children]
                for (this_edge, tree_edge) in edge_combinations:
                    if this_edge.is_tree_construction(tree_edge):
                        return this_edge._get_tree_construction_nodes(tree_edge, nodes)

        raise RuntimeError("Cannot get tree construction that is not there...")


    def get_tree_nodes(self, nodes = None):
        if nodes is None:
            nodes = []

        if self not in nodes:
            yield self
            nodes.append(self)
            for node in self.children:
                for tree_node in node.get_tree_nodes(nodes):
                    yield tree_node
#    def get_tree_nodes(self, ids = None):
#        if ids is None:
#            ids = []
#
#        if self.id not in ids:
#            yield self
#            ids.append(self.id)
#            for node in self.children:
#                for tree_node in node.get_tree_nodes(ids):
#                    yield tree_node

    def list(self):
        return list(self.get_tree_nodes())

    def __str__(self):
        return "(value: {0}; id: {1}; tag: {2})".format(self.value, self.id, self.tag)

    def __repr__(self):
        return self.__str__()

    def dot_graph(self):
        dot_graph = graphviz.Digraph()

        for node in self.get_tree_nodes():
            dot_graph.node(str(node.id), node.value)
            for child in node.children:
                dot_graph.edge(str(node.id), str(child.id))

        return dot_graph

    def render(self, file_name):
        self.dot_graph().render(file_name, cleanup=True)

def old_main():
    node2 = Node("C")
    node1 = Node("B", [node2])
    node0 = Node("A", [node1])


    con_1_node2 = Node("C", [], "1")
    con_1_node1 = Node("B", [con_1_node2], "2")

    con_2_node3 = Node("D", [], "3")
    con_2_node2 = Node("C2", [con_2_node3], "1")
    con_2_node1 = Node("B2", [con_2_node2], "2")

    rule0 = Rule(con_1_node1, con_2_node1)


    con_3_node1 = Node("A", [], "1")
    con_4_node1 = Node("A1", [], "1")
    rule1 = Rule(con_3_node1, con_4_node1)


    grammar = Grammar([rule0, rule1])

    node0.render("gen0")

    grammar.expand(node0)

    node0.render("gen1")

    grammar.expand(node0)

    node0.render("gen2")

def main():
    graph = Node("S")
    graph.render("game_gen_0")

    rules = []
    rules.append(start_rule())
    rules.append(add_task_0())
    rules.append(add_task_1())
    rules.append(add_task_2())
    rules.append(define_task_0())
    rules.append(define_task_1())
    rules.append(move_lock())
    grammar = RandomGrammar(rules)

    for i in range(1,11):
        print "<<< GENERATION {0} >>>".format(i)
        grammar.expand(graph)
        graph.render("game_gen_{0}".format(str(i).zfill(2)))

def start_rule():
    lhs = Node("S", tag=0)

    rhs_node_0 = Node("e", tag=0)
    rhs_node_1 = Node("T", tag=1)
    rhs_node_2 = Node("g", tag=2)
    rhs_node_0.add_child(rhs_node_1)
    rhs_node_1.add_child(rhs_node_2)
    rhs = rhs_node_0

    prob = 1

    return (Rule(lhs, rhs), prob)

def add_task_0():
    lhs_node_0 = Node("T", tag=0)
    lhs_node_1 = Node("g", tag=1)
    lhs_node_0.add_child(lhs_node_1)
    lhs = lhs_node_0

    rhs_node_0 = Node("b", tag=0)
    rhs_node_1 = Node("g", tag=1)
    rhs_node_0.add_child(rhs_node_1)
    rhs = rhs_node_0

    prob = 1

    return (Rule(lhs, rhs), prob)

def add_task_1():
    lhs_node_0 = Node("T", tag=0)
    lhs_node_1 = Node("g", tag=1)
    lhs_node_0.add_child(lhs_node_1)
    lhs = lhs_node_0

    rhs_node_0 = Node("T", tag=0)
    rhs_node_2 = Node("T", tag=2)
    rhs_node_1 = Node("g", tag=1)
    rhs_node_0.add_child(rhs_node_2)
    rhs_node_2.add_child(rhs_node_1)
    rhs = rhs_node_0

    prob = 3

    return (Rule(lhs, rhs), prob)

def add_task_2():
    lhs_node_0 = Node("T", tag=0)
    lhs_node_1 = Node("g", tag=1)
    lhs_node_0.add_child(lhs_node_1)
    lhs = lhs_node_0

    rhs_node_0 = Node("T", tag=0)
    rhs_node_2 = Node("T", tag=2)
    rhs_node_3 = Node("T", tag=3)
    rhs_node_1 = Node("g", tag=1)
    rhs_node_0.add_child(rhs_node_2)
    rhs_node_2.add_child(rhs_node_3)
    rhs_node_3.add_child(rhs_node_1)
    rhs = rhs_node_0

    prob = 2

    return (Rule(lhs, rhs), prob)

def define_task_0():
    lhs = Node("T", tag=0)

    rhs = Node("t", tag=0)

    prob = 5

    return (Rule(lhs, rhs), prob)

def define_task_1():
    lhs_node_0 = Node("*", tag=0)
    lhs_node_1 = Node("T", tag=1)
    lhs_node_0.add_child(lhs_node_1)
    lhs = lhs_node_0

    rhs_node_0 = Node("*", tag=0)
    rhs_node_1 = Node("l", tag=1)
    rhs_node_2 = Node("k", tag=2)
    rhs_node_0.add_child(rhs_node_1)
    rhs_node_2.add_child(rhs_node_1)
    rhs_node_0.add_child(rhs_node_2)
    rhs = rhs_node_0

    prob = 10

    return (Rule(lhs, rhs), prob)

def move_lock():
    lhs_node_0 = Node("l", tag=0)
    lhs_node_1 = Node("*", tag=1)
    lhs_node_2 = Node("*", tag=2)
    lhs_node_2.add_child(lhs_node_1)
    lhs_node_1.add_child(lhs_node_0)
    lhs = lhs_node_0

    rhs_node_0 = Node("l", tag=0)
    rhs_node_1 = Node("*", tag=1)
    rhs_node_2 = Node("*", tag=2)
    rhs_node_2.add_child(rhs_node_1)
    rhs_node_2.add_child(rhs_node_0)
    rhs = rhs_node_0

    prob = 11

    return (Rule(lhs, rhs), prob)

if __name__ == "__main__":
    main()
