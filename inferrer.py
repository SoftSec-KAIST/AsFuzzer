import multiprocessing
import glob
import os, sys
import argparse
import time
from arch.helper import get_opcode
from AsInferrer.asinferrer import AsInferrer
from AsInferrer.config import check_assembler


def validate_assemblers(arch, targets):
    """Verify each assembler binary is a valid executable before inference starts.

    Aborts (returns False) on broken binaries (e.g. un-pulled Git LFS pointers);
    missing assemblers are only warned about and skipped.
    """
    print('[+] Validating assemblers (arch: %s)' % arch)
    ok = True
    for target in targets:
        path, status = check_assembler(arch, target)
        if status == 'unsupported':
            continue
        elif status == 'ok':
            print('  [*] %-6s %-24s OK' % (target, path))
        elif status == 'missing':
            print('  [!] %-6s %-24s MISSING (skipped)' % (target, path))
        elif status == 'lfs_pointer':
            ok = False
            print('  [-] %-6s %-24s INVALID: Git LFS pointer file '
                  '(run: git lfs pull)' % (target, path))
        else:
            ok = False
            print('  [-] %-6s %-24s INVALID: %s' % (target, path, status))
    return ok


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
    total = len(OPCODE)
    if core and core > 1:
        p = multiprocessing.Pool(core)
        compile_cnt = 0
        task_args = [(arch, target, opcode, phase, verbose, logfile) for opcode in OPCODE]
        for i, cnt in enumerate(p.imap_unordered(job, task_args)):
            compile_cnt += cnt
            if not verbose and total > 0:
                pct = (i + 1) / total * 100
                print('\r  [%5.1f%%] (%d/%d)' % (pct, i + 1, total),
                      end='', flush=True, file=sys.stderr)
        if not verbose and total > 0:
            print(file=sys.stderr)
    else:
        compile_cnt = 0
        for i, opcode in enumerate(OPCODE):
            if not verbose and total > 0:
                pct = i / total * 100
                print('\r  [%5.1f%%] (%d/%d) %-30s' % (pct, i, total, opcode),
                      end='', flush=True, file=sys.stderr)
            compile_cnt += job((arch, target, opcode, phase, verbose, logfile))
        if not verbose and total > 0:
            print('\r  [100.0%%] (%d/%d) done%s' % (total, total, ' ' * 30),
                  flush=True, file=sys.stderr)
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
        targets = [args.target]
    else:
        targets = [t for t in ['gas', 'clang', 'icc', 'masm']
                   if not (t in ['icc', 'masm'] and args.arch not in ['x86', 'x86-64'])]

    if not validate_assemblers(args.arch, targets):
        print('[-] Assembler validation failed. Aborting.', file=sys.stderr)
        sys.exit(1)

    if args.target:
        if args.opcode:
            job((args.arch, args.target, args.opcode, args.phase, args.verbose, args.logfile))
        else:
            multi((args.arch, args.target, args.phase, args.core, args.verbose, args.logfile, args.reset))
    else:
        for target in targets:
            multi((args.arch, target, args.phase, args.core, args.verbose, args.logfile, args.reset))
