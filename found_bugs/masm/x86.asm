;############################################################################
; Total: 36 (C1:5, C2:0, C3:31, C4:0, C5:0, C6:0)
; Compile:      wine64 ../../bin/masm32 /c x86.asm
; disassembly:  ../../bin/objdump -d -M intel  --no-show-raw-insn --target coff-i386 x86.obj
;############################################################################

.model flat
.code

C1:
    ; C1. Using wrong register(s) (5)
    lods WORD PTR [EAX+1]                              ; lods [ESI]
    lwpval EBP, DWORD PTR [EAX+1], 1                   ; lwpval eax,DWORD PTR [eax+0x1],0x1
    lwpins EBP, DWORD PTR [1], 1                       ; lwpins eax,DWORD PTR ds:0x1,0x1
    scas YMMWORD PTR [EAX+1]                           ; scas [EDI]
    stos XMMWORD PTR [1]                               ; stos [EDI]


C3:
    ; C3. Ignoring pointer directives (31)
    aesdecwide128kl DWORD PTR [1]
    aesdecwide256kl BYTE PTR [EAX+1]
    aesencwide128kl QWORD PTR [1]
    aesencwide256kl XMMWORD PTR [1]
    clwb XMMWORD PTR [1]
    clflush XMMWORD PTR [1]
    clflushopt DWORD PTR [1]
    cldemote WORD PTR [1]
    invlpg XMMWORD PTR [1]
    fsave ZMMWORD PTR [1]
    fldenv ZMMWORD PTR [1]
    fnsave YMMWORD PTR [1]
    frstor QWORD PTR [1]
    fstenv BYTE PTR [EAX+1]
    fxsave BYTE PTR [1]
    fnstenv QWORD PTR [EAX+1]
    fxrstor XMMWORD PTR [1]
    prefetch QWORD PTR [EAX+1]
    prefetchw QWORD PTR [EAX]
    prefetchnta XMMWORD PTR [1]
    prefetcht0 QWORD PTR [EAX+1]
    prefetcht1 DWORD PTR [EAX]
    prefetcht2 DWORD PTR [1]
    prefetchwt1 QWORD PTR [EAX+1]
    xlat BYTE PTR [1]
    xrstor XMMWORD PTR [EAX+1]
    xsavec YMMWORD PTR [1]
    xsaves DWORD PTR [EAX+1]
    xrstors ZMMWORD PTR [EAX+1]
    xsaveopt DWORD PTR [EAX+11]
    xsave XMMWORD PTR [1]

    end
