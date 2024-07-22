from arch import intel, arm, mips, aarch64, riscv

def get_opcode(arch):
    if arch in ['x86', 'x86-64']:
        return intel.OPCODE
    elif arch in ['arm', 'thumb']:
        return arm.OPCODE
    elif arch == 'aarch64':
        return aarch64.OPCODE
    elif arch == 'mips':
        return mips.OPCODE
    elif arch == 'riscv':
        return riscv.OPCODE
    raise NotImplementedError

arch_template_map = {
    'x86-64':intel.TEMPLATE,
    'x86':intel.TEMPLATE_I386,
    'arm':arm.TEMPLATE,
    'thumb':arm.TEMPLATE,
    'aarch64':aarch64.TEMPLATE,
    'mips':mips.TEMPLATE,
    'riscv':riscv.TEMPLATE
}

def get_arch_template(arch):
    if arch not in arch_template_map.keys():
        raise NotImplementedError
    return arch_template_map[arch]
