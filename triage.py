import multiprocessing
import glob
import random
import os
import pickle
import argparse
import time
import signal
from collections import namedtuple
from AsFuzzer.normalizer import GasAsm, MasmAsm
from AsFuzzer.normalizer import  BinDump
from arch import intel, arm, mips
from AsInferrer.config import get_assembler




def retrieve_logs(target_path, tool, opdict):
    for srcfile in glob.glob(target_path):
        opcode = srcfile.split('/')[-1].split('_')[-1][:-2]
        if opcode not in opdict:
            opdict[opcode] = []
        opdict[opcode].append(srcfile)

    return opdict

def print_opdict(opdict):

    for opcode in sorted(opdict):
        print('%s'%(opcode))
        for inst in sorted(set(opdict[opcode])):
            print('\t%s'%(inst))

def write_code(arch, assembler, lines, workdir):
    filename = workdir + '/src.s'
    if assembler in ['masm']:
        with open(filename, 'w') as f:
            if arch in ['x86']:
                f.write('.model flat\n.code\n')
            elif arch in ['x86-64']:
                f.write('.code\n')
            elif arch in ['arm', 'aarch64']:
                f.write('code\n')

            for line in lines:
                f.write(line + '\n')

            if arch in ['x86', 'x86-64']:
                f.write('end\n')
    else:
        with open(filename, 'w') as f:
            if arch in ['x86', 'x86-64']:
                f.write('.intel_syntax noprefix\n')
            for line in lines:
                f.write(line + '\n')
    return filename

def compile_code(arch, assembler, srcfile, log='/dev/null'):
    if srcfile.endswith('.asm'):
        output = srcfile[:-4] + '.o'
    else:
        output = srcfile[:-2] + '.o'
    if assembler in ['masm']:
        cmd = '%s /Fo %s /c %s 2> %s >&2'%(get_assembler(arch, assembler), output, srcfile, log)
    elif assembler in ['gas']:
        cmd = '%s -o %s %s 2> %s >&2'%(get_assembler(arch, assembler), output, srcfile, log)
    else:
        cmd = '%s -o %s -c %s 2> %s >&2'%(get_assembler(arch, assembler), output, srcfile, log)
    os.system(cmd)
    return output

def make_dump(arch, assembler, output, workdir):
    dump = workdir + '/dump.txt'
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

    os.system(cmd)
    return dump

def make_diff(instfile, dumpfile, workdir):
    difffile = f'{workdir}/diff.txt'
    os.system(f'sdiff {instfile} {dumpfile} > {difffile}')
    return difffile


def make_files(arch, tool, workdir, opcode, opdict, opdir):
    lines = []
    if not os.path.exists(opdir):
        os.makedirs(opdir)
    for asmfile in opdict[opcode]:
        with open(asmfile) as fd:
            lines.extend([line for line in fd.read().split('\n') if opcode in line])
    with open(f'{opdir}/insts.txt', 'w') as fd:
        for line in sorted(set(lines)):
            fd.write(line + '\n')
    srcfile = write_code(arch, tool, sorted(set(lines)), opdir)
    objfile = compile_code(arch, tool, srcfile)
    if os.path.exists(objfile):
        dumpfile = make_dump(arch, tool, objfile, opdir)
    else:
        dumpfile = ''

    return srcfile, objfile, dumpfile


def make_triage(arch, tool, opdict):
    workdir = f'triage/{arch}/{tool}/'

    for opcode in opdict:
        opdir = f'{workdir}/{opcode}'
        srcfile, objfile, dumpfile = make_files(arch, tool, workdir, opcode, opdict, opdir)
        if dumpfile:
            difffile = make_diff(f'{opdir}/insts.txt', dumpfile, opdir)


def make_triage_two(arch, tool1, tool2, opdict):
    uname = f'{tool1}_{tool2}'
    workdir1 = f'triage/{arch}/{uname}/{tool1}'
    workdir2 = f'triage/{arch}/{uname}/{tool2}'

    for opcode in opdict:
        opdir1 = f'{workdir1}/{opcode}'
        _, _, dumpfile1 = make_files(arch, tool1, workdir1, opcode, opdict, opdir1)
        opdir2 = f'{workdir2}/{opcode}'
        _, _, dumpfile2 = make_files(arch, tool2, workdir2, opcode, opdict, opdir2)
        if dumpfile1 and  dumpfile2:
            difffile = make_diff(dumpfile1, dumpfile2, opdir1)
            difffile = make_diff(dumpfile1, dumpfile2, opdir2)


def report_summary(arch):

    for tool in ['clang', 'gas', 'icc', 'masm']:
        opdict = dict()
        opdict = retrieve_logs(f'diff/{arch}/diff/{tool}/bindiff/*.s', tool, opdict)

        print('[%s] %d'%(tool, len(opdict)))
        make_triage(arch, tool, opdict)


    for tool1 in ['clang', 'gas', 'icc', 'masm']:
        for tool2 in ['clang', 'gas', 'icc', 'masm']:
            if tool1 == tool2: continue
            if tool1 > tool2: continue

            opdict = dict()

            uname = '_'.join(sorted([tool1, tool2]))

            opdict = retrieve_logs(f'diff/{arch}/same/{uname}/{tool1}/bindiff/*.s', tool, opdict)

            print('[%s vs. %s] %d'%(tool1, tool2, len(opdict)))
            make_triage_two(arch, tool1, tool2, opdict)



def multi(arch, core):
    opcode = []
    if arch in ['x86', 'x86-64']:
        opcode = intel.OPCODE
    elif arch in ['arm', 'aarch64']:
        opcode = arm.OPCODE
    elif arch in ['mips']:
        opcode = mips.OPCODE

    print(len(opcode))
    p = multiprocessing.Pool(core)
    p.map(run, [(arch, op) for op in opcode])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AsFuzz_diff_test')
    parser.add_argument('arch', type=str)

    args = parser.parse_args()
    report_summary(args.arch)
