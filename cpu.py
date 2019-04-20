from devices import *

# from https://stackoverflow.com/a/31151236/3552541
def bit_not(n, numbits=8):
    return (1 << numbits) - 1 - n

class CPU:
    def __init__(self):
        self.running = False

        self.pc = 0
        self.registers = [0]*4
        self.eq = False

        self.memory = [0]*256
        self.devices = [NullDev()]*256
        self.devices[0] = IODev()
        self.devices[1] = VideoDev()

        self.jumptable = [
            self._add,
            self._load,
            self._store,
            self._addi,
            self._and,
            self._not,
            self._jump,
            self._branch_eq,
            self._input,
            self._output,
            self._compare_eq,
            self._loadp,
            self._storep,
            self._loadi,
            self._comparei_eq,
            self._halt
        ]
    
    def load(self, filename):
        with open(filename, 'rb') as f:
            for i in range(256):
                b = f.read(1)
                self.memory[i] = ord(b) if b else 0
            
    def step(self):
        ir1 = self.memory[self.pc]
        self.pc += 1
        ir2 = self.memory[self.pc]
        self.pc += 1

        instr = {
            'op': ir1 >> 4,
            'dest': (ir1 >> 2) & 0b11,
            'op1': ir1 & 0b11,
            'op2': ir2 >> 6,
            'num': ir2,
            'addr': ir2,
            'dev': ir2
        }

        self.jumptable[instr['op']](**instr)
    
    def run(self):
        self.running = True
        while self.running:
            self.step()

    def _add(self, dest, op1, op2, **_):
        self.registers[dest] = (self.registers[op1] + self.registers[op2])%256
    
    def _load(self, dest, addr, **_):
        self.registers[dest] = self.memory[addr]
    
    def _store(self, op1, addr, **_):
        self.memory[addr] = self.registers[op1]
    
    def _addi(self, dest, op1, num, **_):
        self.registers[dest] = (self.registers[op1] + num)%256
    
    def _and(self, dest, op1, op2, **_):
        self.registers[dest] = self.registers[op1] & self.registers[op2]
    
    def _not(self, dest, op1, **_):
        self.registers[dest] = bit_not(self.registers[op1])
    
    def _jump(self, addr, **_):
        self.pc = addr
    
    def _branch_eq(self, addr, **_):
        if self.eq:
            self.pc = addr
    
    def _input(self, dest, dev, **_):
        self.registers[dest] = self.devices[dev].read()
    
    def _output(self, op1, dev, **_):
        self.devices[dev].write(self.registers[op1])
    
    def _compare_eq(self, op1, op2, **_):
        self.eq = self.registers[op1] == self.registers[op2]
    
    def _loadp(self, dest, op1, **_):
        self.registers[dest] = self.memory[self.registers[op1]]
    
    def _storep(self, op1, op2, **_):
        self.memory[self.registers[op2]] = self.registers[op1]
    
    def _loadi(self, dest, num, **_):
        self.registers[dest] = num

    def _comparei_eq(self, op1, num, **_):
        self.eq = self.registers[op1] == num

    def _halt(self, **_):
        self.running = False

if __name__ == '__main__':
    import sys

    cpu = CPU()
    cpu.load(sys.argv[1])
    cpu.run()
