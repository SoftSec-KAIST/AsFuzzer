#####################################################################
# Total: 4 (C1:0, C2:4, C3:0, C4:0, C5:0, C6:0)
# Compile:      ../../bin/mips-linux-gnu-as mips.s -o mips.o
# disassembly:  ../../bin/objdump -d --no-show-raw-insn mips.o
#####################################################################

C2:
    # C2. Confusing an operand and a label (4)
    syscall (1)
    break (2)
    c2 (3)
    c3 (4)
