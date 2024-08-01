#########################################################################################
# Total: 5 (C1:0, C2:5, C3:0, C4:0, C5:0, C6:0)
# Compile:      ../../bin/clang -c --target=mips mips.s -o mips.o
# disassembly:  ../../bin/objdump -d --no-show-raw-insn mips.o
#########################################################################################

C2:
    # C2. Confusing an operand and a label (5)
    bc1tl (1)
    bc1fl (2)
    jal (3)
    jalx (4)
    j (5)
