################################################################################
# Total: 3 (C1:0, C2:0, C3:0, C4:0, C5:0, C6:3)
# Compile:      ../../bin/clang -c --target=armv8-linux-eabi  arm.s -o arm.o
# disassembly:  ../../bin/objdump -d --no-show-raw-insn arm.o
################################################################################

C6:
    # C6. Emitting nothing (3)
    dsb [R3,#1]
    dmb [R8]
    isb [R1,#1]
