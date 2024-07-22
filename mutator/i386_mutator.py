from arch import intel
from mutator.operand import ArgSize, ArgType, Operand
from mutator.base_mutator import BaseMutator


class I386Operand(Operand):
    arch_registers = intel.REGISTERS
    arch_template = intel.TEMPLATE_I386
    
    def __init__(self, expression, is_template=True):
        super().__init__(expression)

    def get_size(self):
        if 'BYTE' in self._expression:   return ArgSize.BYTE
        if 'WORD' in self._expression:   return ArgSize.WORD
        if 'DWORD' in self._expression:   return ArgSize.DWORD
        if 'QWORD' in self._expression:   return ArgSize.QWORD
        if 'XMMWORD' in self._expression:   return ArgSize.XMMWORD
        if 'YMMWORD' in self._expression:   return ArgSize.YMMWORD
        if 'ZMMWORD' in self._expression:   return ArgSize.ZMMWORD

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


class I386Mutator(BaseMutator):
    arch_template = intel.TEMPLATE_I386
    
    def __init__(self, opcode, operands=None, prefix=''):
        super().__init__(opcode, operands, prefix=prefix)

    def copy(self):
        new_operands = [I386Operand(operand.get_template()) for operand in self.operands]
        return I386Mutator(self.opcode, new_operands, self.prefix)

    # permute_number_of_operands_with_GP_regs
    def phase1(self):
        ret = [I386Mutator(self.opcode)]
        for num_of_op in range(1, 5):
            ops = [I386Operand('REG32') for idx in range(num_of_op)]
            ret.append(I386Mutator(self.opcode, ops))
        return ret

    # _operand_type
    def phase2(self, permutations=[], idx = 0):
        operand_types = self.arch_template.keys()

        if idx > self.get_number_of_operands():
            return permutations
        elif idx == 0:
            init_permutation = [I386Mutator(self.opcode)]
            return self.phase2(init_permutation, idx+1)
        else:
            new_permutation = []
            for inst in permutations:
                for operand in operand_types:
                    new_inst = inst.copy()
                    new_inst.add_operand(I386Operand(operand))
                    new_permutation.append(new_inst)
            return self.phase2(new_permutation, idx+1)

    # permute_operand_size
    def phase3(self):
        operand_sizes = ['BYTE', 'WORD', 'DWORD', 'QWORD', 'XMMWORD', 'YMMWORD', 'ZMMWORD', 'TBYTE']
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




