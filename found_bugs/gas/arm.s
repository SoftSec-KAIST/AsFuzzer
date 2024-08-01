#####################################################################
# Total: 1 (C1:1, C2:0, C3:0, C4:0, C5:0, C6:0)
# Compile:      ../../bin/arm-linux-gnueabi-as arm.s -o arm.o
# disassembly:  ../../bin/objdump -d --no-show-raw-insn arm.o
#####################################################################

C1:
    # C1. Using wrong register(s) (1)
    lsr R0, #1, 1<<4
