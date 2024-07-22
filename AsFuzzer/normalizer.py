import argparse, multiprocessing
import re
from collections import namedtuple
import os
import subprocess
import glob
import arch.intel


from AsInferrer.config import get_assembler_cmd, get_assembler
from arch import intel, arm, aarch64, mips, riscv


class BinDump:
    def __init__(self, arch, opcode, dump, verbose=False):
        self.arch = arch
        self.verbose = verbose
        self.dump_list = []
        self.unknown = False
        self.err_lines = []
        self.err_asm_lines  = []
        self.err_line_num = []

        self.errors = []
        self.err_code = []

        for code in dump:
            inst = BinInst(arch, opcode, code)
            if inst.unknown:
                self.errors.append('unknown')
                self.unknown = True
            elif 'nop' in inst.line.split():
                continue
            elif '...' in inst.line.split():
                continue


            if inst.line:
                self.dump_list.append(inst)

    def dump_all(self, output):
        with open(output, 'w') as f:
            for disasm in self.dump_list:
                norm = disasm.get_normal_form()
                f.write(norm+'\n')

    def dump_asm_lines(self, output):
        with open(output, 'w') as f:
            for asm in self.err_asm_lines:
                f.write(str(asm)+'\n')


    def dump_lines(self, output):
        with open(output, 'w') as f:
            for disasm in self.err_lines:
                norm = disasm.get_normal_form()
                f.write(norm+'\n')

    def cmp_asm_code(self, asm_list, tool):
        if len(asm_list) != len(self.dump_list):
            self.errors.append('num_of_code')

        for idx in range(len(asm_list)):
            asm = asm_list[idx]
            if idx >= len(self.dump_list):
                continue
            disasm = self.dump_list[idx]
            a=str(asm)
            b=str(disasm)

            if len(asm.operands) > len(disasm.operands):
                pass
            elif len(asm.operands) < len(disasm.operands):
                pass
            else:
                bError = False
                norm = disasm.get_normal_form()
                for op_idx in range(len(asm.operands)):
                    op1 = disasm.normalize_operand(op_idx)
                    op2 = str(asm.operands[op_idx])
                    if 'IMM' in op1:
                        if op2.isdigit() or op2.startswith('0x'):
                            continue
                        elif re.findall('[0-9]<<[0-9]', op2):
                            continue
                        elif op2.startswith('#') and op2[1:].isdigit():
                            continue
                    elif op1.startswith('zero,'):
                        continue

                    self.errors.append('type_mismatch')
                    bError = True

                    if self.verbose:
                        print('[%5s]  %30s   |   %30s'%(tool, a, b))

                if bError:
                    self.err_lines.append(disasm)
                    self.err_asm_lines.append(asm)
                    self.err_line_num.append(idx)

    def check_size_mismatch(self, operand1, operand2):
        if ' PTR ' in operand1:
            if ' PTR ' not in operand2:
                return True
            elif operand1.split()[0] != operand2.split()[0]:
                return True
        return False
    def cmp_dump_code(self, other):
        if len(self.dump_list) != len(other.dump_list):
            self.errors.append('num_of_code')
            other.errors.append('num_of_code')

        for idx1, disasm1 in enumerate(self.dump_list):
            errors = []
            if idx1 >= len(other.dump_list):
                return

            disasm2 = other.dump_list[idx1]

            bBug = False
            if len(disasm1.operands) != len(disasm2.operands):
                errors.append('num_of_operands')
                other.errors.append('num_of_operands')
                bBug = True
            else:
                for op_idx, operand1 in enumerate(disasm1.operands):
                    operand2 = disasm2.operands[op_idx]
                    if self.check_size_mismatch(operand1, operand2):
                        errors.append('size_mismatch')
                        bBug = True
                    elif self.check_size_mismatch(operand2, operand1):
                        errors.append('size_mismatch')
                        bBug = True
                    elif operand1 != operand2:
                        errors.append('type_mismatch')
                        other.errors.append('type_mismatch')
                        bBug = True
            self.err_code.append(self.get_err_code(errors))
            if bBug:
                self.errors.extend(errors)
                self.err_lines.append(disasm1)
                other.err_lines.append(disasm2)
                self.err_line_num.append(idx1)

    def get_err_code(self, errors):
        if 'num_of_code' in errors:
            return 1
        elif 'num_of_operands' in errors:
            return 2
        elif 'type_mismatch' in errors and 'size_mismatch' in errors:
            return 3
        elif 'type_mismatch' in errors:
            return 4
        elif 'size_mismatch' in errors:
            return 5
        return 0

    def has_bugs(self):
        return len(self.errors) > 0





class GasAsm:
    def __init__(self, arch, assembler):
        self.arch = arch
        self.assembler = assembler
        self.asm = ''

    def write_code(self, lines, filename):
        with open(filename, 'w') as f:
            if self.arch in ['x86', 'x86-64']:
                f.write('.intel_syntax noprefix\n')

            for line in lines:
                f.write('\t' + str(line) + '\n')
        self.asm = filename

    def compile(self, output, log='/dev/null'):

        if self.assembler in ['clang']:
            cmd = '%s -c %s -o %s > %s 2>&1'%(get_assembler(self.arch, self.assembler), self.asm, output, log)
        elif self.assembler in ['icc']:
            cmd = '%s -c %s -o %s -diag-disable=10441 > %s 2>&1'%(get_assembler(self.arch, self.assembler), self.asm, output, log)
        else:
            cmd = '%s %s -o %s > %s 2>&1'%(get_assembler(self.arch, self.assembler), self.asm, output, log)
        os.system(cmd)


    def compile_cmd(self, output):
        if self.assembler in ['clang']:
            cmd = '%s -c %s -o %s'%(get_assembler(self.arch, self.assembler), self.asm, output)
        elif self.assembler in ['icc']:
            cmd = '%s -c %s -o %s -diag-disable=10441'%(get_assembler(self.arch, self.assembler), self.asm, output)
        else:
            cmd = '%s %s -o %s'%(get_assembler(self.arch, self.assembler), self.asm, output)
        return cmd

    def get_dump(self, output, dump):
        if self.arch in ['x86'] and self.assembler in ['masm']:
            cmd = 'bin/objdump -d -M intel --no-show-raw-insn --target coff-i386 ' + output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
        elif self.arch in ['x86', 'x86-64']:
            cmd = 'bin/objdump -d -M intel --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
        elif self.arch in ['arm']:
            cmd = 'bin/arm-linux-gnueabi-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
        elif self.arch in ['aarch64']:
            cmd = 'bin/aarch64-linux-gnu-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
        elif self.arch in ['mips']:
            cmd = 'bin/mips-linux-gnu-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
        elif self.arch in ['riscv']:
            cmd = 'bin/riscv-linux-gnu-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
        else:
            cmd = ''

        os.system(cmd)
        if os.path.exists(dump):
            with open(dump, 'r') as f:
                return f.read().split('\n')
        return []




class MasmAsm(GasAsm):

    def write_code(self, lines, filename):
        filename = filename[:-2] + '.asm'
        with open(filename, 'w') as f:
            if self.arch in ['x86']:
                f.write('.model flat\n.code\n')
            elif self.arch in ['x86-64']:
                f.write('.code\n')
            elif self.arch in ['arm', 'aarch64']:
                f.write('code\n')

            for line in lines:
                f.write('\t' + str(line) + '\n')

            if self.arch in ['x86', 'x86-64']:
                f.write('end\n')
            elif self.arch in ['arm', 'aarch64']:
                f.write('\tend\n')

            self.asm = filename


    def compile_cmd(self, output):
        if self.assembler in ['masm']:
            cmd = '%s /Fo %s /c %s 2> /dev/null >&2'%(get_assembler(self.arch, self.assembler), output, self.asm)
        if self.assembler in ['gas']:
            cmd = '%s -o %s %s 2> /dev/null >&2' % (get_assembler(self.arch, self.assembler), output, self.asm)
        else:
            cmd = '%s -o %s -c %s 2> /dev/null >&2' % (get_assembler(self.arch, self.assembler), output, self.asm)
        return cmd

    def compile(self, output, log='/dev/null'):
        if self.assembler in ['masm']:
            cmd = '%s /Fo %s /c %s 2> %s >&2'%(get_assembler(self.arch, self.assembler), output, self.asm, log)
        if self.assembler in ['gas']:
            cmd = '%s -o %s %s 2> %s >&2'%(get_assembler(self.arch, self.assembler), output, self.asm, log)
        else:
            cmd = '%s -o %s -c %s 2> %s >&2'%(get_assembler(self.arch, self.assembler), output, self.asm, log)
        os.system(cmd)


def execute(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return p.returncode, p.stdout, p.stderr

def execute_list(cmd_list):
    for cmd in cmd_list:
        os.system(cmd)


def get_assembly_cmd(arch, assembler, lines, output):
    if assembler in ['masm']:
        tool = MasmAsm(arch, assembler)
    else:
        tool = GasAsm(arch, assembler)
    tool.write_code(lines, output[:-2] + '.s')
    cmd = tool.compile_cmd(output)
    return cmd


def get_diff_test_cmd_list(arch, assembler):
    folder = f'asfuzzer_data/{assembler}/{arch}/final'
    db_folder = f'db/{arch}/{assembler}'
    cmd_list = []

    for asm in glob.glob('%s/*.s' % (folder)):
        filename = os.path.basename(asm)
        db_file = '%s/%s.s'%(db_folder, os.path.splitext(filename)[0])
        cmd = 'cat %s | grep -v intel_syntax | sort -u > %s '%(asm, db_file)
        cmd_list.append(cmd)

    return cmd_list


def get_dump_cmd(arch, assembler, output, dump):
    if arch in ['x86'] and assembler in ['masm']:
        cmd = 'bin/objdump -d -M intel --no-show-raw-insn --target coff-i386 '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    elif arch in ['x86', 'x86-64']:
        cmd = 'bin/objdump -d -M intel --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    else:
        cmd = 'bin/arm-linux-gnueabi-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    return cmd

def get_diff_cmd(output1, output2, diff):
    cmd = 'diff %s %s > %s'%(output1, output2, diff)
    return [cmd]



def create_db(arch, assembler, cores):

    cmd_list = get_diff_test_cmd_list(arch, assembler)

    p = multiprocessing.Pool(cores)
    p.map(execute, cmd_list)


class Inst:
    def __init__(self, arch, opcode, line):
        self.arch = arch
        self.line = line
        self.opcode = line.split()[0]
        operands = ' '.join(line.split()[1:])
        for idx, item in enumerate(line.split()):
            if item == opcode:
                if idx > 0:
                    self.opcode = ' '.join(line.split()[:idx+1])
                    operands = ' '.join(line.split()[idx+1:])
                    break

        self.operands = operands.split(', ')
        self.template = self.get_template()

    def __str__(self):
        return self.line

    def get_template(self):
        if self.arch in ['x86']:
            return intel.TEMPLATE_I386
        elif self.arch in ['x86-64']:
            return intel.TEMPLATE
        elif self.arch in ['arm']:
            return arm.TEMPLATE
        elif self.arch in ['aarch64']:
            return aarch64.TEMPLATE
        elif self.arch in ['mips']:
            return mips.TEMPLATE
        elif self.arch in ['riscv']:
            return riscv.TEMPLATE

    def get_type(self, expr):
        for key, val in self.template.items():
            for item in val[3]:
                if expr == item:
                    return key
        return 'unknown'
    def get_normalize_form(self):
        operand_type = []
        for operand in self.operands:
            if ' PTR ' in operand:
                word_size = ' '.join(operand.split()[:2])
                operand = ' '.join(operand.split()[2:])
                type = word_size + ' ' + self.get_type(operand)
            else:
                type = self.get_type(operand)
            operand_type.append(type)
        return self.opcode + ' ' + (', '.join(operand_type))

class BinInst(Inst):
    def __init__(self, arch, opcode, line):
        self.line = ''
        self.opcode = ''
        self.operands = []
        self.unknown = False
        if line:
            if ', #' not in line:
                line = line.split('#')[0]

            line = ':'.join(line.split(':')[1:])
            if '<unknown>' in line:
                self.unknown = True
            line = line.split('<.')[0]
            if line:
                super().__init__(arch, opcode, line)

    def normalize_operand(self, idx):
        arg = self.operands[idx]
        expr = re.findall('\[(.*)\]',arg)
        if expr:
            size = ''
            if ' ptr ' in arg:
                size = arg.split('[')[0]
                size = ' '.join(size.split()[:2])
            terms = re.split('\+|-', expr[0])

            for term in terms:
                if term.isdigit() or term.startswith('0x'):
                    continue
                expr[0] = expr[0].replace(term, term.upper())

            if size:
                return size.upper() + ' ['+expr[0]+']'
            return '['+expr[0]+']'
        elif arg.isdigit() or arg.startswith('0x'):
            return 'IMM'
        elif arg.startswith('#') and arg[1:].isdigit():
            return 'IMM'

        if self.arch in ['x86', 'x86-64']:
            if arg.upper() in arch.intel.REGISTERS:
                return arg.upper()
        elif self.arch in ['arm']:
            if arg.upper() in arch.arm.REGISTERS:
                return arg.upper()
        elif self.arch in ['aarch64']:
            if arg.upper() in arch.aarch64.REGISTERS:
                return arg.upper()
        elif self.arch in ['riscv']:
            if arg.upper() in arch.riscv.REGISTERS:
                return arg.upper()
        elif self.arch in ['mips']:
            if arg.upper() in arch.mips.REGISTERS:
                return arg.upper()

        return arg

    def get_normal_form(self):
        oper_list = []
        for op_idx in range(len(self.operands)):
            operand = self.normalize_operand(op_idx)
            oper_list.append(operand)
        if oper_list:
            norm = self.opcode + ' ' + ', '.join(oper_list)
        else:
            norm = self.opcode
        return norm

    def __str__(self):
        line = ' '.join(self.line.split())
        exprs = re.findall('\[(.*)\]',line)
        for expr in exprs:
            new_expr = ''.join(expr.split())
            line = line.replace(expr, new_expr)
        return line

class Normalizer:
    def __init__(self, arch, assembler, filename):
        self.arch = arch
        self.assembler = assembler
        self.code = []
        self.filename = filename
        with open(filename) as f:
            lines = f.read().split('\n')
            self.code = self.read_code(lines)

    def read_code(self, lines):
        code = []
        for line in lines:
            if line in ['.model flat', '.code', 'end', '.intel_syntax noprefix', '.thumb']:
                continue
            if not line: continue

            inst = Inst(line)
            code.append(inst)
        return code


class BinNormalizer(Normalizer):
    def read_code(self, lines):
        code = []
        for line in lines:
            if not line: continue

            line = ':'.join(line.split(':')[1:])
            line = line.split('<.')[0]
            if not line: continue

            inst = Inst(line)
            code.append(inst)
        return code


def compare(asm1, asm2):
    if len(asm1.code) != len(asm2.code):
        print('the number of code diff')

    for idx in range(len(asm1.code)):
        if asm1.code[idx].opcode != asm2.code[idx].opcode:
            print('opcode diff')
            return
        if len(asm1.code[idx].operands) != len(asm2.code[idx].operands):
            print('the number of operand diff')
        for idx2 in range(len(asm1.code[idx].operands)):
            if asm1.code[idx].operands[idx2] != asm2.code[idx].operands[idx2] :
                print('operand str diff')
                break

        print('same')

def opcode_filter(asm1, asm2):
    code_cnt1 = len(asm1.code)
    code_cnt2 = len(asm2.code)
    if code_cnt1 != code_cnt2:
        if code_cnt2 == 0:
            pass
        elif code_cnt1 * 2 == code_cnt2:
            if asm1.code[0].opcode == asm2.code[0].opcode:
                if '<unknown>' in asm2.code[1].line:
                    print('Bug: ', asm1.filename)
                elif asm1.code[0].opcode == asm2.code[1].opcode:
                    print('Bug: ', asm1.filename)
        else:
            pass
        return []

    matched_code = []
    for idx in range(code_cnt1):
        if asm1.code[idx].opcode != asm2.code[idx].opcode:
            continue
        matched_code.append(asm1.code[idx].line)
    return matched_code

def single_run(arch, tool, asm):
    if asm.endswith('.s'):
        asm1 = Normalizer(arch, tool, asm)
        asm2 = BinNormalizer(arch, tool, asm[:-2]+'.txt')
        valid_code = opcode_filter(asm1, asm2)

    else:
        BinNormalizer(arch, tool, asm)
        return



def parse_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            inst = BinInst('', line)
            norm = inst.get_normal_form()
            print(norm)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AsFuzz_diff_test')
    parser.add_argument('filename', type=str)

    args = parser.parse_args()

    parse_file(args.filename)
