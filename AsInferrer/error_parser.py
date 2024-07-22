def filter_error(asm_code, blacklist):
    new_asm = []
    for asm in asm_code:
        valid = True
        if not asm.is_valid():
            continue
        for log in asm.get_log():
            for keyword in blacklist:
                if keyword in log:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            new_asm.append(asm)
    return new_asm

def get_blacklist(arch, phase, assembler):
    if assembler in ['masm']:
        blacklist= ['syntax error']

        if phase >= 2:
            blacklist.extend(['coprocessor register cannot be first operand',
                              'immediate operand not allowed', 'memory operand not allowed',
                              'register cannot be', 'jump destination must specify a label',
                              'instruction does not allow NEAR indirect addressing'])

        if phase >= 3:
            blacklist.extend(['invalid operand size', 'instruction operands must be the same size',
                              'invalid instruction operands' ])
        return blacklist

    elif assembler in ['icc']:
        blacklist=['unsupported instruction', 'is not supported in 64-bit mode',
                    'invalid character', 'no such instruction', 'number of operands mismatch']
        if phase >= 2:
            blacklist.extend(['operand type mismatch', 'register type mismatch',
                              "default mask isn't allowed for", 'invalid VSIB address',
                              'immediate operands are allowed', 'too many memory references'])
        if phase >= 3:
            blacklist.extend(['operand size mismatch', "can't determine immediate size",
                              'ambiguous operand size', 'invalid instruction suffix for', 'incorrect register',
                              'not allowed with', 'broadcast is needed for operand of such type for',
                              'conflicting operand size modifiers' ])
        return blacklist

    elif assembler in ['gas']:
        blacklist=[ 'unsupported instruction', 'no such instruction',
                        'Internal error', 'invalid instruction suffix',
                        'invalid character', 'number of operands mismatch']

        if arch == 'x86-64':
            blacklist.extend(['is not supported in 64-bit mode'])
        if arch == 'arm':
            blacklist.extend(['bad instruction', 'junk at end of line', 'ARM register expected',
                              'use is obsoleted for'])
        if arch == 'thumb':
            blacklist.extend(['bad instruction', 'junk at end of line', 'ARM register expected',
                              'use is obsoleted for'])
        if arch == 'mips':
            blacklist.extend(['not supported on this processor', 'bad expression',
                              'opcode not supported on this processor: mips1'])
        if arch == 'aarch64':
            blacklist.extend(['must be an SVE vector register', "expected '{' at operand 1"])

        if arch == 'riscv':
            blacklist.extend(['internal: unreachable INSN_CLASS_', 'unrecognized opcode'])

            if phase >= 2:
                blacklist.extend(['illegal operands', 'unknown CSR', 'requires absolute expression'])


        if phase >= 2:
            blacklist.extend(['operand type mismatch', 'register type mismatch', 'too many memory references',\
                                'can\'t use register', 'at most 2 immediate operands are allowed', 'cannot represent'])

        if phase >= 3:
            blacklist.extend(['operand size mismatch','ambiguous memory operand size', 'ambiguous operand size'])

        return blacklist
    elif assembler in ['clang']:
        blacklist = ['number of operands mismatch', 'not supported']
        if phase >= 2:
            blacklist.extend(['invalid operand for instruction', 'unknown token in expression',
                              'operand type mistmatch', 'destination and source registers', 'invalid instruction',
                                'unexpected token'])
        if phase >= 3:
            blacklist.extend(['operand size mismatch'])
        if phase >= 4:
            blacklist.extend(["missing `lock'", 'expecting', 'not a valid'])

        if arch == 'mips':
            blacklist.extend(['opcode not supported', 'invalid operands', 'must be an', 'too few operands'])
            if phase >= 2:
                blacklist.extend(['expected'])
        if arch == 'riscv':
            blacklist.extend(['too few operands'])
            if phase >= 2:
                blacklist.extend(['operand must be', 'for operand modifier', 'invalid operand', 'expected \''])
        return blacklist
    raise NotImplementedError

