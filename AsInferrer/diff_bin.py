import argparse, multiprocessing
from collections import namedtuple
import os
import subprocess
import glob

from AsInferrer.config import get_assembler_cmd, get_assembler

class GasAsm:
    def __init__(self, arch, assembler):
        self.arch = arch
        self.assembler = assembler
        self.asm = ''

    def write_code(self, lines, filename):
        with open(filename, 'w') as f:
            if arch in ['x86','x86-64']:
                f.write('.intel_syntax noprefix\n')

            for line in lines:
                f.write(line + '\n')
        self.asm = filename

    def compile_cmd(self, output):
        if self.assembler in ['clang', 'icc']:
            cmd = '%s -c %s -o %s'%(get_assembler(self.arch, self.assembler), self.asm, output)
        else:
            cmd = '%s %s -o %s'%(get_assembler(self.arch, self.assembler), self.asm, output)
        return cmd


class MasmAsm(GasAsm):

    def write_code(self, lines, filename):
        filename = filename[:-2] + '.asm'
        with open(filename, 'w') as f:
            if arch in ['x86']:
                f.write('.model flat\n.code\n')
            elif arch in ['x86-64']:
                f.write('.code\n')
            elif arch in ['arm', 'aarch64']:
                f.write('code\n')

            for line in lines:
                f.write('\t' + line + '\n')

            if arch in ['x86', 'x86-64']:
                f.write('end\n')
            elif arch in ['arm', 'aarch64']:
                f.write('\tend\n')
            self.asm = filename


    def compile_cmd(self, output):
        cmd = '%s /Fo %s /c %s'%(get_assembler(self.arch, self.assembler), output, self.asm)
        return cmd

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
    print(cmd)
    return cmd


def create_db_cmd(arch, assembler):
    folder = f'asfuzzer_data/{assembler}/{arch}/final'
    db_folder = f'db/{arch}/{assembler}/asm'
    cmd_list = []

    #execute('mkdir -p %s/'%(db_folder))

    for asm in glob.glob('%s/*.s' % (folder)):
        filename = os.path.basename(asm)
        db_file = '%s/%s.s'%(db_folder, os.path.splitext(filename)[0])
        cmd = 'cat %s | grep -v intel_syntax | sort -u > %s '%(asm, db_file)
        #print(cmd)
        cmd_list.append(cmd)

    return cmd_list

def update_db_cmd(arch, assembler):
    db_folder = f'db/{arch}/{assembler}/asm'
    bin_folder = f'db/{arch}/{assembler}/bin'
    cmd_list = []

    execute('mkdir -p %s/'%(bin_folder))

    for asm in glob.glob('%s/*.s' % (db_folder)):
        filename = os.path.basename(asm)
        output = '%s/%s.o'%(bin_folder, filename[:-2])
        dump = '%s/%s.txt'%(bin_folder, filename[:-2])

        cmd_list.append(get_dump_cmd(arch, assembler, output, dump))

    return cmd_list


def get_dump_cmd(arch, assembler, output, dump):
    if arch in ['x86'] and assembler in ['masm']:
        cmd = 'bin/objdump -d -M intel --no-show-raw-insn --target coff-i386 ' + output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    elif arch in ['x86', 'x86-64']:
        cmd = 'bin/objdump -d -M intel --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    elif arch in ['arm']:
        cmd = 'bin/arm-linux-gnueabi-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    elif arch in ['aarch64']:
        cmd = 'bin/aarch64-linux-gnu-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    elif arch in ['mips']:
        cmd = 'bin/mips-linux-gnu-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    elif arch in ['riscv']:
        cmd = 'bin/riscv-linux-gnu-objdump -d --no-show-raw-insn '+ output + " | grep '00000\s*<' -A1000 | grep -v '00000\s*<' > " + dump
    else:
        cmd = ''
    #print(cmd)
    return cmd

def get_diff_cmd(output1, output2, diff):
    cmd = 'diff %s %s > %s'%(output1, output2, diff)
    print(cmd)
    return [cmd]

def create_db(arch, assembler, cores):

    cmd_list = create_db_cmd(arch, assembler)

    p = multiprocessing.Pool(cores)
    p.map(execute, cmd_list)

def update_db(arch, assembler, cores):

    cmd_list = update_db_cmd(arch, assembler)

    p = multiprocessing.Pool(cores)
    p.map(execute, cmd_list)



def run(arch, assembler):
    gfolder = 'assfuzzer_data/%s/%s/final/'%(assembler, arch)

    for asm in glob.glob('%s/*.s'%(gfolder)):
        filename = os.path.basename(asm)
