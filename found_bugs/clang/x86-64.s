############################################################
# Total: 72 (C1:20, C2:23, C3:29, C4:0, C5:0, C6:0)
# Compile:      ../../bin/clang -c x86-64.s -o x86-64.o
# disassembly:  ../../bin/objdump -d -M intel --no-show-raw-insn x86-64.o
############################################################

.intel_syntax noprefix

C1:
    # C1. Using wrong register(s) (20)
    cmpbexadd [RAX+1], EBP, R9D             # cmpbexadd DWORD PTR [rax+0x1],r13d,r9d
    cmpbxadd [RAX+1], EBP, R9D              # cmpbxadd DWORD PTR [rax+0x1],r13d,r9d
    cmplexadd [RAX+1], EBP, R9D             # cmplexadd DWORD PTR [rax+0x1],r13d,r9d
    cmplxadd [RAX+1], EBP, R9D              # cmplxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnbexadd [RAX+1], EBP, R9D            # cmpnbexadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnbxadd [RAX+1], EBP, R9D             # cmpnbxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnlxadd [RAX+1], EBP, R9D             # cmpnlxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnoxadd [RAX+1], EBP, R9D             # cmpnoxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnpxadd [RAX+1], EBP, R9D             # cmpnpxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnsxadd [RAX+1], EBP, R9D             # cmpnsxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpnzxadd [RAX+1], EBP, R9D             # cmpnzxadd DWORD PTR [rax+0x1],r13d,r9d
    cmppxadd [RAX+1], EBP, R9D              # cmppxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpsxadd [RAX+1], EBP, R9D              # cmpsxadd DWORD PTR [rax+0x1],r13d,r9d
    cmpzxadd [RAX+1], EBP, R9D              # cmpzxadd DWORD PTR [rax+0x1],r13d,r9d
    enqcmd R14D, ZMMWORD PTR [RAX+1]        # enqcmd r14d,[eax+0x1]
    lar R11, R8W                            # lar    r11,r8
    movmskpd R9, XMM0                       # movmskpd r9d,xmm0
    pmovmskb R10, MM2                       # pmovmskb r10d,mm2
    tpause RDX                              # tpause EDX
    umwait RBP                              # umwait EBP


C2:
    # C2. Confusing an operand and a label (23)
    call YMMWORD PTR [1]
    ja BYTE PTR [1]
    jae DWORD PTR [1]
    jb QWORD PTR [1]
    jbe BYTE PTR [1]
    je ZMMWORD PTR [1]
    jecxz QWORD PTR [1]
    jge ZMMWORD PTR [1]
    jl BYTE PTR [1]
    jle BYTE PTR [1]
    jne [1]
    jno BYTE PTR [1]
    jnp [1]
    jns [1]
    jo BYTE PTR [1]
    jp BYTE PTR [1]
    jrcxz DWORD PTR [1]
    js YMMWORD PTR [1]
    jmp XMMWORD PTR [1]
    loop DWORD PTR [1]
    loope QWORD PTR [1]
    loopne ZMMWORD PTR [1]
    xbegin BYTE PTR [1]

C3:
    # C3. Ignoring pointer directives  (29)
    aesencwide128kl XMMWORD PTR [1]
    aesencwide256kl YMMWORD PTR [1]
    aesdecwide128kl YMMWORD PTR [1]
    aesdecwide256kl BYTE PTR [1]
    fldenv ZMMWORD PTR [1]
    fnsave DWORD PTR [1]
    frstor ZMMWORD PTR [1]
    fxsave XMMWORD PTR [1]
    fnstenv DWORD PTR [1]
    fxrstor WORD PTR [1]
    fxsave64 XMMWORD PTR [1]
    fxrstor64 ZMMWORD PTR [1]
    ldtilecfg DWORD PTR [1]
    lgdt XMMWORD PTR [1]
    lidt ZMMWORD PTR [1]
    sgdt YMMWORD PTR [1]
    sttilecfg QWORD PTR [1]
    xsave WORD PTR [1]
    xrstor YMMWORD PTR [1]
    xsavec DWORD PTR [1]
    xsaves WORD PTR [1]
    xrstors ZMMWORD PTR [1]
    xsave64 ZMMWORD PTR [1]
    xrstor64 BYTE PTR [1]
    xsavec64 BYTE PTR [1]
    xsaveopt DWORD PTR [1]
    xsaves64 YMMWORD PTR [1]
    xrstors64 QWORD PTR [1]
    xsaveopt64 YMMWORD PTR [1]






