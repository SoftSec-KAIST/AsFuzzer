import multiprocessing
import glob
import os, sys
import argparse
import time
from arch.helper import get_opcode
from AsInferrer.asinferrer import AsInferrer


def multi(args):
    arch, target, phase, core, verbose, logfile, reset = args
    OPCODE = get_opcode(arch)

    if logfile:
        fd = open(logfile, 'a')
    else:
        fd = sys.stdout

    if not reset:
        folder = 'asfuzzer_data/%s/%s/template/db'%(target, arch)
        check_list = []
        for db in glob.glob('%s/*.db'%(folder)):
            filename = os.path.basename(db)
            check_list.append(filename[:-3])
        OPCODE = [op for op in OPCODE if op not in check_list]


    print('[+] Infer assembler grammar (Arch: %s, Assembler: %s, OPCODE: %d)'%(arch, target, len(OPCODE)), file=fd)

    start = time.time()
    if core and core > 1:
        p = multiprocessing.Pool(core)
        p.map(job, [(arch, target, opcode, phase, verbose, logfile) for opcode in OPCODE])
    else:
        compile_cnt = 0
        for opcode in OPCODE:
            compile_cnt += job((arch, target, opcode, phase, verbose, logfile))
    end = time.time()
    print("Finish grammar inference (Arch: %s, Assembler: %s, Time: %s sec)"%(arch, target, str(end-start)), file=fd)

def job(args):
    arch, target, opcode, phase, verbose, logfile = args

    inferrer = AsInferrer(arch, target, opcode, logfile)
    valid_code = inferrer.run(phase)

    if verbose:
        print('%-30s : %d'%(opcode, len(valid_code)), flush=True)
    return inferrer.compile_cnt



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AsFuzzer')

    parser.add_argument('arch', type=str)
    parser.add_argument('--target', type=str)
    parser.add_argument('--opcode', type=str)
    parser.add_argument('--phase', type=int, default=3)
    parser.add_argument('--core', type=int, default=1, help='Number of cores to use')
    parser.add_argument('--verbose', '-v', default=False, action='store_true')
    parser.add_argument('--reset', '-r', default=False, action='store_true')
    parser.add_argument('--logfile', type=str)
    args = parser.parse_args()

    if args.target:
        if args.opcode:
            job((args.arch, args.target, args.opcode, args.phase, args.verbose, args.logfile))
        else:
            multi((args.arch, args.target, args.phase, args.core, args.verbose, args.logfile, args.reset))
    else:
        for target in ['gas', 'clang', 'icc', 'masm']:
            if target in ['icc', 'masm'] and args.arch not in ['x86', 'x86-64']:
                continue

            multi((args.arch, target, args.phase, args.core, args.verbose, args.logfile, args.reset))
