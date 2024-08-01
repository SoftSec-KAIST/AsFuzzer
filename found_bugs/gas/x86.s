###########################################################
# Total: 22 (C1:4, C2:5, C3:12, C4:1, C5:0, C6:0)
# Compile:      ../../bin/as -32 x86.s -o x86.o
# disassembly:  ../../bin/objdump -d -M intel --no-show-raw-insn x86.o
###########################################################

.intel_syntax noprefix

C1:
    # C1. Using wrong register(s) (4)
    ltr EDI                                             # ltr    di
    lldt EDI                                            # lldt   di
    verr EDI                                            # verr   di
    verw EDI                                            # verw   di

C2:
    # C2. Confusing an operand and a label (5)
    loop XMMWORD PTR [1]
    loope XMMWORD PTR [1]
    loopne XMMWORD PTR [1]
    jecxz ZMMWORD PTR [1]
    jcxz BYTE PTR [1]

C3:
    # C3. Ignoring pointer directives (12)
    cldemote XMMWORD PTR [1]
    clflush DWORD PTR [1]
    clflushopt WORD PTR [1]
    clwb XMMWORD PTR [EAX]
    invlpg QWORD PTR [EAX+1]
    prefetch WORD PTR [EAX+1]
    prefetchw ZMMWORD PTR [EAX+1]
    prefetchnta XMMWORD PTR [EAX+1]
    prefetcht0 DWORD PTR [EAX+1]
    prefetcht1 QWORD PTR [EAX+1]
    prefetcht2 WORD PTR [EAX+1]
    prefetchwt1 WORD PTR [EAX+1]

C4:
    # C4. Incorrect # of operands (1)
    div AX, WORD PTR [1]
