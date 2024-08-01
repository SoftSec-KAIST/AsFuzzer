###########################################################
# Total: 27 (C1:11, C2:5, C3:11, C4:0, C5:0, C6:0)
# Compile:      ../../bin/as x86-64.s -o x86-64.o
# disassembly:  ../../bin/objdump -d -M intel --no-show-raw-insn x86-64.o
###########################################################

.intel_syntax noprefix

C1:
    # C1. Using wrong register(s) (11)
    lar R11, R8W                            # lar   r11,r8
    lldt R8D                                # lldt  r8w
    lsl RAX, WORD PTR [1]                   # lsl   eax,WORD PTR ds:0x1
    ltr EDI                                 # ltr   di
    mov R10, GS                             # mov   r10d, gs
    movmskpd R9, XMM0                       # movmskpd r9d,  xmm0
    pmovmskb R10, MM2                       # pmovmskb r10d, mm2
    sldt R15                                # sldt  r15d
    str R8                                  # str   r8d
    verr RAX                                # verr  ax
    verr RSP                                # verr  sp

C2:
    # C2. Confusing an operand and a label (5)
    jecxz YMMWORD PTR [1]
    jrcxz QWORD PTR [1]
    loop XMMWORD PTR [1]
    loope XMMWORD PTR [1]
    loopne XMMWORD PTR [1]

C3:
    # C3. Ignoring pointer directives (11)
    cldemote QWORD PTR [1]
    clflush WORD PTR [1]
    clflushopt XMMWORD PTR [1]
    clwb XMMWORD PTR [1]
    invlpg WORD PTR [1]
    prefetch YMMWORD PTR [1]
    prefetchw YMMWORD PTR [1]
    prefetcht0 ZMMWORD PTR [1]
    prefetcht1 XMMWORD PTR [1]
    prefetcht2 XMMWORD PTR [1]
    prefetchwt1 ZMMWORD PTR [1]


