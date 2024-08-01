###########################################################
# Total: 60 (C1:3, C2:24, C3:18, C4:0, C5:15, C6:0)
# Compile:      ../../bin/clang -m32 -c x86.s -o x86.o
# disassembly:  ../../bin/objdump -d -M intel --no-show-raw-insn x86.o
###########################################################

.intel_syntax noprefix

C1:
    # C1. Using wrong register(s) (3)
    enqcmd SP, ZMMWORD PTR [EAX+1]                      # enqcmd    sp,[bx+si+0x1]
    enqcmds SP, ZMMWORD PTR [EAX]                       # enqcmds   sp,[bx+si]
    movdir64b SP, ZMMWORD PTR [ECX]                     # movdir64b sp,[bx+di]

C2:
    # C2. Confusing an operand and a label (24)
    call XMMWORD PTR [1]
    ja BYTE PTR [1]
    jb QWORD PTR [1]
    jcxz YMMWORD PTR [1]
    je XMMWORD PTR [1]
    jecxz ZMMWORD PTR [1]
    jg BYTE PTR [1]
    jl XMMWORD PTR [1]
    jo YMMWORD PTR [1]
    jp XMMWORD PTR [1]
    js ZMMWORD PTR [1]
    jae WORD PTR [1]
    jbe DWORD PTR [1]
    jge WORD PTR [1]
    jle ZMMWORD PTR [1]
    jmp QWORD PTR [1]
    jne WORD PTR [1]
    jno WORD PTR [1]
    jnp WORD PTR [1]
    jns XMMWORD PTR [1]
    loop DWORD PTR [1]
    loope DWORD PTR [1]
    loopne YMMWORD PTR [1]
    xbegin WORD PTR [1]

C3:
    # C3. Ignoring pointer directives (18)
    aesdecwide128kl XMMWORD PTR [1]
    aesdecwide256kl BYTE PTR [1]
    aesencwide128kl ZMMWORD PTR [1]
    aesencwide256kl YMMWORD PTR [1]
    clrssbsy DWORD PTR [1]
    fldenv YMMWORD PTR [1]
    fnsave ZMMWORD PTR [1]
    frstor WORD PTR [1]
    fxsave BYTE PTR [1]
    fnstenv YMMWORD PTR [1]
    fxrstor QWORD PTR [1]
    rstorssp DWORD PTR [1]
    xrstor QWORD PTR [1]
    xrstors DWORD PTR [1]
    xsave XMMWORD PTR [1]
    xsavec BYTE PTR [1]
    xsaveopt BYTE PTR [1]
    xsaves QWORD PTR [1]

C5:
    # C5. Emitting invalid code (17)
    cmpbxadd DWORD PTR [1], EDI, EBP
    cmplexadd DWORD PTR [1], EDI, EBP
    cmplxadd DWORD PTR [1], EDI, EBP
    cmpnbexadd DWORD PTR [1], EDI, EBP
    cmpnbxadd DWORD PTR [1], EDI, EBP
    cmpbexadd DWORD PTR [1], EDI, EBP
    cmpnlxadd DWORD PTR [1], EDI, EBP
    cmpnoxadd DWORD PTR [1], EDI, EBP
    cmpnpxadd DWORD PTR [1], EDI, EBP
    cmpnsxadd DWORD PTR [1], EDI, EBP
    cmpnzxadd DWORD PTR [1], EDI, EBP
    cmpoxadd DWORD PTR [1], EDI, EBP
    cmppxadd DWORD PTR [1], EDI, EBP
    cmpsxadd DWORD PTR [1], EDI, EBP
    cmpzxadd DWORD PTR [1], EDI, EBP
    enqcmd BX, ZMMWORD PTR [1]
    enqcmds BX, ZMMWORD PTR [1]


