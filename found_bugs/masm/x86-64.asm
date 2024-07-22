;#########################################################################
; Total: 48 (C1:6, C2:0, C3:42, C4:0, C5:0, C6:0)
; Compile:      wine64 ../../bin/masm64 /c x86-64.asm
; disassembly:  ../../bin/objdump -d -M intel --no-show-raw-insn x86-64.obj
;#########################################################################

.code

C1:
    ; C1. Using wrong register(s) (6)
    incsspd R15                                      ; incsspd R15D
    lods ZMMWORD PTR [1]                             ; lods   eax,DWORD PTR ds:[rsi]
    lwpins EBP, DWORD PTR [1], 1                     ; lwpins eax,DWORD PTR ds:0x1,0x1
    rdsspd RDX                                       ; rdsspd EDX
    scas YMMWORD PTR [1]                             ; scas   eax,DWORD PTR es:[rdi]
    stos YMMWORD PTR [1]                             ; stos   DWORD PTR es:[rdi],eax

C3:
    ; C3. Ignoring pointer directives (42)
    aesdecwide128kl QWORD PTR [1]                  ; aesdecwide128kl [RAX+0x1]
    aesdecwide256kl XMMWORD PTR [1]                ; aesdecwide256kl [RAX+0x1]
    aesencwide128kl DWORD PTR [1]                    ; aesencwide128kl [RAX]
    aesencwide256kl ZMMWORD PTR [1]                  ; aesencwide256kl [RAX]
    cldemote XMMWORD PTR [1]                       ; cldemote [RAX+0x1]
    clflush YMMWORD PTR [1]                        ; clflush [RAX+0x1]
    clflushopt YMMWORD PTR [1]                     ; clflushopt [RAX+0x1]
    clwb XMMWORD PTR [1]                           ; clwb [RAX+0x1]
    cmpxchg16b YMMWORD PTR [1]                       ; cmpxchg16b [RAX]
    fsave QWORD PTR [1]                            ; fsave [RAX+0x1]
    fldenv BYTE PTR [1]                            ; fldenv [RAX+0x1]
    fnsave YMMWORD PTR [1]                         ; fnsave [RAX+0x1]
    frstor XMMWORD PTR [1]                           ; frstor [RAX]
    fstenv BYTE PTR [1]                              ; fstenv [RAX]
    fxsave ZMMWORD PTR [1]                         ; fxsave [RAX+0x1]
    fnstenv WORD PTR [1]                           ; fnstenv [RAX+0x1]
    fxrstor DWORD PTR [1]                          ; fxrstor [RAX+0x1]
    fxsave64 BYTE PTR [1]                          ; fxsave64 [RAX+0x1]
    fxrstor64 XMMWORD PTR [1]                      ; fxrstor64 [RAX+0x1]
    invlpg ZMMWORD PTR [1]                           ; invlpg BYTE PTR ds:0x1, invlpg [RAX]
    ldtilecfg DWORD PTR [1]                          ; ldtilecfg ds:0x1/ ldtilecfg [RAX]
    prefetch WORD PTR [1]                          ; prefetch [RAX+0x1]
    prefetchw XMMWORD PTR [1]                      ; prefetchw [RAX+0x1]
    prefetchnta DWORD PTR [1]                      ; prefetchnta [RAX+0x1]
    prefetcht0 ZMMWORD PTR [1]                       ; prefetcht0 [RAX]
    prefetcht1 YMMWORD PTR [1]                     ; prefetcht1 [RAX+0x1]
    prefetcht2 QWORD PTR [1]                         ; prefetcht2 [RAX]
    prefetchwt1 QWORD PTR [1]                      ; prefetchwt1 [RAX+0x1]
    sgdt YMMWORD PTR [1]                           ; ssgdt   ds:0x1; gdt [RAX+0x1]
    sidt YMMWORD PTR [1]                           ; sidt   ds:0x1
    sttilecfg YMMWORD PTR [1]                        ; sttilecfg ds:0x1 , sttilecfg [RAX]
    xrstor ZMMWORD PTR [1]                         ; xrstor [RAX+0x1]
    xsavec XMMWORD PTR [1]                         ; xsavec [RAX+0x1]
    xsaves XMMWORD PTR [1]                         ; xsaves [RAX+0x1]
    xrstors QWORD PTR [1]                          ; xrstors [RAX+0x1]
    xsave64 XMMWORD PTR [1]                          ; xsave64 [RAX]
    xrstor64 WORD PTR [1]                          ; xrstor64 [RAX+0x1]
    xsavec64 YMMWORD PTR [1]                       ; xsavec64 [RAX+0x1]
    xsaveopt YMMWORD PTR [1]                       ; xsaveopt [RAX+0x1]
    xsaves64 XMMWORD PTR [1]                         ; xsaves64 [RAX]
    xrstors64 ZMMWORD PTR [1]                        ; xrstors64 [RAX]
    xsaveopt64 ZMMWORD PTR [1]                       ; xsaveopt64 [RAX]

    end
