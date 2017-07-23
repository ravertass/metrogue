#!/usr/bin/python2

import itertools
import networkx as nx
from graph import *

def main():
    g = nx.DiGraph()
    g.add_node(0, value='S')
    render_pdf(g)

    random_set(g)
    locks_and_keys(g)

i = itertools.count(0)
def render_pdf(g):
    render(g, "cool_graph_{0}".format(str(i.next()).zfill(2)))

###############################################################
#                 Step 1: Create a random set                 #
###############################################################

def random_set(g):
    start_rule().apply(g)
    render_pdf(g)

    for _ in range(0,11):
        grow().apply(g)
    render_pdf(g)

    lock_goal().apply(g)
    render_pdf(g)

    while random_task_grammar().is_applicable(g):
        random_task_grammar().expand(g)
    render_pdf(g)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

def key():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)

    return Rule(lhs, rhs)

def task():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='t', mark=0)

    return Rule(lhs, rhs)

def lock():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='T', mark=0)

    rhs = nx.DiGraph()
    rhs.add_node(0, value='l', mark=0)

    return Rule(lhs, rhs)

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
    while unlocks().is_applicable(g):
        unlocks().apply(g)
    render_pdf(g)

    while lock_door().is_applicable(g):
        lock_door().apply(g)
    render_pdf(g)

    while remove_unnecessary_locks().is_applicable(g):
        remove_unnecessary_locks().apply(g)
    render_pdf(g)

    while move_unlocks_grammar_23().is_applicable(g):
        move_unlocks_grammar_23().expand(g)
    render_pdf(g)

    while remove_unnecessary_locks().is_applicable(g):
        remove_unnecessary_locks().apply(g)
    render_pdf(g)

    while move_unlocks_grammar_01().is_applicable(g):
        move_unlocks_grammar_01().expand(g)
    render_pdf(g)

    while remove_unnecessary_locks().is_applicable(g):
        remove_unnecessary_locks().apply(g)
    render_pdf(g)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

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

    return Rule(lhs, rhs)

def move_unlocks_grammar_23():
    rules = [
        (move_unlocks_2(),  1),
        (move_unlocks_2b(), 1),
        (move_unlocks_3(),  1),
        (move_unlocks_3b(), 1),
    ]

    return RandomGrammar(rules)

def remove_unnecessary_locks():
    lhs = nx.DiGraph()
    lhs.add_node(0, value='k', mark=0)
    lhs.add_node(1, value='l', mark=1)
    lhs.add_node(2, value='k', mark=2)
    lhs.add_node(2, value='l', mark=2)
    lhs.add_edge(0, 1, value='u')
    lhs.add_edge(2, 1, value='u')
    lhs.add_edge(2, 3, value='u')

    rhs = nx.DiGraph()
    rhs.add_node(0, value='k', mark=0)
    rhs.add_node(1, value='l', mark=1)
    rhs.add_node(2, value='k', mark=2)
    rhs.add_node(2, value='l', mark=2)
    rhs.add_edge(0, 1, value='u')
    rhs.add_edge(2, 3, value='u')

    return Rule(lhs, rhs)

if __name__ == '__main__':
    main()
