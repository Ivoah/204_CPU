import sys

instructions = {
    'add': [0b0000, 'dest', 'op1', 'op2'],
    'load': [0b0001, 'dest', 'addr'],
    'store': [0b0010, 'op1', 'addr'],
    'addi': [0b0011, 'dest', 'op1', 'num'],
    'and': [0b0100, 'dest', 'op1', 'op2'],
    'not': [0b0101, 'dest', 'op1'],
    'jump': [0b0110, 'addr'],
    'branch.eq': [0b0111, 'addr'],
    'input': [0b1000, 'dest', 'dev'],
    'output': [0b1001, 'op1', 'dev'],
    'compare.eq': [0b1010, 'op1', 'op2'],
    'loadp': [0b1011, 'dest', 'op1'],
    'storep': [0b1100, 'op1', 'op2'],
    'halt': [0b1111]
}

macros = {
    '.str': lambda *args: [ord(c) for c in ' '.join(args)] + [0],
    '.bytes': lambda *args: [parsenum(n) for n in args]
}

registers = {
    'r0': 0,
    'r1': 1,
    'r2': 2,
    'r3': 3
}

packing = {
    'opcode': 12,
    'dest': 10,
    'op1': 8,
    'op2': 6,
    'num': 0,
    'addr': 0,
    'dev': 0
}

def parsenum(n):
    if n in labels.keys():
        return labels[n]
    elif n.startswith('\''):
        if len(n) == 4 and n[1] == '\\':
            return {
                '\\': ord('\\'),
                'a': ord('\a'),
                'b': ord('\b'),
                'f': ord('\f'),
                'n': ord('\n'),
                'r': ord('\r'),
                't': ord('\t'),
            }[n[2]]
        elif len(n) == 3:
            return ord(n[1])
        else:
            raise ValueError(f'Malformed character {n}')
    elif n.startswith('0x'):
        return int(n[2:], 16)
    elif n.startswith('0b'):
        return int(n[2:], 2)
    else:
        return int(n)

labels = {}
program = []

with open(sys.argv[1]) as source:
    pc = 0
    for line in source:
        line = line.strip().split()

        if line[0] in instructions.keys():
            program.append(line)
            pc += 2
        elif line[0] in macros.keys():
            program.append(line)
            pc += len(macros[line[0]](*line[1:]))
        elif line[0].endswith(':'):
            labels[line[0][:-1]] = pc

with open(sys.argv[2], 'wb') as output:
    for line in program:
        if line[0] in instructions.keys():
            instr = instructions[line[0]][0] << packing['opcode']
            for i in range(1, len(line)):
                arg_type = instructions[line[0]][i]
                if arg_type in ['dest', 'op1', 'op2']:
                    v = registers[line[i]]
                elif arg_type in ['num', 'dev', 'addr']:
                    v = parsenum(line[i])

                instr |= v << packing[instructions[line[0]][i]]
            output.write(instr.to_bytes(2, 'big'))

        elif line[0] in macros.keys():
            output.write(bytes(macros[line[0]](*line[1:])))
