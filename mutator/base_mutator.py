from abc import ABC, abstractmethod
from mutator.operand import ArgType


class BaseMutator(ABC):
    def __init__(self, opcode, operands=None, prefix=''):
        self.opcode = opcode
        if operands:    self.operands = operands
        else:           self.operands = []
        self.prefix = prefix
        self.logs = []
        self.valid = True

    def get_log(self):
        return self.logs

    def add_log(self, log):
        self.logs.append(log)

    def has_log(self):
        return len(self.logs) != 0

    def is_valid(self):
        return self.valid

    def disable(self):
        self.valid = False

    def copy(cls):
        pass

    def add_operand(self, operand):
        self.operands.append(operand)

    def get_number_of_operands(self):
        return len(self.operands)

    def update_prefix(self, prefix):
        self.prefix = prefix


    def fixup(self, old_operand, new_operand):
        for operand in self.operands:
            if operand.change_expression(old_operand, new_operand.upper()):
                operand.disable_template()

    def print_with_log(self):
        inst = str(self)
        if self.has_log():
            for idx, log in enumerate(self.logs):
                if idx == 0:
                    print('%-40s # %s'%(inst, log))
                else:
                    print('%-40s # %s'%('', log))
        else: print(inst)

    def get_template(self):
        tokens = []
        if not self.is_valid():
            tokens.append('#')

        if self.prefix:
            tokens.append(self.prefix)
        tokens.append(self.opcode)

        tokens.append(', '.join([op.get_template() for op in self.operands]))

        return ' '.join(tokens)

    def get_normalized_asm(self):
        tokens = []
        if not self.is_valid():
            tokens.append('#')

        if self.prefix:
            tokens.append(self.prefix)
        tokens.append(self.opcode)

        tokens.append(', '.join([op.get_normalized_operand() for op in self.operands]))

        return ' '.join(tokens)
    
    def get_random_asm(self):
        tokens = []
        if not self.is_valid():
            tokens.append('#')

        if self.prefix:
            tokens.append(self.prefix)
        tokens.append(self.opcode)

        tokens.append(', '.join([op.get_random_operand() for op in self.operands]))

        return ' '.join(tokens)

    def __str__(self):
        tokens = []
        if not self.is_valid():
            tokens.append('#')

        if self.prefix:
            tokens.append(self.prefix)
        tokens.append(self.opcode)

        tokens.append(', '.join([str(op) for op in self.operands]))

        return ' '.join(tokens)

    def reverse_order(self):
        tokens = []
        if not self.is_valid():
            tokens.append('#')

        if self.prefix:
            tokens.append(self.prefix)
        tokens.append(self.opcode)

        if self.opcode in ['xbegin, msvd, ljmp']:
            return ''

        new_operands = []
        for op in reversed(self.operands):
            if op.get_type() == ArgType.REGISTER:
                new_operands.append('%' + str(op))
            elif op.get_type() == ArgType.MEMORY:
                expr = str(op)[1:-1]
                if expr.isdigit():
                    tmp = '($%s)'%(expr)
                else:
                    tmp = '(%%%s)'%(expr)
                new_operands.append(tmp)
            elif op.get_type() == ArgType.IMMEDIATE:
                if self.opcode.startswith('j') or self.opcode in ['call', 'lcall']:
                    new_operands.append(str(op))
                else:
                    new_operands.append('$' + str(op))
            else:
                assert False, 'Unknown operands'
        tokens.append(', '.join(new_operands))

        return ' '.join(tokens)


