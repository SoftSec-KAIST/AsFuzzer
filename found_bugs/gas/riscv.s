#####################################################################
# Total: 4 (C1:0, C2:4, C3:0, C4:0, C5:0, C6:0)
# Compile:      ../../bin/riscv-linux-gnu-as riscv.s -o riscv.o
# disassembly:  ../../bin/objdump -d --no-show-raw-insn riscv.o
#####################################################################

C2:
    # C2. Confusing an operand and a label (4)
    j (1)
    jal (2)
    jalr (a3)
    jr (a4)

