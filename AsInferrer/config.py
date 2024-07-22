import os

bin_path = 'bin'

as_cmd = {
    'x86-64' : 'as',
    'x86' : 'as --32',
    'arm' : 'arm-linux-gnueabi-as',
    'thumb' : 'arm-linux-gnueabi-as -mthumb -mthumb-interwork',
    'aarch64' : 'aarch64-linux-gnu-as',
    'mips' : 'mips-linux-gnu-as',
    'riscv': 'riscv-linux-gnu-as -march=rv64g'
}

clang_cmd = {
    'x86-64' : 'clang -c',
    'x86' : 'clang -c --target=i386',
    'arm' : 'clang -c --target=armv8-linux-eabi',
    'thumb' : 'clang -c --target=armv8-linux-eabi -mthumb',
    'aarch64' : 'clang -c --target=aarch64-linux-eabi',
    'mips' : 'clang -c --target=mips',
    'riscv' : 'clang -c --target=riscv64 -march=rv64g'
}

icc_cmd = {
    'x86-64' : 'icc64 -c',
    'x86' : 'icc32'
}
masm_cmd = {
    'x86-64' : 'masm64 /c',
    'x86' : 'masm32 /c',
}

def get_assembler(arch, target):
    if target == 'gas':
        return f'{bin_path}/{as_cmd[arch]}'
    elif target == 'clang':
        return f'{bin_path}/{clang_cmd[arch]}'
    elif target == 'icc':
        if arch in ['x86']:
            return f'./{bin_path}/{icc_cmd[arch]}'
        elif arch in ['x86-64']:
            return f'{bin_path}/{icc_cmd[arch]}'
        return ''
    elif target == 'masm':
        if arch in ['x86', 'x86-64']:
            if os.name in ['nt']:
                return f'.\{bin_path}\{masm_cmd[arch]}'
            else:
                return f'wine64 ./{bin_path}/{masm_cmd[arch]}'

        return ''

    raise NotImplementedError


def get_assembler_cmd(arch, target):
    if target in ['clang']:
        return get_assembler(arch, target) + ' --save-temps=/tmp/'
    elif target in ['icc']:
        return get_assembler(arch, target) + ' -diag-disable=10441'

    return get_assembler(arch, target)

def get_supported_archs():
    return as_cmd.keys()
