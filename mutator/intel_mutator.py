from arch import intel
from mutator.operand import ArgSize, ArgType, Operand
from mutator.base_mutator import BaseMutator


class IntelOperand(Operand):
    arch_registers = intel.REGISTERS
    arch_template = intel.TEMPLATE

    def __init__(self, expression, is_template=True):
        super().__init__(expression, is_template)

    def get_size(self):
        if 'BYTE' in self._expression:   return ArgSize.BYTE
        if 'WORD' in self._expression:   return ArgSize.WORD
        if 'DWORD' in self._expression:   return ArgSize.DWORD
        if 'QWORD' in self._expression:   return ArgSize.QWORD
        if 'XMMWORD' in self._expression:   return ArgSize.XMMWORD
        if 'YMMWORD' in self._expression:   return ArgSize.YMMWORD
        if 'ZMMWORD' in self._expression:   return ArgSize.ZMMWORD
        if 'TMMWORD' in self._expression:   return ArgSize.TMMWORD

        return ArgSize.UNKNOWN

    def get_normalized_operand(self):
        expr = self._expression
        # if expr is template, then print representative value
        if self._is_template:
            if expr == 'IMM':
                expr = 'IMM'
            elif expr == 'MEMB': # mem_base
                expr = '[REG]'
            elif expr == 'MEMBD': # mem_base_disp
                expr = '[REG+IMM]'
            elif expr == 'MEMD': # mem_disp
                expr = '[IMM]'
            else:
                tpl_elem = self.arch_template[expr][2]
                expr = tpl_elem[0]
        if self._directive:
            return '%s %s'%(self._directive, expr)
        return expr


class IntelMutator(BaseMutator):
    arch_template = intel.TEMPLATE

    def __init__(self, opcode, operands=None, prefix=''):
        super().__init__(opcode, operands, prefix=prefix)

    def copy(self):
        new_operands = [IntelOperand(operand.get_template()) for operand in self.operands]
        return IntelMutator(self.opcode, new_operands, self.prefix)

    def phase1(self):
        ret = [IntelMutator(self.opcode)]
        for num_of_op in range(1, 5):
            ops = [IntelOperand('REG64') for idx in range(num_of_op)]
            ret.append(IntelMutator(self.opcode, ops))
        return ret

    # permute_operand_type
    def phase2(self, permutations=[], idx = 0):
        operand_types = self.arch_template.keys()

        if idx > self.get_number_of_operands():
            return permutations
        elif idx == 0:
            init_permutation = [IntelMutator(self.opcode)]
            return self.phase2(init_permutation, idx+1)
        else:
            new_permutation = []
            for inst in permutations:
                for operand in operand_types:
                    new_inst = inst.copy()
                    new_inst.add_operand(IntelOperand(operand))
                    new_permutation.append(new_inst)
            return self.phase2(new_permutation, idx+1)

    # permute_operand_size
    def phase3(self):
        operand_sizes = ['BYTE', 'WORD', 'DWORD', 'QWORD', 'XMMWORD', 'YMMWORD', 'ZMMWORD', 'TBYTE',] # 'TMMWORD']
        permutations = []
        for size in operand_sizes:
            new_inst = self.copy()
            bUpdate = False
            for idx, operand in enumerate(self.operands):
                if operand.is_memory_operand():
                    new_inst.operands[idx].update_directive('%s PTR'%(size))
                    bUpdate = True
            if bUpdate:
                permutations.append(new_inst)

        return permutations

    # permute_prefix
    def phase4(self):
        permutations = []
        for prefix in intel.PREFIX:
            new_inst = self.copy()
            new_inst.update_prefix(prefix)
            permutations.append(new_inst)
        return permutations




