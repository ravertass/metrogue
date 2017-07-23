#!/usr/bin/python2

import itertools
import networkx as nx
import graphviz
from graph import *

def main():
    g = nx.DiGraph(name='2-step-graph')
    g.add_node(0, value='S')
    render_pdf(g)

    random_set(g)
    locks_and_keys(g)

###############################################################
#                 Step 1: Create a random set                 #
###############################################################

def random_set(g):
    start_rule().apply(g)

    grow_rule = grow()
    for _ in range(0,5):
        grow_rule.apply(g)

    lock_goal().apply(g)

    while random_task_grammar().is_applicable(g):
        random_task_grammar().expand(g)

def start_rule():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='S', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='e', mark=0)
    rhs.add_node(1, value='k', mark=1)
    rhs.add_node(2, value='T', mark=2)
    rhs.add_node(3, value='g', mark=3)
    rhs.add_edge(0, 1)
    rhs.add_edge(1, 2)
    rhs.add_edge(2, 3)

    return Rule('Start rule', lhs, rhs)

def grow():
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

    return Rule('Grow', lhs, rhs)

def lock_goal():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)
    lhs.add_node(1, value='g', mark=1)
    lhs.add_edge(0, 1)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='T', mark=0)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_node(1, value='g', mark=1)
    rhs.add_edge(0, 2)
    rhs.add_edge(2, 1)

    return Rule('Lock goal', lhs, rhs)

def key():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)

    return Rule('Key', lhs, rhs)

def task():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='t', mark=0)

    return Rule('Task', lhs, rhs)

def lock():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='l', mark=0)

    return Rule('Lock', lhs, rhs)

def random_task_grammar():
    rules = [
        (key(),  1),
        (task(), 1),
        (lock(), 1),
    ]

    return RandomGrammar(rules)

###############################################################
#             Step 2: Lock and key relationships              #
###############################################################

def locks_and_keys(g):
#    while unlocks().is_applicable(g):
#        unlocks().apply(g)
#    render_pdf(g)

    lock_door_rule = lock_door()
    while lock_door_rule.is_applicable(g):
        lock_door_rule.apply(g)
    #render_pdf(g)

    remove_unnecessary_locks_rule = remove_unnecessary_locks()
    while remove_unnecessary_locks_rule.is_applicable(g):
        remove_unnecessary_locks_rule.apply(g)
    #render_pdf(g)

    move_unlocks_grammar_23_grammar = move_unlocks_grammar_23()
    while move_unlocks_grammar_23_grammar.is_applicable(g):
        move_unlocks_grammar_23_grammar.expand(g)
    #render_pdf(g)

    while remove_unnecessary_locks_rule.is_applicable(g):
        remove_unnecessary_locks_rule.apply(g)
    #render_pdf(g)

#    while move_unlocks_grammar_01().is_applicable(g):
#        move_unlocks_grammar_01().expand(g)
#    render_pdf(g)
#
#    while remove_unnecessary_locks().is_applicable(g):
#        remove_unnecessary_locks().apply(g)
#    render_pdf(g)

def unlocks():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='k', mark=1)
    lhs.add_node(2, value='*', mark=2)
    lhs.add_edge(0, 1)
    lhs.add_edge(1, 2)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='k', mark=1)
    rhs.add_node(2, value='*', mark=2)
    rhs.add_edge(0, 1)
    rhs.add_edge(0, 2)
    rhs.add_edge(1, 2, value='u')

    return Rule('Unlocks', lhs, rhs)

def move_unlocks_0():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='k', mark=0)
    lhs.add_node(1, value='t', mark=1)
    lhs.add_node(2, value='*', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(1, 2)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)
    rhs.add_node(1, value='t', mark=1)
    rhs.add_node(2, value='*', mark=2)
    rhs.add_edge(0, 2, value='u')
    rhs.add_edge(1, 2)

    return Rule('Move unlocks 0', lhs, rhs)

def move_unlocks_0b():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='k', mark=0)
    lhs.add_node(1, value='t', mark=1)
    lhs.add_node(2, value='*', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(0, 2, value='u')
    lhs.add_edge(1, 2)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)
    rhs.add_node(1, value='t', mark=1)
    rhs.add_node(2, value='*', mark=2)
    rhs.add_edge(0, 2, value='u')
    rhs.add_edge(1, 2)

    return Rule('Move unlocks 0b', lhs, rhs)

def move_unlocks_1():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='k', mark=0)
    lhs.add_node(1, value='k', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(1, 2, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)
    rhs.add_node(1, value='k', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 2, value='u')
    rhs.add_edge(1, 2, value='u')

    return Rule('Move unlocks 1', lhs, rhs)

def move_unlocks_1b():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='k', mark=0)
    lhs.add_node(1, value='k', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(0, 2, value='u')
    lhs.add_edge(1, 2, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)
    rhs.add_node(1, value='k', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 2, value='u')
    rhs.add_edge(1, 2, value='u')

    return Rule('Move unlocks 1b', lhs, rhs)

def move_unlocks_grammar_01():
    rules = [
        (move_unlocks_0(),  1),
        (move_unlocks_0b(),  1),
        (move_unlocks_1(),  1),
        (move_unlocks_1b(), 1),
    ]

    return RandomGrammar(rules)

def lock_door():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='*', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1)
    lhs.add_edge(1, 2)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='*', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 1)
    rhs.add_edge(0, 2)
    rhs.add_edge(1, 2, value='u')

    return Rule('Lock door', lhs, rhs)

def move_unlocks_2():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='t', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1)
    lhs.add_edge(1, 2, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='t', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 1)
    rhs.add_edge(0, 2, value='u')

    return Rule('Move unlocks 2', lhs, rhs)

def move_unlocks_2b():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='t', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1)
    lhs.add_edge(0, 2, value='u')
    lhs.add_edge(1, 2, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='t', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 1)
    rhs.add_edge(0, 2, value='u')
    lhs.add_edge(1, 2)

    return Rule('Move unlocks 2b', lhs, rhs)

def move_unlocks_3():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='l', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(1, 2, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 1, value='u')
    rhs.add_edge(0, 2, value='u')

    return Rule('Move unlocks 3', lhs, rhs)

def move_unlocks_3b():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='l', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(0, 2, value='u')
    lhs.add_edge(1, 2, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 1, value='u')
    rhs.add_edge(0, 2, value='u')

    return Rule('Move unlocks 3b', lhs, rhs)

def move_unlocks_3c():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='l', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_node(3, value='*', mark=3)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(1, 2, value='u')
    lhs.add_edge(2, 3)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_node(3, value='*', mark=3)
    rhs.add_edge(0, 1, value='u')
    rhs.add_edge(0, 2, value='u')
    rhs.add_edge(1, 3)
    rhs.add_edge(2, 3)

    return Rule('Move unlocks 3c', lhs, rhs)

def move_unlocks_3d():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='*', mark=0)
    lhs.add_node(1, value='l', mark=1)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_node(3, value='*', mark=3)
    lhs.add_node(4, value='*', mark=4)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(1, 2, value='u')
    lhs.add_edge(2, 3)
    lhs.add_edge(1, 4)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='*', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_node(3, value='*', mark=3)
    rhs.add_node(4, value='*', mark=4)
    rhs.add_edge(0, 1, value='u')
    rhs.add_edge(0, 2, value='u')
    rhs.add_edge(1, 4)
    rhs.add_edge(2, 3)

    return Rule('Move unlocks 3d', lhs, rhs)

def move_unlocks_grammar_23():
    rules = [
        (move_unlocks_2(),  1),
        (move_unlocks_2b(), 1),
#        (move_unlocks_3(),  1),
        (move_unlocks_3b(), 1),
        (move_unlocks_3c(), 1),
        (move_unlocks_3d(), 1),
    ]

    return RandomGrammar(rules)

def remove_unnecessary_locks():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='k', mark=0)
    lhs.add_node(1, value='l', mark=1)
    lhs.add_node(2, value='k', mark=2)
    lhs.add_node(3, value='l', mark=3)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(2, 1, value='u')
    lhs.add_edge(2, 3, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='k', mark=2)
    rhs.add_node(3, value='l', mark=3)
    rhs.add_edge(0, 1, value='u')
    rhs.add_edge(2, 3, value='u')

    return Rule('Remove unnecessary unlocks', lhs, rhs)

if __name__ == '__main__':
    main()
