from copy import deepcopy
from os import listdir
from os.path import isfile, join
from typing import List, Set


def SORT_LITERALS(literalList: List[str]):
    result = deepcopy(literalList)
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


def RESOLVABLE(a: List[str], b: List[str]) -> bool:
    ''' Chỉ resolve khi hai mệnh đề có duy nhất một cặp literal đối nhau '''
    countOppositePair = 0
    for literal in a:
        if NEGATIVE(literal) in b:
            countOppositePair = countOppositePair + 1
    return countOppositePair == 1


def IS_MEANING_LESS(clause: List[str]) -> bool:
    for i in range(len(clause)):
        for j in range(i + 1, len(clause)):
            if NEGATIVE(clause[i]) == clause[j]:
                return True
    return False


def PL_RESOLVE(a: List[str], b: List[str]) -> List[List[str]]:
    if RESOLVABLE(a, b):
        data = a + [x for x in b if x not in a]
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                x = data[i]
                y = data[j]
                if x != 'removed' and y != 'removed' and NEGATIVE(x) == y:
                    data[i] = 'removed'
                    data[j] = 'removed'
        while 'removed' in data:
            data.remove('removed')
        if IS_MEANING_LESS(data):
            return []
        else:
            return [data]
    else:
        return []


def CONTAINS_EMPTY_CLAUSE(clauses: List[List[str]]):
    for clause in clauses:
        if len(clause) == 0:
            return True
    return False


def REMOVE_DUPLICATES(sequence: list):
    result = []
    for element in sequence:
        if element not in result:
            result.append(element)
    return result


def NOT(clause: list) -> List[list]:
    result = []
    for literal in clause:
        result.append([NEGATIVE(literal)])
    return result


def TO_STRING(clause: List[str]):
    if len(clause) > 0:
        return ' OR '.join(SORT_LITERALS(clause))
    else:
        return '{}'


def IS_SUBSET(a: List[List[str]], b: List[List[str]]):
    for clause in a:
        if clause not in b:
            return False
    return True


def PL_RESOLUTION(KB: List[List[str]], alpha: List[str]):

    outputs = []

    clauses = deepcopy(KB)
    clauses = clauses + [x for x in NOT(alpha) if x not in clauses]

    # print('\ninitial clauses =', clauses)

    new = []

    loop = 0
    start = 0
    while (True):
        loop = loop + 1
        print('\nloop #', loop)
        print('current clauses: ' + str(clauses))
        print('start: ' + str(start))
        for i in range(len(clauses)):
            for j in range(start, len(clauses)):
                if i <= j:
                    resolvents = PL_RESOLVE(clauses[i], clauses[j])
                    # print('resolve (' + str(clauses[i]) + ') and (' + str(clauses[j]) + ') = ' + str(resolvents))
                    new = new + [sorted(x)
                                 for x in resolvents if sorted(x) not in new]

        newClauses = [sorted(clause)
                      for clause in new if sorted(clause) not in clauses]
        outputs.append(len(newClauses))
        outputs = outputs + [TO_STRING(clause) for clause in newClauses]
        start = len(clauses)

        # print('loop #', loop)
        print(str(len(newClauses)) + ' new clauses: ' + str(newClauses))

        if CONTAINS_EMPTY_CLAUSE(new):
            # print('new contains empty clause: ', new)
            outputs.append('YES')
            return outputs

        if IS_SUBSET(new, clauses):
            # print('new is subset of clauses')
            # print('new =', new)
            # print('clauses =', clauses)
            outputs.append('NO')
            return outputs

        clauses = clauses + [sorted(x)
                             for x in new if sorted(x) not in clauses]


def CLAUSE(raw: str) -> List[str]:
    return sorted(list(set(raw.replace(' ', '').split('OR'))))


def READ_INPUT(inputFilePath: str):
    try:
        with open(inputFilePath, 'r') as inputFile:
            lines = inputFile.readlines()
            alpha = CLAUSE(lines[0].replace('\n', ''))
            numOfClauses = int(lines[1].replace('\n', ''))
            knowledgeBase = REMOVE_DUPLICATES([CLAUSE(lines[i + 2].replace('\n', '')) for i in range(numOfClauses)])
            return knowledgeBase, alpha
    except Exception as err:
        print(err)
        return None


def WRITE_OUTPUT(outputs: list, outputFilePath: str):
    with open(outputFilePath, 'w') as outputFile:
        outputFile.writelines([str(output) + '\n' for output in outputs])


def main():
    try:
        inputPaths = [join('INPUT', file) for file in listdir(
            'INPUT') if isfile(join('INPUT', file))]
        for inputPath in inputPaths:
            print(
                '========================================================================')
            print('\nInput file: ' + inputPath)
            inputs = READ_INPUT(inputPath)
            if inputs == None:
                raise Exception('Invalid input file: ' + inputPath)
            KB = inputs[0]
            alpha = inputs[1]
            print('Knowledge base: ' + str(KB))
            print('Alpha: ' + str(alpha))
            output = PL_RESOLUTION(KB, alpha, debug_mode=True)
            print('Output: ' + str(output))
            outputFilePath = inputPath.replace(
                'INPUT', 'OUTPUT').replace('input', 'output')
            WRITE_OUTPUT(output, outputFilePath)
    except Exception as error:
        print(str(error))


# # test
inputPath = 'INPUT/input0.txt'
inputs = READ_INPUT(inputPath)
KB = inputs[0]
alpha = inputs[1]
print('Knowledge base: ' + str(KB))
print('Alpha: ' + str(alpha))
output = PL_RESOLUTION(KB, alpha)
print('Output: ' + str(output))
outputFilePath = inputPath.replace('INPUT', 'OUTPUT').replace('input', 'output')
WRITE_OUTPUT(output, outputFilePath)