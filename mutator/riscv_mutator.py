from arch import riscv
from mutator.operand import ArgSize, ArgType, Operand
from mutator.base_mutator import BaseMutator


class RiscvOperand(Operand):
    arch_registers = riscv.REGISTERS
    arch_template = riscv.TEMPLATE

    def __init__(self, expression, is_template=True):
        super().__init__(expression)

    def get_size(self):
        return ArgSize.DWORD # currently no size perm

    def get_normalized_operand(self):
        expr = self._expression
        # if expr is template, then print representative value
        if self._is_template:
            if expr == 'IMM':
                expr = 'IMM'
            elif expr == 'MEMB': # mem_base
                expr = '(REG)'
            elif expr == 'MEMBD': # mem_base_disp
                expr = 'IMM(REG)'
            elif expr == 'MEMD': # mem_disp
                expr = '(IMM)'
            else:
                tpl_elem = self.arch_template[expr][2]
                expr = tpl_elem[0]
        if self._directive:
            return '%s %s'%(self._directive, expr)
        return expr


class RiscvMutator(BaseMutator):
    arch_template = riscv.TEMPLATE

    def __init__(self, opcode, operands=None, prefix=''):
        super().__init__(opcode, operands, prefix=prefix)

    def copy(self):
        new_operands = [RiscvOperand(operand.get_template()) for operand in self.operands]
        return RiscvMutator(self.opcode, new_operands, self.prefix)

    def phase1(self):
        #gp_registers = ['x0', 'x1', 'x2', 'x3']
        gp_registers = ['a0', 'a1', 'a2', 'a3']

        ret = [RiscvMutator(self.opcode)]
        for num_of_op in range(1, 5):
            ops = [RiscvOperand('REG64') for idx in range(num_of_op)]
            ret.append(RiscvMutator(self.opcode, ops))

        return ret

    def phase2(self, permutations=[], idx = 0):
        operand_types = self.arch_template.keys()

        if idx > self.get_number_of_operands():
            return permutations
        elif idx == 0:
            init_permutation = [RiscvMutator(self.opcode)]
            return self.phase2(init_permutation, idx+1)
        else:
            new_permutation = []
            for inst in permutations:
                for operand in operand_types:
                    new_inst = inst.copy()
                    new_inst.add_operand(RiscvOperand(operand))
                    new_permutation.append(new_inst)
            return self.phase2(new_permutation, idx+1)

    def phase3(self):
        return []

    def phase4(self):
        return []


