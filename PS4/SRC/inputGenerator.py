import random
from os import makedirs
from os.path import isdir
from copy import deepcopy
from typing import List

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

def generate(inputFilePath: str):
    literals = ['A', 'B', 'C', '-D', '-E', '-F']
    kb_size = random.randint(10, 20)

    kb = []
    while (len(kb) < kb_size):
        clauseLen = random.randint(3, 5)
        clause = ' OR '.join(SORT_LITERALS(list(set(random.choices(literals, k=clauseLen)))))
        if clause not in kb:
            kb.append(clause)

    alpha = ' OR '.join(SORT_LITERALS(list(set(random.choices(literals, k=random.randint(3, 5))))))
    while alpha in kb:
        alpha = ' OR '.join(SORT_LITERALS(list(set(random.choices(literals, k=random.randint(3, 5))))))

    output_data = [alpha, kb_size] + kb
    with open(inputFilePath, 'w') as inputFile:
        inputFile.writelines([str(x) + '\n' for x in output_data])


if not isdir('INPUT'):
    makedirs('INPUT')

for i in range(0, 5):
    path = f'INPUT/input{i}.txt'
    generate(path)