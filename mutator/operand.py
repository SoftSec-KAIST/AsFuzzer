import random
from enum import IntEnum
from abc import ABC, abstractmethod

class ArgType(IntEnum):
    UNKNOWN = 0

    REGISTER = 1
    MEMORY = 2
    IMMEDIATE = 3


class ArgSize(IntEnum):
    UNKNOWN = 0

    BIT = 1
    BYTE = 8
    WORD = 16
    DWORD = 32
    QWORD = 64
    X87 = 80
    XMM = 128
    YMM = 256
    ZMM = 512

'''
OPERAND = DIRECTIVE EXPRESSION

DIRECTIVE, EXPRESSION is string
ex) OPERAND('R12'), OPERAND('DWORD PTR RDI')
Should be implemented like IntelOperand(Operand).
+ EXPRESSION could include TEMPLATE (ex. OPERAND('DWORD PTR REG64'))
'''
class Operand(ABC):
    def __init__(self, expression: str, is_template=True):
        self._directive = ' '.join(expression.split()[:-1])
        self._expression = expression.split()[-1]
        self._is_template = is_template
        
    # subclass should have self.arch_template property
    @property
    def arch_registers(self):
        raise NotImplementedError
    
    @property
    def arch_template(self):
        raise NotImplementedError

    def change_expression(self, old_pattern, new_pattern):
        new_expr = self._expression.replace(old_pattern, new_pattern)
        if self._expression != new_expr:
            self._expression = self._expression.replace(old_pattern, new_pattern)
            return True
        else:
            return False

    def update_directive(self, directive):
        self._directive = directive

    def is_template(self):
        return self._is_template

    def disable_template(self):
        self._is_template = False
        
    def get_type(self):
        if self._is_template:
            return self.arch_template[self._expression][0]
        
        if '[' in self._expression:
            return ArgType.MEMORY
        elif self._expression in self.arch_registers:
            return ArgType.REGISTER
        elif self._expression.isdigit():
            return ArgType.IMMEDIATE

        assert False, 'Define more rules to get type'
        return ArgType.UNKNOWN

    @abstractmethod
    def get_size(self):
        pass
    
    def __str__(self):
        expr = self._expression
        # if expr is template, then print representative value
        if self._is_template:
            tpl_elem = self.arch_template[expr][2]
            expr = tpl_elem[0] 
        if self._directive:
            return '%s %s'%(self._directive, expr)
        return expr

    def is_memory_operand(self):
        return ArgType.MEMORY == self.get_type()

    def get_template(self):
        if self._directive:
            return '%s %s'%(self._directive, self._expression)
        return self._expression

    @abstractmethod
    def get_normalized_operand(self):
        pass
    
    def get_random_operand(self):
        expr = self._expression
        if self._is_template:
            assert expr in self.arch_template.keys()
            # choose from list arch.TEMPLATE
            candidates = self.arch_template[expr][3]
            expr = random.choice(candidates)
        if self._directive:
            return '%s %s'%(self._directive, expr)
        return expr
        
                
