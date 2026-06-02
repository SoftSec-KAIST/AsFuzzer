import os, re, sys
from mutator.helper import get_mutator
import pickle
from AsInferrer.error_parser import filter_error, get_blacklist
from AsInferrer.config import get_assembler_cmd, get_supported_archs
from AsInferrer.diff_bin import get_dump_cmd, get_assembler

class AsInferrer:
    """
    Main AsFuzzer class.
    Generates assembly instruction of given opcode which compiles with no error in as.

    :param arch: arch to fuzz
    :param opcode: opcode to fuzz
    :return:
    """
    def __init__(self, arch, assembler, opcode, logfile = '', debug=False):
        self.opcode = opcode
        self.debug = debug
        self.bugs = []
        self.assembler = assembler
        self.header = ''
        self.tail = ''
        self.tried = 0
        self.final = 0
        self.compile_cnt = 0
        self.os= os.name
        self.logfile = logfile
        self.fd = None
        if arch in ['x86', 'x86-64']:
            if assembler in ['masm']:
                if arch in ['x86']:
                    self.header = '.model flat\n.code'
                else:
                    self.header = '.code'
                self.tail = 'end'
            else:
                self.header = '.intel_syntax noprefix'
        elif arch == 'thumb':
            self.header = '.thumb'
        else:
            if assembler in ['masm']:
                self.header = 'code'
                self.tail = '\tend'

            if arch not in get_supported_archs():
                raise NotImplementedError
        self.asm_cmd = {}
        self.gas_cmd = get_assembler_cmd(arch, 'gas')
        self.clang_cmd = get_assembler_cmd(arch, 'clang')
        self.icc_cmd = get_assembler_cmd(arch, 'icc')
        self.masm_cmd = get_assembler_cmd(arch, 'masm')
        self.mutator = get_mutator(arch)
        self.arch = arch
        self.dir = f'asfuzzer_data/{assembler}/{arch}'

    def print_log(self, msg):
        if self.logfile:
            print(msg, file=self.fd)

    def is_windows(self):
        return self.os in ['nt']
    def get_path(self, sub_dir, extension='.s'):
        if self.is_windows():
            return '%s\%s\%s%s'%(self.dir.replace('/','\\'), sub_dir.replace('/','\\'), self.opcode, extension)
        return '%s/%s/%s%s'%(self.dir, sub_dir, self.opcode, extension)

    def execute(self, asm_code, cur_phase, internal_error_proof=True):
        if self.assembler in ['masm']:
            sub_code = []
            ret = []
            for idx, asm in enumerate(asm_code):
                sub_code.append(asm)
                if idx % 50 == 0 and idx > 0:
                    ret.extend(self.sub_execute(sub_code, cur_phase, internal_error_proof))
                    sub_code = []
            if sub_code:
                ret.extend(self.sub_execute(sub_code, cur_phase, internal_error_proof))

            return ret

        return self.sub_execute(asm_code, cur_phase, internal_error_proof)


    def sub_execute(self, asm_code, cur_phase, internal_error_proof=True):
        asm_file = self.get_path('phase%d/asm'%(cur_phase))
        log_file = self.get_path('phase%d/log'%(cur_phase), extension='.log')

        if self.is_windows():
            asm_file = asm_file.replace('/', '\\')
            log_file = log_file.replace('/', '\\')
            os.system('mkdir %s > $null 2>&1'%(os.path.dirname(asm_file)))
            os.system('mkdir %s > $null 2>&1'%(os.path.dirname(log_file)))
        else:
            os.system('mkdir -p %s'%(os.path.dirname(asm_file)))
            os.system('mkdir -p %s'%(os.path.dirname(log_file)))

        errs = []

        internal_errors = dict()
        unexpected_err_list = []
        while True:
            self.compile_cnt += 1
            with open(asm_file, 'w') as f:
                f.write(self.get_header() + '\n')
                for  asm in asm_code:
                    f.write('\t' + str(asm) + '\n')
                if self.get_tail():
                    f.write(self.get_tail() + '\n')

            if self.assembler in ['gas']:
                os.system('%s %s -o /dev/null 2> %s'%(self.gas_cmd, asm_file, log_file))
            elif self.assembler in ['icc']:
                os.system('%s %s -o /dev/null 2> %s'%(self.icc_cmd, asm_file, log_file))
            elif self.assembler in ['masm']:
                obj_file = asm_file + '.obj'
                self.print_log('%s /Fo %s %s > %s 2>&1'%(self.masm_cmd, obj_file, asm_file, log_file))
                os.system('%s /Fo %s %s > %s 2>&1'%(self.masm_cmd, obj_file, asm_file, log_file))
            elif self.assembler in ['clang']:
                os.system('%s %s -o /dev/null 2> %s >&2'%(self.clang_cmd, asm_file, log_file))
            else:
                raise NotImplementedError

            with open(log_file, 'r') as f:
                logs = f.read().split('\n')

            if internal_error_proof:
                crash = False
                idx = 0
                for log in logs:
                    if 'error' in log and '(' in log:
                        if self.assembler in ['masm']:
                            if self.arch in ['x86']:
                                idx = int(log.split('(')[1].split(')')[0]) - 3
                            else:
                                idx = int(log.split('(')[1].split(')')[0]) - 2
                        else:
                            idx = int(log.split(':')[1]) - 2

                    # icc/gas
                    if 'Internal error in' in log:
                        if self.assembler in ['masm']:
                            if self.arch in ['x86']:
                                idx = int(log.split('(')[1].split(')')[0]) - 3
                            else:
                                idx = int(log.split('(')[1].split(')')[0]) - 2
                        else:
                            idx = int(log.split(':')[1]) - 2
                        asm_code[idx].disable()
                        asm_code[idx].add_log(log)
                        crash = True
                        self.bugs.append(asm_code[idx])
                    # clang
                    elif 'PLEASE submit a bug report to' in log:
                        last_err = 0
                        if idx + 1 in unexpected_err_list:
                            bug_idx = max(unexpected_err_list) + 1
                        else:
                            bug_idx = idx+1
                        unexpected_err_list.append(bug_idx)
                        asm_code[bug_idx].disable()
                        asm_code[bug_idx].add_log(log)
                        crash = True
                        self.bugs.append(asm_code[bug_idx])
                        break

                if crash:
                    continue

            break

        for i, log in enumerate(logs):
            if 'Error' in log or 'error:' in log or 'error :' in log or ': error ' in log or 'Warning' in log or 'warning' in log or 'bug' in log:
                # if 'Warning' in log:
                #     print(log)
                if 'Fontconfig warning' in log:
                    continue
                try:
                    if self.assembler in ['masm']:
                        if self.arch in ['x86']:
                            idx = int(log.split('(')[1].split(')')[0]) - 3
                        else:
                            idx = int(log.split('(')[1].split(')')[0]) - 2
                    else:
                        idx = int(log.split(':')[1]) - 2
                    if idx >= 0:
                        asm_code[idx].add_log(log)
                except:
                    self.print_log('%s %s %s'%('\n'.join(logs[i-50:i+50]), asm_file, log_file))
                    continue
            elif 'Assembler messages:' in log:
                pass
            elif 'Info:' in log or 'note:' in log:
                pass
            else:
                continue
                if log:
                    self.print_log(log)


        if self.debug:
            for line in asm_code:
                line.print_with_log()

        if self.assembler in ['masm']:
            try:
                os.remove(asm_file + '.obj')
            except OSError:
                pass

        return asm_code

    def refine_operand(self, asm_code):
        for asm in asm_code:
            for log in asm.get_log():
                if 'expected' in log:
                    for (old, new) in re.findall("`(.*)'.*expected `(.*)'", log):
                        asm.fixup(old, new)

        return asm_code

    def refine(self, valid_code, invalid_code, phase):
        while True:
            new_asm_code = self.execute(valid_code, phase)
            new_invalid_code = [asm for asm in new_asm_code if asm.has_log()]
            if not new_invalid_code:
                break

            valid_code = [asm for asm in new_asm_code if not asm.has_log()]
            invalid_code.extend(new_invalid_code)

        return valid_code, invalid_code



    def phase1(self, candidates, blacklist):
        asm_gen = self.mutator(self.opcode)
        asm_code = asm_gen.phase1()

        asm_code = self.execute(asm_code, 1)

        valid_code = [asm for asm in asm_code if not asm.has_log()]
        invalid_code = [asm for asm in asm_code if asm.has_log()]
        if self.assembler not in ['masm']:
            valid_code, invalid_code = self.refine(valid_code, invalid_code, 1)

        candidate_code = filter_error(invalid_code, blacklist)
        # unsupproted?
        return valid_code, candidate_code

    def phase2(self, candidates, blacklist):
        asm_code = []
        for candidate in candidates:
            asm_code.extend(candidate.phase2())

        asm_code = self.execute(asm_code, 2)

        valid_code = [asm for asm in asm_code if not asm.has_log()]
        invalid_code = [asm for asm in asm_code if asm.has_log()]

        if self.assembler not in ['masm']:
            valid_code, invalid_code = self.refine(valid_code, invalid_code, 2)

        candidate_code = filter_error(invalid_code, blacklist)


        # Warning: XXX is expected
        if self.arch in ['x86', 'x86-64']:
            candidate_code = self.refine_operand(candidate_code)

        return valid_code, candidate_code


    def phase3(self, candidates, blacklist = ''):
        asm_code = []
        for candidate in candidates:
            asm_code.extend(candidate.phase3())

        asm_code = self.execute(asm_code, 3)

        valid_code = [asm for asm in asm_code if not asm.has_log()]
        invalid_code = [asm for asm in asm_code if asm.has_log()]
        if self.assembler not in ['masm']:
            valid_code, invalid_code = self.refine(valid_code, invalid_code, 3)
        candidate_code = filter_error(invalid_code, blacklist=blacklist)

        return valid_code, candidate_code

    def phase4(self, candidates, blacklist = ''):
        asm_code = []
        for candidate in candidates:
            asm_code.extend(candidate.phase4())

        asm_code = self.execute(asm_code, 4)

        valid_code = [asm for asm in asm_code if not asm.has_log()]
        if self.assembler not in ['masm']:
            valid_code, invalid_code = self.refine(valid_code, invalid_code, 4)
        candidate_code = []

        return valid_code, candidate_code

    def phase10(self, candidates):
        asm_code = self.execute(candidates, 10)

        valid_code = [asm for asm in asm_code if not asm.has_log()]
        return valid_code

    def get_header(self):
        return self.header

    def get_tail(self):
        return self.tail

    def get_valid_asm_format(self, asm_lines):
        lines = [self.get_header()]
        for asm in asm_lines:
            lines.append('\t'+str(asm))
        if self.get_tail():
            lines.append(self.get_tail())
        return lines

    def write_code(self, code, folder):
        if self.assembler in ['masm']:
            asm_file = self.get_path(folder, extension='.asm')
        else:
            asm_file = self.get_path(folder)
        new_folder = os.path.dirname(asm_file)
        if self.is_windows():
            os.system('mkdir %s > $null 2>&1'%(new_folder))
        else:
            os.system('mkdir -p %s'%(new_folder))

        with open(asm_file, 'w') as f:
            for line in self.get_valid_asm_format(code):
                f.write(line + '\n')

        # write masm -> gas , gas -> masm
        if folder in ['final/asm'] and self.arch in ['x86', 'x86-64']:
            if self.assembler in ['masm']:
                other_asm_file = self.get_path(folder)
                self.header = '.intel_syntax noprefix'
                self.tail = ''
            else:
                other_asm_file = self.get_path(folder, extension='.asm')
                if self.arch in ['x86']:
                    self.header = '.model flat\n.code'
                else:
                    self.header = '.code'
                self.tail = 'end'
            with open(other_asm_file, 'w') as f:
                for line in self.get_valid_asm_format(code):
                    f.write(line + '\n')

        return asm_file


    def write_template(self, code, folder):
        asm_folder = folder + '/asm'
        db_folder = folder + '/db'
        tpl_file = self.get_path(asm_folder)
        db_file = self.get_path(db_folder, extension='.db')

        if self.is_windows():
            os.system('mkdir %s > $null 2>&1'%(os.path.dirname(tpl_file)))
            os.system('mkdir %s > $null 2>&1'%(os.path.dirname(db_file)))
        else:
            os.system('mkdir -p %s'%(os.path.dirname(tpl_file)))
            os.system('mkdir -p %s'%(os.path.dirname(db_file)))



        with open(tpl_file, 'w') as f:
            for asm in code:
                f.write(asm.get_template()+ '\n')

        with open(db_file, 'wb') as f:
            pickle.dump(code, f)



    def run(self, phase=3):

        if self.logfile:
            self.fd = open(self.logfile, 'a')
        else:
            self.fd = sys.stdout

        valid, valid_code = [], []
        candidates = []
        phase_funcs = [self.phase1, self.phase2, self.phase3, self.phase4]
        #asm_gen = self.mutator(self.opcode)
        check_list = []

        for i in range(phase):
            cur_phase = i + 1

            blacklist = get_blacklist(self.arch, cur_phase, self.assembler)

            candidates.extend(valid_code)
            valid, candidates = phase_funcs[i](candidates, blacklist)
            for asm in valid:
                if str(asm) not in check_list:
                    valid_code.append(asm)
                    check_list.append(str(asm))

            #valid_code.extend(valid) # phase2 contains phase1 -> maybe optimize this

        if self.bugs:
            self.write_code(self.bugs, 'bugs')


        # filter assembly code if disassembled code has different opcode
        #if self.assembler not in ['masm']:
        valid_code = self.filter(valid_code)

        if valid_code:
            self.write_template(valid_code, 'template')

        if self.logfile:
            self.fd.close()
        self.fd = None
        return valid_code



    def compile(self, asm, output):
        if self.assembler in ['clang', 'icc']:
            cmd = '%s -c %s -o %s 2> /dev/null'%(get_assembler(self.arch, self.assembler), asm, output)
        elif self.assembler in ['gas']:
            cmd = '%s %s -o %s 2> /dev/null'%(get_assembler(self.arch, self.assembler), asm, output)
        elif self.assembler in ['masm']:
            cmd = '%s /Fo %s /c %s 2> /dev/null 1>&2'%(get_assembler(self.arch, self.assembler), output, asm)
        self.compile_cnt += 1
        os.system(cmd)

    def get_dump(self, binfile):
        if os.path.exists(binfile):
            dump_file = binfile[:-2] + '.txt'
            cmd = get_dump_cmd(self.arch, self.assembler, binfile, dump_file)
            os.system(cmd)
            with open(dump_file) as f:
                return f.read().split('\n')
        return []

    def filter(self, valid_code, fd=None):
        if fd is not None:
            self.fd = fd

        mismatch = 0
        refined_lines = []
        bin_file = self.get_path('tmp/bin', extension='.o')
        asm_file = self.get_path('tmp/asm', extension='.s')

        if self.is_windows():
            bin_file = bin_file.replace('\\','/')
            asm_file = asm_file.replace('\\','/')
        os.system('mkdir -p %s'%(os.path.dirname(bin_file)))
        os.system('mkdir -p %s'%(os.path.dirname(asm_file)))

        while len(valid_code) > 0 :
            asm = self.write_code(valid_code, 'tmp/asm')
            if self.is_windows():
                asm = asm.replace('\\','/')
            self.compile(asm, bin_file)
            dump_lines = self.get_dump(bin_file)

            if not dump_lines:
                ex_len = len(valid_code)
                valid_code = self.phase10(valid_code)
                if ex_len == len(valid_code):
                    valid_code = valid_code[1:]

                continue

            for idx, line in enumerate(dump_lines):
                if self.opcode in line.split():
                    refined_lines.append(valid_code[0])
                    valid_code.pop(0)
                else:
                    if idx == 0:
                        self.print_log('[%5s] %-30s | %-30s'%(self.assembler, str(valid_code[0]), line))
                        valid_code.pop(0)
                        mismatch += 1
                    break
        if refined_lines:
            if mismatch:
                self.print_log('[+] filter(%s-%s-%s) %d %d'%(self.arch, self.opcode, self.assembler, len(refined_lines), mismatch))
            else:
                self.print_log('[*] filter(%s-%s-%s) %d %d'%(self.arch, self.opcode, self.assembler, len(refined_lines), mismatch))

            asm = self.write_code(refined_lines, 'final/asm')
            bin_file = self.get_path('final/bin', extension='.o')
            os.system('mkdir -p %s'%(os.path.dirname(bin_file)))
            self.compile(asm, bin_file)
            self.get_dump(bin_file)

        elif mismatch > 0:
            self.print_log('[+] filter(%s-%s-%s) %d %d'%(self.arch, self.opcode, self.assembler, len(refined_lines), mismatch))

        return refined_lines
