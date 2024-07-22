../../bin/clang -c case1.s -o case1_clang.o 2> /dev/null
../../bin/as case1.s -o case1_gas.o 2> /dev/null
../../bin/icc64 -c case1.s -o case1_icc.o -diag-disable=10441 2> /dev/null
wine64 ../../bin/masm64 /Fo case1_masm.o /c case1.asm 2> /dev/null
