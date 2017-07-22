#!/usr/bin/python2

import random
import networkx as nx
import networkx.algorithms.isomorphism as iso
import networkx.drawing.nx_pydot as dot
import graphviz

class RandomGrammar(object):
    def __init__(self, rules_with_weights):
        self._rules_with_weights = rules_with_weights

    def expand(self, graph):
        applicable_rules_with_weights = self._applicable_rules(graph)
        rule = self._choose_rule(applicable_rules_with_weights)
        if rule is not None:
            rule.apply(graph)

    def _applicable_rules(self, graph):
        rules = []
        for rule, weight in self._rules_with_weights:
            if rule.is_applicable(graph):
                if weight == 11:
                    print "yes"
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

class Rule(object):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def is_applicable(self, graph):
        return self._matcher(graph).subgraph_is_isomorphic()

    def _matcher(self, graph):
        return iso.DiGraphMatcher(graph,
                                  self._lhs,
                                  node_match=do_nodes_match,
                                  edge_match=do_edges_match)

    def apply(self, graph):
        marked_nodes = self._marked_nodes(graph)

        self._remove_edges(graph, marked_nodes.values())

        r_marks = []
        new_nodes = {}
        # Change values of existing nodes with equiv marks, and add nodes with new marks
        for r_node, r_node_attrs in self._rhs.nodes(data=True):
            mark = r_node_attrs['mark']
            r_marks.append(mark)
            if mark in marked_nodes.keys():
                # Node in RHS has equiv in LHS
                node = marked_nodes[mark]
                new_value = r_node_attrs['value']
                if new_value != '*':
                    graph.node[node]['value'] = new_value
                new_nodes[mark] = node
            else:
                # Node in RHS has no equiv in LHS
                node = add_node(graph, r_node_attrs['value'])
                new_nodes[mark] = node

        # Remove nodes with marks not in RHS
        for mark, node in marked_nodes.iteritems():
            if mark not in r_marks:
                graph.remove_node(node)

        self._add_edges(graph, new_nodes)

    def _marked_nodes(self, graph):
        marked_nodes = {}
        matcher = self._matcher(graph)
        for match in matcher.subgraph_isomorphisms_iter():
            for g_node, l_node in match.iteritems():
                l_node_attrs = self._lhs.node[l_node]
                marked_nodes[l_node_attrs['mark']] = g_node

        return marked_nodes

    def _remove_edges(self, graph, nodes):
        for node in nodes:
            for succ in graph.successors(node):
                if succ in nodes:
                    graph.remove_edge(node, succ)
            for pred in graph.predecessors(node):
                if pred in nodes:
                    graph.remove_edge(pred, node)

    def _add_edges(self, graph, new_nodes):
        for r_node, r_node_attrs in self._rhs.nodes(data=True):
            mark = r_node_attrs['mark']
            new_node = new_nodes[mark]
            for succ in self._rhs.successors(r_node):
                succ_mark = self._rhs.node[succ]['mark']
                new_succ = new_nodes[succ_mark]
                value = self._rhs[r_node][succ].get('value')
                graph.add_edge(new_node, new_succ, value=value)


def do_nodes_match(node_attrs_a, node_attrs_b):
    return node_attrs_a['value'] == node_attrs_b['value'] or \
           '*' in (node_attrs_a['value'], node_attrs_b['value'])

def do_edges_match(edge_attrs_a, edge_attrs_b):
    return edge_attrs_a.get('value') == edge_attrs_b.get('value')

def add_node(graph, value, mark=None):
    n = 0
    while n in graph.nodes():
        n += 1
    if mark is None:
        graph.add_node(n, value=value)
    else:
        graph.add_node(n, value=value, mark=mark)

    return n

def pydot_graph(nx_graph):
    dot_graph = graphviz.Digraph()

    for node, node_attrs in nx_graph.nodes(data=True):
        dot_graph.node(str(node), node_attrs['value'])

    for node, succ, value in nx_graph.edges(data='value'):
        if value is not None and value == 'u':
            arrowhead = 'diamond'
        else:
            arrowhead = 'normal'
        dot_graph.edge(str(node), str(succ), arrowhead=arrowhead)

    return dot_graph

def render(nx_graph, file_name):
    pydot_graph(nx_graph).render(file_name, cleanup=True)

def main():
    graph = nx.DiGraph()
    graph.add_node(0, value='S')
    render(graph, "game_gen_00")

    start_rule().apply(graph)
    render(graph, "game_gen_01")

    #add_task_grammar = RandomGrammar([(add_task_0(), 2), (add_task_1(), 1)])
    for i in range(2,8):
        #add_task_grammar.expand(graph)
        add_task_0().apply(graph)
        render(graph, "game_gen_{0}".format(str(i).zfill(2)))

    add_boss().apply(graph)
    render(graph, "game_gen_08")

    define_task_grammar = RandomGrammar([(define_task_0(), 1), (define_task_1(), 1)])
    for i in range(9,15):
        define_task_grammar.expand(graph)
        render(graph, "game_gen_{0}".format(str(i).zfill(2)))

    for i in range(15,21):
        if move_lock().is_applicable(graph):
            move_lock().apply(graph)
            render(graph, "game_gen_{0}".format(str(i).zfill(2)))

def start_rule():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='S', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='e', mark=0)
    rhs.add_node(1, value='T', mark=1)
    rhs.add_node(2, value='g', mark=2)
    rhs.add_edge(0, 1)
    rhs.add_edge(1, 2)

    return Rule(lhs, rhs)

def add_boss():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)
    lhs.add_node(1, value='g', mark=1)
    lhs.add_edge(0, 1)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='b', mark=0)
    rhs.add_node(1, value='g', mark=1)
    rhs.add_edge(0, 1)

    return Rule(lhs, rhs)

def add_task_0():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)
    lhs.add_node(1, value='g', mark=1)
    lhs.add_edge(0, 1)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='T', mark=0)
    rhs.add_node(2, value='T', mark=2)
    rhs.add_node(1, value='g', mark=1)
    rhs.add_edge(0, 2)
    rhs.add_edge(2, 1)

    return Rule(lhs, rhs)

def add_task_1():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)
    lhs.add_node(1, value='g', mark=1)
    lhs.add_edge(0, 1)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='T', mark=0)
    rhs.add_node(2, value='T', mark=2)
    rhs.add_node(3, value='T', mark=3)
    rhs.add_node(1, value='g', mark=1)
    rhs.add_edge(0, 2)
    rhs.add_edge(2, 3)
    rhs.add_edge(3, 1)

    return Rule(lhs, rhs)

def define_task_0():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='t', mark=0)

    return Rule(lhs, rhs)

def define_task_1():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='T', mark=1)
    lhs.add_edge(0, 1)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='k', mark=2)
    rhs.add_edge(0, 1)
    rhs.add_edge(0, 2)
    rhs.add_edge(2, 1, value='u')

    return Rule(lhs, rhs)

def move_lock():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='l', mark=0)
    lhs.add_node(1, value='*', mark=1)
    lhs.add_node(2, value='*', mark=2)
    lhs.add_edge(2, 1)
    lhs.add_edge(1, 0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='l', mark=0)
    rhs.add_node(1, value='*', mark=1)
    rhs.add_node(2, value='*', mark=2)
    rhs.add_edge(2, 1)
    rhs.add_edge(2, 0)

    return Rule(lhs, rhs)

if __name__ == '__main__':
    main()

