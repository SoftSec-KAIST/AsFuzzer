#####################################################################
# Total: 3 (C1:2, C2:1, C3:0, C4:0, C5:0, C6:0)
# Compile:      ../../bin/aarch64-linux-gnu-as aarch64.s -o aarch64.o
# disassembly:  ../../bin/objdump -d --no-show-raw-insn aarch64.o
#####################################################################

C1:
    # C1. Using wrong register(s) (2)
    tbz X0, [1], D0
    tbnz X0, [1], H0

C2:
    # C2. Confusing an operand and a label (1)
    adrp X0, 1<<4
