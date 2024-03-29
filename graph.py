#!/usr/bin/python2

import os, errno
import random
import networkx as nx
import networkx.algorithms.isomorphism as iso
import graphviz
import itertools

STEP_DIR = 'steps'
RULE_DIR = 'rules'

class RandomGrammar(object):
    def __init__(self, rules_with_weights):
        self._rules_with_weights = rules_with_weights

    def is_applicable(self, graph):
        for rule, _ in self._rules_with_weights:
            if rule.is_applicable(graph):
                return True
        return False

    def expand(self, graph):
        applicable_rules_with_weights = self._applicable_rules(graph)
        rule = self._choose_rule(applicable_rules_with_weights)
        if rule is not None:
            rule.apply(graph)

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

class Rule(object):
    _step_counter = itertools.count(0)

    def __init__(self, name, lhs, rhs, render=True):
        self.name = name
        self._lhs = lhs
        self._rhs = rhs

        self._should_render = render
        if self._should_render:
            self._render_rule()

    def is_applicable(self, graph):
        return self._matcher(graph).subgraph_is_isomorphic()

    def _matcher(self, graph):
        return iso.DiGraphMatcher(graph,
                                  self._lhs,
                                  node_match=do_nodes_match,
                                  edge_match=do_edges_match)

    def apply(self, graph):
        if not self.is_applicable(graph):
            raise RuntimeError("Should not try to apply inapplicable rule!")
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

        for node in new_nodes.values():
            graph.node[node]['preds'] = len(graph.predecessors(node))

        if self._should_render:
            self._render_step(graph, new_nodes.values())

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

    def _render_rule(self):
        if not os.path.exists(RULE_DIR):
            create_dir(RULE_DIR)

        lhs_dot = pydot_graph(self._lhs, unique=True)

        rhs_dot = pydot_graph(self._rhs, unique=True)

        dot = graphviz.Digraph(format='png')
        dot.subgraph(lhs_dot)
        dot.subgraph(rhs_dot)
        dot.graph_attr['label'] = self.name

        file_name = self.name.lower().replace(' ', '_')
        dot.render(os.path.join(RULE_DIR, file_name), cleanup=True)

    def _render_step(self, graph, new_nodes):
        if not os.path.exists(STEP_DIR):
            create_dir(STEP_DIR)

        dot = pydot_graph(graph, format='png', nodes_to_mark=new_nodes)
        dot.graph_attr['label'] = self.name

        i = self.__class__._step_counter.next()
        i_str = str(i).zfill(3)
        file_name = '{0}_{1}'.format(graph.graph['name'], i_str)
        dot.render(os.path.join(STEP_DIR, file_name), cleanup=True)

def create_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise



def do_nodes_match(node_attrs_a, node_attrs_b):
    return (node_attrs_a.get('value') == node_attrs_b.get('value') or \
           '*' in (node_attrs_a.get('value'), node_attrs_b.get('value'))) and \
           (node_attrs_a.get('preds') == node_attrs_b.get('preds') \
            if None not in (node_attrs_a.get('preds'), node_attrs_b.get('preds')) else True)

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

node_i = itertools.count(0)
def pydot_graph(nx_graph, format='pdf', nodes_to_mark=None, unique=False):
    if nodes_to_mark is None:
        nodes_to_mark = []

    suffix = str(node_i.next()) if unique else ''

    dot_graph = graphviz.Digraph(format=format)
    dot_graph.graph_attr['rankdir'] = 'LR'
    dot_graph.node_attr['fontname'] = 'Monospace'

    for node, node_attrs in nx_graph.nodes(data=True):
        mark = node_attrs.get('mark')
        mark_prefix = str(mark) + ' : ' if mark is not None else ''

        style = ''
        if node in nodes_to_mark:
            style = 'filled'

        label = str(node) + suffix
        dot_graph.node(label, mark_prefix + str(node_attrs.get('value')), style=style)

    for node, succ, value in nx_graph.edges(data='value'):
        if value is not None and value == 'u':
            arrowhead = 'odiamond'
        else:
            arrowhead = 'normal'
        dot_graph.edge(str(node) + suffix, str(succ) + suffix, arrowhead=arrowhead)

    return dot_graph

def render(nx_graph, file_name):
    pydot_graph(nx_graph).render(file_name, cleanup=True)

render_i = itertools.count(0)
def render_pdf(g):
    render(g, "{0}_{1}".format(g.graph.get('name'), str(render_i.next()).zfill(2)))

