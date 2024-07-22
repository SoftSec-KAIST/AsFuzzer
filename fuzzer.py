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


Pair = namedtuple('Pair', ['assembler', 'num', 'glist',  'gdict'])

total_iter = 0

class TimeOutException(Exception):
    pass

def alarm_handler(signum, frame):
    global total_iter
    print("Time is up! (Iterations: %s)"%(total_iter))
    raise TimeOutException()

class AsFuzzer2:

    def __init__(self, arch, timeout = 0, num_of_inst=20, random = False, id=0, opcode='', verbose=False):
        self.arch = arch
        self.id = id
        self.num_of_inst = num_of_inst
        self.pairs = []
        self.num = 0
        self.debug = False
        self.random = random
        self.start = time.time()
        self.verbose = verbose

        self.summary_dict = {'gas':[], 'clang':[], 'icc':[], 'masm':[]}
        self.diff_err_dict = {'gas':{}, 'clang':{}, 'icc':{}, 'masm':{}}
        self.same_err_dict = {'clang_gas':{}, 'clang_icc':{}, 'clang_masm':{},
                              'gas_icc':{}, 'gas_masm':{}, 'icc_masm':{}}

        if timeout > 0:
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(timeout)

        for target in ['gas', 'clang', 'icc', 'masm']:
            if target in ['icc', 'masm'] and arch not in ['x86', 'x86-64']:
                continue
            for other in ['gas', 'clang', 'icc', 'masm']:
                if other in ['icc', 'masm'] and arch not in ['x86', 'x86-64']:
                    continue
                if target == other: continue

                self.create_folders(arch, target, other)

            pair = self.make_pairs(target, opcode)
            self.pairs.append(pair)

    def make_pairs(self, target, opcode=''):
        if opcode:
            folder = 'asfuzzer_data/%s/%s/template/db/%s.db'%(target, self.arch, opcode)
        else:
            folder = 'asfuzzer_data/%s/%s/template/db/*.db'%(target, self.arch)
        gdict = dict()
        for db in glob.glob(folder):
            filename = os.path.basename(db)
            with open(db, 'rb') as f:
                data = pickle.load(f)
                gdict[filename] = data

        return Pair(target, len(gdict), list(gdict.keys()), gdict)

    def seq_run(self, opcode):
        num_of_pairs = len(self.pairs)
        if opcode:
            opcode += '.db'
        for idx1 in range(num_of_pairs):
            for idx2 in range(num_of_pairs):
                if idx1 == idx2:
                    continue
                if opcode:
                    self.debug = True
                    if opcode in self.pairs[idx1].gdict:
                        self.seq_test_inst(self.pairs[idx1], self.pairs[idx2], opcode)
                else:
                    self.seq_test_grammar(self.pairs[idx1], self.pairs[idx2])

    def create_folders(self, arch, tool1, tool2):

        uname = '_'.join(sorted([tool1,tool2]))
        folder1 = f'diff/{arch}/same/{uname}/{tool1}/temp/'
        folder2 = f'diff/{arch}/same/{uname}/{tool2}/temp/'
        folder3 = f'diff/{arch}/same/{uname}/{tool1}/bindiff/'
        folder4 = f'diff/{arch}/same/{uname}/{tool2}/bindiff/'

        os.system('mkdir -p %s/'%(folder1))
        os.system('mkdir -p %s/'%(folder2))
        os.system('mkdir -p %s/'%(folder3))
        os.system('mkdir -p %s/'%(folder4))

        folder5 = f'diff/{arch}/diff/{tool1}/temp/'
        folder6 = f'diff/{arch}/diff/{tool1}/bindiff/'

        os.system('mkdir -p %s/'%(folder5))
        os.system('mkdir -p %s/'%(folder6))

    def seq_test_grammar(self, pair1, pair2):
        for opcode_idx in range(pair1.num):
            opcode = pair1.glist[opcode_idx]
            #print(opcode)
            self.seq_test_inst(pair1, pair2, opcode)


    def seq_test_inst(self, pair1, pair2, opcode):
        grammar1 = pair1.gdict[opcode]
        if opcode in pair2.gdict:
            grammar2 = pair2.gdict[opcode]
        else:
            grammar2 = []

        commonst_list, diff_list = self.seq_gen_inst_list(grammar1, grammar2)
        self.test_for_same_grammars(opcode, pair1.assembler, pair2.assembler, commonst_list)
        self.test_for_diff_grammars(opcode, pair1.assembler, pair2.assembler, diff_list)

    def seq_gen_inst_list(self, grammar1, grammar2):
        common_list = []
        diff_list = []

        num_of_inst = len(grammar1)
        check_list = []
        for idx in range(num_of_inst):
            template = grammar1[idx]
            if str(template) in check_list:
                continue
            check_list.append(str(template))
            if self.is_in_grammar(grammar2, template):
                common_list.append(template)
            else:
                diff_list.append(template)
        return common_list, diff_list



    def compile_and_dump(self, asm_lines, assembler, output, sensitive=False):
        if assembler in ['masm']:
            tool = MasmAsm(self.arch, assembler)
        else:
            tool = GasAsm(self.arch, assembler)

        asm = output[:-2] + '.s'
        tool.write_code(asm_lines, asm)
        if sensitive:
            log_file = output[:-2] + '.log'
            tool.compile(output, log_file)
            with open(log_file, 'r') as f:
                logs = f.read()
                for msg in ['Warning', 'warning']:
                    if msg in logs:
                        #print('[-] drop compiled result since assembler emits warning')
                        return []
        else:
            tool.compile(output)

        if os.path.exists(output):
            dump = output[:-2] + '.txt'
            return tool.get_dump(output, dump)
        return []

    def test_for_same_grammars(self, opcode, tool1, tool2, common_list, id = 0):

        if not common_list:
            return

        if opcode.endswith('.db'):
            opcode = opcode[:-3]

        arch = self.arch
        uname = '_'.join(sorted([tool1,tool2]))
        folder1 = f'diff/{arch}/same/{uname}/{tool1}/temp'
        folder2 = f'diff/{arch}/same/{uname}/{tool2}/temp'
        folder3 = f'diff/{arch}/same/{uname}/{tool1}/bindiff'
        folder4 = f'diff/{arch}/same/{uname}/{tool2}/bindiff'

        if id > 0:
            output1 = f'{folder1}/{id}_{opcode}.o'
            output2 = f'{folder2}/{id}_{opcode}.o'
            output3 = f'{folder3}/{id}_{opcode}.txt'
            output4 = f'{folder4}/{id}_{opcode}.txt'
            output5 = f'{folder3}/{id}_{opcode}.s'
        else:
            output1 = f'{folder1}/{opcode}.o'
            output2 = f'{folder2}/{opcode}.o'
            output3 = f'{folder3}/{opcode}.txt'
            output4 = f'{folder4}/{opcode}.txt'
            output5 = f'{folder3}/{opcode}.s'

        asm_lines = []
        for line in common_list:
            if self.random:
                asm_lines.append(line.get_random_asm())
            else:
                asm_lines.append(str(line))


        if opcode in self.same_err_dict[uname]:
            asm_lines = [asm for asm in asm_lines if asm not in self.same_err_dict[uname][opcode]]

        if not asm_lines:
            return


        # get binary & dump file
        dump1 = self.compile_and_dump(asm_lines, tool1, output1)
        dump2 = self.compile_and_dump(asm_lines, tool2, output2)

        # get binary & dump file
        if dump1 and dump2:
            if dump1 != dump2:
                if opcode not in self.same_err_dict[uname]:
                    self.same_err_dict[uname][opcode] = []
                for line in asm_lines:
                    self.same_err_dict[uname][opcode].append(line)

                with open(output3, 'w') as f:
                    for line in dump1:
                        f.write(line+'\n')
                with open(output4, 'w') as f:
                    for line in dump2:
                        f.write(line+'\n')
                '''
                diff_asm = self.filter(asm_lines, dump1, dump1, opcode)
                if diff_asm:
                    with open(output5, 'w') as f:
                        for line in diff_asm:
                            f.write(line+'\n')
                '''
                self.summary_dict[tool1].append(opcode)
                self.summary_dict[tool2].append(opcode)

                if tool1 in ['masm']:
                    os.rename(output1[:-2] + '.asm', output3[:-4] + '.s')
                else:
                    os.rename(output1[:-2] + '.s', output3[:-4] + '.s')

                if tool2 in ['masm']:
                    os.rename(output2[:-2] + '.asm', output4[:-4] + '.s')
                else:
                    os.rename(output2[:-2] + '.s', output4[:-4] + '.s')

        os.system('rm -f %s.*'%(output1[:-2]))
        os.system('rm -f %s.*'%(output2[:-2]))


    def filter(self, asm_lines, dump1, dump2, opcode):
        code1 = [asm for asm in asm_lines if opcode in asm.split()]
        code2 = [asm for asm in dump1 if opcode in asm.split()]
        code3 = [asm for asm in dump2 if opcode in asm.split()]

        ret = []
        for idx in range(len(code1)):
            if code2[idx] != code3[idx]:
                ret.append(code1[idx])
        return ret

    def test_for_diff_grammars(self, opcode, tool1, tool2, diff_list, id = 0):
        if not diff_list:
            return

        if opcode.endswith('.db'):
            opcode = opcode[:-3]

        arch = self.arch

        folder1 = f'diff/{arch}/diff/{tool1}/temp'
        folder2 = f'diff/{arch}/diff/{tool1}/bindiff'

        if id > 0:
            output1 = f'{folder1}/{id}_{opcode}.o'
            output2 = f'{folder2}/{id}_{opcode}.s'
            output3 = f'{folder2}/{id}_{opcode}.txt'
        else:
            output1 = f'{folder1}/{opcode}.o'
            output2 = f'{folder2}/{opcode}.s'
            output3 = f'{folder2}/{opcode}.txt'

        asm_lines = []
        for line in diff_list:
            if self.random:
                asm_lines.append(line.get_random_asm())
            else:
                asm_lines.append(str(line))

        if opcode in self.diff_err_dict[tool1]:
            asm_lines = [asm for asm in asm_lines if asm not in self.diff_err_dict[tool1][opcode]]

        if not asm_lines:
            return

        # get binary & dump file
        dump1 = self.compile_and_dump(asm_lines, tool1, output1, sensitive=True)

        report = BinDump(arch, opcode, dump1, self.verbose)
        report.cmp_asm_code(diff_list, tool1)
        if report.has_bugs():
            if opcode not in self.diff_err_dict[tool1]:
                self.diff_err_dict[tool1][opcode] = []
            for line in asm_lines:
                self.diff_err_dict[tool1][opcode].append(line)

            report.dump_all(output3)
            if tool1 in ['masm']:
                os.rename(output1[:-2] + '.asm', output2)
            else:
                os.rename(output1[:-2] + '.s', output2)
            '''
            if 'type' in report.errors:
                report.dump_asm_lines(output2)
                report.dump_lines(output3)

            else:
                report.dump_all(output3)
                with open(output2, 'w') as f:
                    for line in diff_list:
                        f.write(str(line)+'\n')
            '''
            self.summary_dict[tool1].append(opcode)

        os.system('rm -f %s.*'%(output1[:-2]))



    def rand_gen_inst_list(self, grammar1, grammar2, num_of_inst):
        common_list = []
        diff_list = []
        if len(grammar1) == 0:
            return common_list, diff_list

        for idx in range(num_of_inst):
            temp_idx = random.randrange(0, len(grammar1))
            template = grammar1[temp_idx]
            if self.is_in_grammar(grammar2, template):
                common_list.append(template)
            else:
                diff_list.append(template)
        return common_list, diff_list


    def fuzz(self, opcode, pair1, pair2, grammar1, grammar2, num_of_inst):
        common_list, diff_list = self.rand_gen_inst_list(grammar1, grammar2, num_of_inst)
        id = time.time() - self.start
        self.test_for_same_grammars(opcode, pair1.assembler, pair2.assembler, common_list, id)
        id = time.time() - self.start
        self.test_for_diff_grammars(opcode, pair1.assembler, pair2.assembler, diff_list, id)

    def random_test_grammar(self, pair1, pair2, optimize = True, fixed_opcode=''):
        grammar1 = []

        while len(grammar1) == 0:
            opcode_idx = random.randrange(0, pair1.num)
            opcode = pair1.glist[opcode_idx]
            grammar1 = pair1.gdict[opcode]


        if fixed_opcode:
            opcode = fixed_opcode + '.db'
            if opcode not in pair1.gdict:
                return
            grammar1 = pair1.gdict[opcode]


        if opcode in pair2.gdict:
            grammar2 = pair2.gdict[opcode]
        else:
            grammar2 = []

        if optimize:
            self.fuzz(opcode, pair1, pair2, grammar1, grammar2, self.num_of_inst)
        else:
            for idx in range(self.num_of_inst):
                self.fuzz(opcode, pair1, pair2, grammar1, grammar2, 1)

    def single_run(self, opcode, target):
        num_of_pairs = len(self.pairs)
        for idx1, pair1 in enumerate(self.pairs):
            if pair1.assembler == target:
                key = opcode + '.db'
                if key not in pair1.gdict:
                    return
                grammar1 = pair1.gdict[key]
                if len(grammar1) == 0:
                    return

                idx2 = random.randrange(0, num_of_pairs)
                while idx1 == idx2:
                    idx2 = random.randrange(0, num_of_pairs)
                pair2 = self.pairs[idx2]
                if key in pair2.gdict:
                    grammar2 = pair2.gdict[key]
                else:
                    grammar2 = []
                self.fuzz(opcode, pair1, pair2, grammar1, grammar2, self.num_of_inst)
                break

    def rand_run(self, optimize, target='', fixed_opcode=''):
        num_of_pairs = len(self.pairs)
        if target:
            for idx1 in range(num_of_pairs):
                if self.pairs[idx1].assembler == target:
                    break
        else:
            idx1 = random.randrange(0,num_of_pairs)

        idx2 = random.randrange(0,num_of_pairs)
        while idx1 == idx2:
            idx2 = random.randrange(0,num_of_pairs)
        if self.pairs[idx1].num > 0:
            self.random_test_grammar(self.pairs[idx1], self.pairs[idx2], optimize, fixed_opcode)

    def run(self, common_list, diff_list):

        if diff_list:
            if common_list:
                print(common_list)

    def is_in_grammar(self, grammar, template):
        for temp in grammar:
            if temp.get_template() == template.get_template():
                return True
        return False


    def retrieve_logs(self, target_path, opdict):
        for logfile in glob.glob(target_path):
            if logfile.endswith('.s'):
                opcode = logfile.split('/')[-1].split('_')[-1][:-2]
            if logfile.endswith('.txt'):
                opcode = logfile.split('/')[-1].split('_')[-1][:-4]
            if opcode not in opdict:
                opdict[opcode] = []
            with open(logfile, 'r') as fd:
                opdict[opcode].extend([line for line in fd.read().split('\n') if line])

        return opdict

    def print_opdict(self, opdict):

        for opcode in sorted(opdict):
            print('%s'%(opcode))
            for inst in sorted(set(opdict[opcode])):
                print('\t%s'%(inst))


    def report_summary(self, filename, arch):

        for tool in ['clang', 'gas', 'icc', 'masm']:
            opdict = dict()
            print('[%s]'%(tool))
            opdict = self.retrieve_logs(f'diff/{arch}/diff/{tool}/bindiff/*.s', opdict)
            self.print_opdict(opdict)


        for tool1 in ['clang', 'gas', 'icc', 'masm']:
            for tool2 in ['clang', 'gas', 'icc', 'masm']:
                if tool1 == tool2: continue
                if tool1 > tool2: continue

                opdict = dict()
                print('[%s vs. %s]'%(tool1, tool2))

                uname = '_'.join(sorted([tool1, tool2]))

                opdict = self.retrieve_logs(f'diff/{arch}/same/{uname}/{tool1}/bindiff/*.s', opdict)

                self.print_opdict(opdict)


        if filename:
            with open(filename, 'w') as fd:
                for tool in ['clang', 'gas', 'icc', 'masm']:
                    oplist = self.summary_dict[tool]
                    opset = set(self.summary_dict[tool])

                    print('[+] %s: %d\t%d'%(tool, len(oplist), len(opset)), file=fd)
                    print(list(opset), file=fd)


def run(cfg):
    arch, opcode = cfg
    fuzzer = AsFuzzer2(arch)
    fuzzer.seq_run(opcode)

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
    parser.add_argument('--timeout', type=int, default=0)
    parser.add_argument('--N', type=int, default=20, help='Number of instructions in each iteration')
    parser.add_argument('--no-random', dest='random', action='store_false')
    parser.add_argument('--core', type=int, default=1, help='Number of cores to use')
    parser.add_argument('--opcode', type=str)
    parser.add_argument('--no-optimize', dest='optimize', action='store_false')
    parser.add_argument('--target', type=str, help='Target Assembler to expand coverage')
    parser.add_argument('--report', type=str, help='Save summary')
    parser.add_argument('--verbose', action='store_true')


    args = parser.parse_args()
    if args.core > 1:
        multi(args.arch, args.core)
    elif args.target and args.opcode:
        fuzzer = AsFuzzer2(args.arch, args.timeout, args.N, args.random, opcode=args.opcode, verbose=args.verbose)
        fuzzer.single_run(args.opcode, args.target)
    else:
        try:
            fuzzer = AsFuzzer2(args.arch, args.timeout, args.N, args.random, verbose=args.verbose)
            if args.random:
                while True:
                    fuzzer.rand_run(args.optimize, args.target, fixed_opcode=args.opcode)
                    total_iter += 1
            else:
                fuzzer.seq_run(args.opcode)
        except TimeOutException as e:
            fuzzer.report_summary(args.report, args.arch)
