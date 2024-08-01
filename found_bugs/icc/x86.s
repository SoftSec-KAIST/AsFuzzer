###########################################################
# Total: 183 (C1:0, C2:3, C3:11, C4:169, C5:0, C6:0)
# Compile:      ../../bin/icc32 -c x86.s -o x86.o -diag-disable=10441
# disassembly:  ../../bin/objdump -d -M intel --no-show-raw-insn x86.o
###########################################################

.intel_syntax noprefix

C2:
    # C2. Confusing an operand and a label (3)
    loop XMMWORD PTR [1]
    loope XMMWORD PTR [1]
    loopne XMMWORD PTR [1]

C3:
    # C3. Ignoring pointer directives (11)
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
    # C4. Incorrect # of operands (169)
    div    AX, WORD PTR [EAX+1]
    vaddpd ZMM0, ZMM0, ZMM0, 1
    vaddps ZMM0, ZMM0, ZMM0, 1
    vaddsd XMM0, XMM0, XMM0, 1
    vaddss XMM0, XMM0, XMM0, 1
    vcomisd XMM0, XMM0, 1
    vcomiss XMM0, XMM0, 1
    vcvtdq2ps ZMM0, ZMM0, 1
    vcvtpd2dq YMM0, ZMM0, 1
    vcvtpd2ps YMM0, ZMM0, 1
    vcvtpd2qq ZMM0, ZMM0, 1
    vcvtpd2udq YMM0, ZMM0, 1
    vcvtph2ps ZMM0, YMM0, 1
    vcvtps2dq XMM0, [EAX]
    vcvtps2ph 1, 1, ZMM0, YMM0
    vcvtps2qq XMM0, [1]
    vcvtps2udq ZMM0, [EAX]
    vcvtqq2pd ZMM0, ZMM0, 1
    vcvtqq2ps YMM0, ZMM0, 1
    vcvtsd2si EBP, [1]
    vcvtsd2ss XMM0, XMM0, XMM0, 1
    vcvtsd2usi EBX, XMM0, 1
    vcvtsi2ss XMM0, XMM0, EBP, 1
    vcvtss2sd XMM0, XMM0, XMM0, 1
    vcvtss2si EBX, XMM0, 1
    vcvtss2usi ESI, XMM0, 1
    vcvttpd2dq YMM0, ZMM0, 1
    vcvttpd2qq ZMM0, ZMM0, 1
    vcvttpd2udq YMM0, ZMM0, 1
    vcvttps2dq YMM0, XMMWORD PTR [EAX]
    vcvttps2qq ZMM0, YMM0, 1
    vcvttps2udq ZMM0, ZMM0, 1
    vcvttps2uqq ZMM0, YMM0, 1
    vcvttsd2si ESI, [EAX+1]
    vcvttsd2usi ECX, XMM0, 1
    vcvttss2si EDX, XMM0, 1
    vcvttss2usi ESI, XMM0, 1
    vcvtudq2ps ZMM0, [1]
    vcvtuqq2pd ZMM0, ZMM0, 1
    vcvtuqq2ps YMM0, ZMM0, 1
    vcvtusi2ss XMM0, XMM0, EBP, 1
    vdivpd ZMM0, ZMM0, ZMM0, 1
    vdivps ZMM0, ZMM0, ZMM0, 1
    vdivsd XMM0, XMM0, XMM0, 1
    vdivss XMM0, XMM0, XMM0, 1
    vexp2pd ZMM0, ZMM0, 1
    vexp2ps ZMM0, ZMM0, 1
    vfixupimmpd ZMM0, ZMM0, ZMM0, 1, 1
    vfixupimmps 1, 1, ZMM0, ZMM0, ZMM0
    vfixupimmsd XMM0, XMM0, XMM0, 1, 1
    vfixupimmss XMM0, XMM0, XMM0, 1, 1
    vfmadd132pd ZMM0, ZMM0, ZMM0, 1
    vfmadd132ps ZMM0, ZMM0, ZMM0, 1
    vfmadd132sd XMM0, XMM0, XMM0, 1
    vfmadd132ss XMM0, XMM0, XMM0, 1
    vfmadd213pd ZMM0, ZMM0, ZMM0, 1
    vfmadd213ps ZMM0, ZMM0, ZMM0, 1
    vfmadd213sd XMM0, XMM0, XMM0, 1
    vfmadd213ss XMM0, XMM0, XMM0, 1
    vfmadd231pd ZMM0, ZMM0, ZMM0, 1
    vfmadd231ps ZMM0, ZMM0, ZMM0, 1
    vfmadd231sd XMM0, XMM0, XMM0, 1
    vfmadd231ss XMM0, XMM0, XMM0, 1
    vfmaddsub132pd ZMM0, ZMM0, ZMM0, 1
    vfmaddsub132ps ZMM0, ZMM0, ZMM0, 1
    vfmaddsub213pd ZMM0, ZMM0, ZMM0, 1
    vfmaddsub213ps ZMM0, ZMM0, ZMM0, 1
    vfmaddsub231pd ZMM0, ZMM0, ZMM0, 1
    vfmaddsub231ps ZMM0, ZMM0, ZMM0, 1
    vfmsub132pd ZMM0, ZMM0, ZMM0, 1
    vfmsub132ps ZMM0, ZMM0, ZMM0, 1
    vfmsub132sd XMM0, XMM0, XMM0, 1
    vfmsub132ss XMM0, XMM0, XMM0, 1
    vfmsub213pd ZMM0, ZMM0, ZMM0, 1
    vfmsub213ps ZMM0, ZMM0, ZMM0, 1
    vfmsub213sd XMM0, XMM0, XMM0, 1
    vfmsub213ss XMM0, XMM0, XMM0, 1
    vfmsub231pd ZMM0, ZMM0, ZMM0, 1
    vfmsub231ps ZMM0, ZMM0, ZMM0, 1
    vfmsub231sd XMM0, XMM0, XMM0, 1
    vfmsub231ss XMM0, XMM0, XMM0, 1
    vfmsubadd132pd ZMM0, ZMM0, ZMM0, 1
    vfmsubadd132ps ZMM0, ZMM0, ZMM0, 1
    vfmsubadd213pd ZMM0, ZMM0, ZMM0, 1
    vfmsubadd213ps ZMM0, ZMM0, ZMM0, 1
    vfmsubadd231pd ZMM0, ZMM0, ZMM0, 1
    vfmsubadd231ps ZMM0, ZMM0, ZMM0, 1
    vfnmadd132pd ZMM0, ZMM0, ZMM0, 1
    vfnmadd132ps ZMM0, ZMM0, ZMM0, 1
    vfnmadd132sd XMM0, XMM0, XMM0, 1
    vfnmadd132ss XMM0, XMM0, XMM0, 1
    vfnmadd213pd ZMM0, ZMM0, ZMM0, 1
    vfnmadd213ps ZMM0, ZMM0, ZMM0, 1
    vfnmadd213sd XMM0, XMM0, XMM0, 1
    vfnmadd213ss XMM0, XMM0, XMM0, 1
    vfnmadd231pd ZMM0, ZMM0, ZMM0, 1
    vfnmadd231ps ZMM0, ZMM0, ZMM0, 1
    vfnmadd231sd XMM0, XMM0, XMM0, 1
    vfnmadd231ss XMM0, XMM0, XMM0, 1
    vfnmsub132pd ZMM0, ZMM0, ZMM0, 1
    vfnmsub132ps ZMM0, ZMM0, ZMM0, 1
    vfnmsub132sd XMM0, XMM0, XMM0, 1
    vfnmsub132ss XMM0, XMM0, XMM0, 1
    vfnmsub213pd ZMM0, ZMM0, ZMM0, 1
    vfnmsub213ps ZMM0, ZMM0, ZMM0, 1
    vfnmsub213sd XMM0, XMM0, XMM0, 1
    vfnmsub213ss XMM0, XMM0, XMM0, 1
    vfnmsub231pd ZMM0, ZMM0, ZMM0, 1
    vfnmsub231ps ZMM0, ZMM0, ZMM0, 1
    vfnmsub231sd XMM0, XMM0, XMM0, 1
    vfnmsub231ss XMM0, XMM0, XMM0, 1
    vgetexppd ZMM0, ZMM0, 1
    vgetexpps ZMM0, ZMM0, 1
    vgetexpsd XMM0, XMM0, XMM0, 1
    vgetexpss XMM0, XMM0, XMM0, 1
    vgetmantpd 1, 1, ZMM0, ZMM0
    vgetmantps ZMM0, ZMM0, 1, 1
    vgetmantsd 1, 1, XMM0, XMM0, XMM0
    vgetmantss XMM0, XMM0, XMM0, 1, 1
    vmaxpd ZMM0, ZMM0, ZMM0, 1
    vmaxps ZMM0, ZMM0, ZMM0, 1
    vmaxsd XMM0, XMM0, XMM0, 1
    vmaxss XMM0, XMM0, XMM0, 1
    vminpd ZMM0, ZMM0, ZMM0, 1
    vminps ZMM0, ZMM0, ZMM0, 1
    vminsd XMM0, XMM0, XMM0, 1
    vminss XMM0, XMM0, XMM0, 1
    vmulpd ZMM0, ZMM0, ZMM0, 1
    vmulps ZMM0, ZMM0, ZMM0, 1
    vmulsd XMM0, XMM0, XMM0, 1
    vmulss XMM0, XMM0, XMM0, 1
    vrangepd 1, 1, ZMM0, ZMM0, ZMM0
    vrangeps 1, 1, ZMM0, ZMM0, ZMM0
    vrangesd 1, 1, XMM0, XMM0, XMM0
    vrangess 1, 1, XMM0, XMM0, XMM0
    vrcp28pd ZMM0, ZMM0, 1
    vrcp28ps ZMM0, ZMM0, 1
    vrcp28sd XMM0, XMM0, XMM0, 1
    vrcp28ss XMM0, XMM0, XMM0, 1
    vreducepd 1, 1, ZMM0, ZMM0
    vreduceps 1, 1, ZMM0, ZMM0
    vreducesd 1, 1, XMM0, XMM0, XMM0
    vreducess XMM0, XMM0, XMM0, 1, 1
    vrndscalepd ZMM0, ZMM0, 1, 1
    vrndscaleps 1, 1, ZMM0, ZMM0
    vrndscalesd 1, 1, XMM0, XMM0, XMM0
    vrndscaless XMM0, XMM0, XMM0, 1, 1
    vrsqrt28pd ZMM0, ZMM0, 1
    vrsqrt28ps ZMM0, ZMM0, 1
    vrsqrt28sd XMM0, XMM0, XMM0, 1
    vrsqrt28ss XMM0, XMM0, XMM0, 1
    vscalefpd ZMM0, ZMM0, ZMM0, 1
    vscalefps ZMM0, ZMM0, ZMM0, 1
    vscalefsd XMM0, XMM0, XMM0, 1
    vscalefss XMM0, XMM0, [EAX]
    vsqrtpd ZMM0, ZMM0, 1
    vsqrtps ZMM0, ZMM0, 1
    vsqrtsd XMM0, XMM0, XMM0, 1
    vsqrtss XMM0, XMM0, XMM0, 1
    vsubpd ZMM0, ZMM0, ZMM0, 1
    vsubps ZMM0, ZMM0, ZMM0, 1
    vsubsd XMM0, XMM0, XMM0, 1
    vsubss XMM0, XMM0, XMM0, 1
    vucomisd XMM0, XMM0, 1
    vucomiss XMM0, XMM0, 1
    vcvtpd2uqq ZMM0, ZMM0, 1
    vcvtps2pd ZMM0, YMM0, 1
    vcvtps2uqq ZMM0, YMM0, 1
    vcvttpd2uqq ZMM0, ZMM0, 1


