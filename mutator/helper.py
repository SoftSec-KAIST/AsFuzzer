
from mutator.arm_mutator import ArmMutator
from mutator.intel_mutator import IntelMutator
from mutator.i386_mutator import I386Mutator
from mutator.mips_mutator import MipsMutator
from mutator.aarch64_mutator import AArch64Mutator
from mutator.riscv_mutator import RiscvMutator

mutator_dic = {
    'arm' : ArmMutator,
    'thumb' : ArmMutator,
    'aarch64' : AArch64Mutator,
    'mips' : MipsMutator,
    'x86-64' : IntelMutator,
    'x86' : I386Mutator,
    'riscv' : RiscvMutator
}


def get_mutator(arch):
    if arch not in mutator_dic.keys():
        raise NotImplementedError
    return mutator_dic[arch]

def get_asm_head_tail(arch, target):
    header, tail = '', ''
    if target in ['masm']:
        if arch in ['x86']:
            header = '.model flat\n.code'
            tail = 'end'
        elif arch in ['x86-64']:
            header = '.code'
            tail = 'end'
        elif arch in ['arm', 'aarch64']:
            header = 'code'
            tail = '\tend'
    else:
        if arch in ['x86', 'x86-64']:
            header = '.intel_syntax noprefix'
        elif arch == 'thumb':
            header = '.thumb'
    return header, tail
