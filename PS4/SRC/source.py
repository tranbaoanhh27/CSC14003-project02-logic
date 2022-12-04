import copy
from os import listdir
from os.path import isfile, join
from typing import List, Set


def SORT_LITERALS(literalList: List[str]):
    result = copy.deepcopy(literalList)
    for i in range(len(result)):
        for j in range(i + 1, len(result)):
            a = result[i].replace('-', '')
            b = result[j].replace('-', '')
            if a > b:
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
    return result


def NEGATIVE(literal: str):
    if '-' in literal:
        return literal.replace('-', '')
    else:
        return '-' + literal


class CLAUSE:

    def __init__(self, clauseStr: str) -> None:
        if not clauseStr.replace(' ', '') == "{}":
            self.data = set(clauseStr.replace(' ', '').split('OR'))
        else:
            self.data = set()

    def NOT(self):
        clauses = []
        for literal in self.data:
            clauses.append(NEGATIVE(literal))
        result = set([CLAUSE(clause) for clause in clauses])
        return result

    def IS_EMPTY(self):
        return len(self.data) == 0

    def IS_MEANING_LESS(self):
        temp = list(copy.deepcopy(self.data))
        for i in range(len(temp)):
            for j in range(i + 1, len(temp)):
                if NEGATIVE(temp[i]) == temp[j]:
                    return True
        return False

    def __repr__(self) -> str:
        if len(self.data) == 0:
            return '{}'
        literals = SORT_LITERALS(list(self.data))
        return ' OR '.join(literals)

    def __eq__(self, __o: object) -> bool:
        return self.__repr__() == __o.__repr__()

    def __hash__(self) -> int:
        return hash(self.__repr__())


def RESOLVABLE(a: CLAUSE, b: CLAUSE) -> bool:
    ''' Chỉ resolve khi hai mệnh đề có duy nhất một cặp literal đối nhau '''
    countOppositePair = 0
    for literal in a.data:
        if NEGATIVE(literal) in b.data:
            countOppositePair = countOppositePair + 1
    return countOppositePair == 1


def PL_RESOLVE(a: CLAUSE, b: CLAUSE) -> set:
    if RESOLVABLE(a, b):
        data = list(a.data.union(b.data))
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                x = data[i]
                y = data[j]
                if x != 'removed' and y != 'removed' and NEGATIVE(x) == y:
                    data[i] = 'removed'
                    data[j] = 'removed'
        while 'removed' in data:
            data.remove('removed')
        result = CLAUSE('')
        result.data = set(data)
        if result.IS_MEANING_LESS():
            return set([])
        else:
            return set([result])
    else:
        return set([])


def CONTAINS_EMPTY_CLAUSE(clauses: Set[CLAUSE]):
    for clause in clauses:
        if clause.IS_EMPTY():
            return True
    return False


def PL_RESOLUTION(KB: Set[CLAUSE], alpha: CLAUSE, debug_mode: bool = False):

    outputs = []

    clauses = copy.deepcopy(KB)
    clauses = clauses.union(alpha.NOT())

    if debug_mode:
        print('\ninitial clauses =', clauses)

    new = set()

    loop = 0
    while (True):
        temp = list(clauses)

        loop = loop + 1
        if debug_mode:
            print('\nloop #', loop)
            print('current clauses: ' + str(temp))
        for i in range(len(temp)):
            for j in range(i + 1, len(temp)):
                resolvents = PL_RESOLVE(temp[i], temp[j])
                if debug_mode and len(resolvents) > 0:
                    print('resolve (' + str(temp[i]) + ') and (' + str(temp[j]) + ') = ' + str(resolvents))
                new = new.union(resolvents)

        newClauses = new - clauses
        outputs.append(len(newClauses))
        outputs = outputs + list(newClauses)

        if CONTAINS_EMPTY_CLAUSE(new):
            if debug_mode:
                print('new contains empty clause: ', new)
            outputs.append('YES')
            return outputs

        if new.issubset(clauses):
            if debug_mode:
                print('new is subset of clauses')
                print('new =', new)
                print('clauses =', clauses)
            outputs.append('NO')
            return outputs

        clauses = clauses.union(new)


def READ_INPUT(inputFilePath: str):
    try:
        with open(inputFilePath, 'r') as inputFile:
            lines = inputFile.readlines()
            alpha = CLAUSE(lines[0].replace('\n', ''))
            numOfClauses = int(lines[1].replace('\n', ''))
            knowledgeBase = set([CLAUSE(lines[i + 2].replace('\n', ''))
                                for i in range(numOfClauses)])
            return knowledgeBase, alpha
    except:
        return None


def WRITE_OUTPUT(outputs: list, outputFilePath: str):
    with open(outputFilePath, 'w') as outputFile:
        outputFile.writelines([str(output) + '\n' for output in outputs])


def main():
    try:
        inputPaths = [join('INPUT', file) for file in listdir('INPUT') if isfile(join('INPUT', file))]
        for inputPath in inputPaths:
            print('========================================================================')
            print('\nInput file: ' + inputPath)
            inputs = READ_INPUT(inputPath)
            if inputs == None:
                raise Exception('Invalid input file: ' + inputPath)
            KB = inputs[0]; alpha = inputs[1]
            print('Knowledge base: ' + str(KB))
            print('Alpha: ' + str(alpha))
            output = PL_RESOLUTION(KB, alpha, debug_mode=True)
            print('Output: ' + str(output))
            outputFilePath = inputPath.replace('INPUT', 'OUTPUT').replace('input', 'output')
            WRITE_OUTPUT(output, outputFilePath)
    except Exception as error:
        print(str(error))


# test
inputPath = 'test-input.txt'
inputs = READ_INPUT(inputPath)
KB = inputs[0]; alpha = inputs[1]
print('Knowledge base: ' + str(KB))
print('Alpha: ' + str(alpha))
output = PL_RESOLUTION(KB, alpha, debug_mode=True)
print('Output: ' + str(output))
outputFilePath = inputPath.replace('INPUT', 'OUTPUT').replace('input', 'output')
WRITE_OUTPUT(output, outputFilePath)