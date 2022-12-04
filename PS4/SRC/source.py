import copy

def SORT(literals: list[str]):
    result = copy.deepcopy(literals)
    for i in range(len(result)):
        for j in range(i + 1, len(result)):
            a = result[i].replace('-', '')
            b = result[j].replace('-', '')
            if a > b:
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
    return result

class CLAUSE:

    def __init__(self, clauseStr: str) -> None:
        if not clauseStr.replace(' ', '') == "{}":
            self.data = set(clauseStr.replace(' ', '').split('OR'))
        else:
            self.data = set()

    def NOT(self):
        clauses = []
        for literal in self.data:
            if '-' in literal:
                clauses.append(CLAUSE(literal.replace('-', '')))
            else:
                clauses.append(CLAUSE('-' + literal))
        return set(clauses)

    def IS_EMPTY(self):
        return len(self.data) == 0

    def __repr__(self) -> str:
        if len(self.data) == 0:
            return '{}'
        literals = SORT(list(self.data))
        return ' OR '.join(literals)

    def __eq__(self, __o: object) -> bool:
        return self.__repr__() == __o.__repr__()

    def __hash__(self) -> int:
        return hash(self.__repr__())


def PL_RESOLVE(a: CLAUSE, b: CLAUSE) -> set:
    pass


def CONTAINS_EMPTY_CLAUSE(clauses: set[CLAUSE]):
    for clause in clauses:
        if clause.IS_EMPTY():
            return True
    return False


def PL_RESOLUTION(KB: set[CLAUSE], alpha: CLAUSE) -> bool:
    clauses = copy.deepcopy(KB)
    clauses.union(alpha.NOT())
    new = set()
    while (True):
        for i in range(len(clauses)):
            for j in range(len(clauses)) and i != j:
                resolvents = PL_RESOLVE(clauses[i], clauses[j])
                if CONTAINS_EMPTY_CLAUSE(resolvents):
                    return True
                new.union(resolvents)
        if new.issubset(clauses):
            return False
        clauses = clauses.union(new)
        

x = CLAUSE('A OR -B')
y = CLAUSE('-B OR A')
z = CLAUSE('{}')

a = x.NOT()
b = y.NOT()

print('x = ', x)
print('y = ', y)
print('z =', z)
print('a = ', a)
print('b = ', b)

print(x == y)
print(a == b)