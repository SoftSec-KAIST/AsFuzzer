# using utils/parse_arm.py
OPCODE = ['abs', 'adc', 'adclt', 'adcs', 'add', 'addpl', 'adds', 'addspl',
'adr', 'adrp', 'and', 'ands', 'asr', 'autia1716', 'autiasp', 'autiaz',
'autib1716', 'autibsp', 'autibz', 'b', 'bcc', 'bcs', 'beq', 'bfc', 'bfi',
'bfxil', 'bge', 'bgt', 'bhi', 'bic', 'bics', 'bl', 'ble', 'blr', 'bls', 'blt',
'bmi', 'bne', 'bpl', 'br', 'brk', 'bti', 'bvc', 'bvs', 'cbnz', 'cbz',
'clearbhb', 'clrex', 'cls', 'clz', 'cmeq', 'cmge', 'cmgt', 'cmhi', 'cmhs',
'cmn', 'cmp', 'cmpeq', 'cmpge', 'cmpgt', 'cmphi', 'cmple', 'cmpls', 'cmplt',
'cmpne', 'cmtst', 'crc32b', 'crc32cb', 'crc32ch', 'crc32cw', 'crc32h',
'crc32w', 'csdb', 'dcps1', 'dcps2', 'dcps3', 'dfb', 'dmb', 'drps', 'dsb',
'eon', 'eor', 'eors', 'eret', 'esb', 'fabd', 'fabs', 'facge', 'facgt', 'fadd',
'fcmeq', 'fcmge', 'fcmgt', 'fcmp', 'fcmpe', 'fcvt', 'fcvtas', 'fcvtau',
'fcvtms', 'fcvtmu', 'fcvtns', 'fcvtnu', 'fcvtps', 'fcvtpu', 'fcvtxn', 'fcvtzs',
'fcvtzu', 'fdiv', 'fmadd', 'fmax', 'fmaxnm', 'fmin', 'fminnm', 'fmov', 'fmsub',
'fmul', 'fmulx', 'fneg', 'fnmadd', 'fnmsub', 'fnmul', 'frecpe', 'frecps',
'frecpx', 'frinta', 'frinti', 'frintm', 'frintn', 'frintp', 'frintx', 'frintz',
'frsqrte', 'frsqrts', 'fsqrt', 'fsub', 'hlt', 'hvc', 'isb', 'ldar', 'ldarb',
'ldarh', 'ldaxp', 'ldaxr', 'ldaxrb', 'ldaxrh', 'ldnp', 'ldr', 'ldrb', 'ldrh',
'ldrsb', 'ldrsh', 'ldrsw', 'ldtr', 'ldtrb', 'ldtrh', 'ldtrsb', 'ldtrsh',
'ldtrsw', 'ldur', 'ldurb', 'ldurh', 'ldursb', 'ldursh', 'ldursw', 'ldxp',
'ldxr', 'ldxrb', 'ldxrh', 'lsl', 'lsr', 'madd', 'mla', 'mls', 'mneg', 'mov',
'movk', 'movs', 'movt', 'msub', 'mul', 'mvn', 'neg', 'negs', 'ngc', 'ngcs',
'nop', 'orn', 'orr', 'orrs', 'pacia1716', 'paciasp', 'paciaz', 'pacib1716',
'pacibsp', 'pacibz', 'prfm', 'prfum', 'pssbb', 'rbit', 'ret', 'rev', 'rev16',
'rev32', 'ror', 'rprfm', 'sb', 'sbc', 'sbclt', 'sbcs', 'sbfiz', 'sbfx',
'scvtf', 'sdiv', 'sel', 'sev', 'sevl', 'shl', 'sli', 'smaddl', 'smc', 'smlal',
'smmla', 'smnegl', 'smsubl', 'smulh', 'smull', 'sqabs', 'sqadd', 'sqdmlal',
'sqdmlsl', 'sqdmulh', 'sqdmull', 'sqneg', 'sqrdmulh', 'sqrshl', 'sqrshrn',
'sqrshrun', 'sqshl', 'sqshlu', 'sqshrn', 'sqshrun', 'sqsub', 'sqxtn', 'sqxtun',
'sri', 'srshl', 'srshr', 'srsra', 'ssbb', 'sshl', 'sshr', 'ssra', 'stlr',
'stlrb', 'stlrh', 'stnp', 'stp', 'str', 'strb', 'strh', 'sttr', 'sttrb',
'sttrh', 'stur', 'sturb', 'sturh', 'sub', 'subs', 'suqadd', 'svc', 'sxtb',
'sxth', 'sxtw', 'tbnz', 'tbz', 'tst', 'ubfiz', 'ubfx', 'ucvtf', 'udf', 'udiv',
'umaddl', 'umlal', 'umnegl', 'umsubl', 'umulh', 'umull', 'uqadd', 'uqrshl',
'uqrshrn', 'uqshl', 'uqshrn', 'uqsub', 'uqxtn', 'urshl', 'urshr', 'ursra',
'ushl', 'ushr', 'usqadd', 'usra', 'uxtb', 'uxth', 'wfe', 'wfi', 'xpaclri',
'yield']




REGISTERS = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10',
'R11', 'R12', 'R13', 'R14', 'R15', 'SP', 'FP', 'LR', 'IP']
# currently FP regs, IP, status register not included

PREFIX = [':lower16:', ':lower16:']

candidates = ['R0', '[R0]', '%R0', '#1','#-1', '=1']
#candidates = ['AX', 'EAX', 'RAX', '[RAX]', 'XMM0', 'MMX0', 'YMM0', '1', '[1]']
#candidates_att = ['%AX', '%EAX', '%RAX', '[%RAX]', '%XMM0', '%MMX0', '%YMM0', '$1', '[1]']
#pseudo_prefix = ['{disp8}', '{disp32}', '{evex}', '{load}', '{store}', '{vex2}', '{vex3}']

TEMPLATE = {
    'REG32' : (1, 32, ['R0'],
            ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11',
             'SP', 'FP', 'LR', 'IP']),
    'FP16' : (1, 16, ['H0'],
            ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15',
             'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 'H31']),
    'FP32' : (1, 32, ['S0'],
            ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15',
             'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22', 'S23', 'S24', 'S25', 'S26', 'S27', 'S28', 'S29', 'S30', 'S31']),
    'FP64' : (1, 64, ['D0'],
            ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15',
             'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31']),
    'MEMB' : (2, 0, ['[R0]'], # it may introduce many false positives, since [] could be same as ()
            ['[R0]', '[R1]', '[R2]', '[R3]', '[R4]', '[R5]', '[R6]', '[R7]', '[R8]', '[R9]', '[R10]', '[R11]']),
    'MEMBD' : (2, 0, ['[R0,#1]'],
            ['[R0,#1]', '[R1,#1]', '[R2,#1]', '[R3,#1]', '[R4,#1]', '[R5,#1]', '[R6,#1]', '[R7,#1]', '[R8,#1]', '[R9,#1]', '[R10,#1]', '[R11,#1]']),
    'MEMD' : (2, 0, ['[1]'],
            ['[1]','[2]','[3]','[4]','[5]','[6]','[7]','[8]']),
    'IMM' : (3, 0, ['#1'],
            #['#1']), # gas accepts immediate without sharp but it's feature
            ['#1','#2','#3','#4','#5','#6','#7','#8']),
    # 'LABELEXPR' : (3, 0,
    #         ['=1']),
    'SHIFT' : (3, 0, ['1<<4'],
            ['1<<4'])
}
