#!/usr/bin/python2

import networkx as nx
from graph import *

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
