import random
import argparse
import os
from collections import namedtuple
from arch import intel, arm, mips
from fuzzer import AsFuzzer2, TimeOutException


Pair = namedtuple('Pair', ['assembler', 'num', 'glist',  'gdict'])

total_iter = 0

class AsGen(AsFuzzer2):

    def __init__(self, save_file, arch, N, tot_insts):
        self.save_file = save_file
        self.cnt = 0
        self.tot_insts = tot_insts

        if os.path.exists(save_file):
            os.remove(save_file)
        super().__init__(arch, 0, N, True, 0, '')

    def write_code(self, template):
        with open(self.save_file, 'a') as fd:
            print(str(template), file=fd)

    def rand_gen_inst_list(self, grammar1, grammar2, num_of_inst):
        common_list = []
        diff_list = []
        if len(grammar1) == 0:
            return common_list, diff_list

        for idx in range(num_of_inst):
            if self.cnt >= self.tot_insts:
                continue
            self.cnt += 1
            temp_idx = random.randrange(0, len(grammar1))
            template = grammar1[temp_idx]
            self.write_code(template)
        return common_list, diff_list



def run(cfg):
    arch, opcode = cfg
    fuzzer = AsGen(arch)
    fuzzer.seq_run(opcode)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AsFuzz_diff_test')
    parser.add_argument('arch', type=str)
    parser.add_argument('target', type=str, help='Target Assembler to expand coverage')
    parser.add_argument('tot_insts', type=int)
    parser.add_argument('save_file', type=str)
    parser.add_argument('--N', type=int, default=20, help='Number of instructions in each iteration')
    parser.add_argument('--core', type=int, default=1, help='Number of cores to use')
    parser.add_argument('--no-optimize', dest='optimize', action='store_false')


    args = parser.parse_args()
    try:
        fuzzer = AsGen(args.save_file, args.arch, args.N, args.tot_insts)
        while True:
            fuzzer.rand_run(args.optimize, args.target )
            total_iter += fuzzer.num_of_inst
            if total_iter > args.tot_insts:
                break
    except TimeOutException as e:
        pass

