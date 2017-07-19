#!/usr/bin/python2

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

class Grammar(object):
    def __init__(self, rules):
        self._rules = rules

    def expand(self, string):
        for rule in self._rules:
            string = rule.pre_eval(string)
        for rule in self._rules:
            string = rule.post_eval(string)

        return string

def main():
    rules = [Rule("A", "AB"), Rule("B", "A")]
    grammar = Grammar(rules)
    string = "A"
    print string

    for _ in range(10):
        string = grammar.expand(string)
        print string

if __name__ == "__main__":
    main()
