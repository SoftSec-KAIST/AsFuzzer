#!/bin/bash

function get_num_of_lines()
{
    target=$1
    str=$2

    echo $(cat $target/*  | grep "$str" | awk -F':' '{print $1}' | sort -u | wc -l)
}
function gas_intel_err()
{
    target=$1
    arch=$2
    org=$3

    # mnemonic
    op1=$(get_num_of_lines $target "64-bit")
    op2=$(get_num_of_lines $target "invalid instruction mnemonic")
    op3=$(get_num_of_lines $target "suffix")

    num1=$(get_num_of_lines $target "too many")
    num2=$(get_num_of_lines $target "unsupported syntax")

    # operand size
    size=$(get_num_of_lines $target "size")

    # operand type
    type1=$(get_num_of_lines $target "type")
    type2=$(get_num_of_lines $target "immediate operands are allowed")

    op=$(expr $op1 + $op2 + $op3)
    num=$(expr $num1 + $num2)
    type=$(expr $type1 + $type2)

    echo "$arch - $org gas $op $num $size $type "
}


function clang_intel_err()
{
    target=$1
    arch=$2
    org=$3

    # mnemonic
    op1=$(get_num_of_lines $target  "64-bit")
    op2=$(get_num_of_lines $target  "invalid instruction mnemonic")
    num=$(get_num_of_lines $target  "number")

    # operand size
    size=$(get_num_of_lines $target  "ambiguous operand size")

    # operand type
    type=$(get_num_of_lines $target  "invalid operand for instruction")

    op=$(expr $op1 + $op2)
    echo "$arch - $org clang  $op $num $size $type "
}

function icc_intel_err()
{
    target=$1
    arch=$2
    org=$3
    # mnemonic
    op1=$(get_num_of_lines $target  "no such instruction")
    op2=$(get_num_of_lines $target  "invalid instruction suffix")

    # num of operands
    num=$(get_num_of_lines $target  "number")

    # operand size
    size=$(get_num_of_lines $target  "size")

    # operand type
    type=$(get_num_of_lines $target  "type")

    op=$(expr $op1 + $op2)
    echo "$arch - $org icc  $op $num $size $type "
}

function masm_intel_err()
{
    target=$1
    arch=$2
    org=$3
    # mnemonic
    op=$(get_num_of_lines $target  'symbol redefinition')

    # num of operands
    num=$(get_num_of_lines $target  'syntax error')

    # operand size
    size=$(get_num_of_lines $target  'size')

    # operand type
    type1=$(get_num_of_lines $target  'invalid instruction operands')
    type2=$(get_num_of_lines $target  'label')
    type3=$(get_num_of_lines $target  'expression expected')
    type4=$(get_num_of_lines $target  'invalid use of register')
    type5=$(get_num_of_lines $target  'immediate operand not allowed')
    type6=$(get_num_of_lines $target  'invalid data initializer')
    type7=$(get_num_of_lines $target  'NEAR indirect addressing')
    type=$(expr $type1 + $type2 + $type3 + $type4 + $type5 + $type6 + $type7)

    echo "$arch - $org masm  $op $num $size $type "
}


function gas_arm_err()
{
    target=$1
    arch=$2
    org=$3

    #mnemonic
    op=$(get_num_of_lines $target  'bad instruction')

    #num of operands
    num=$(get_num_of_lines $target  'garbage following instruction')

    #size
    size=$(get_num_of_lines $target  'immediate value out of range')

    #type
    type1=$(get_num_of_lines $target  'immediate expression require')
    type2=$(get_num_of_lines $target  'constant expression require')
    type3=$(get_num_of_lines $target  'immediate operand require')
    type4=$(get_num_of_lines $target  'shift expression expected')
    type5=$(get_num_of_lines $target  "expected: ']'")
    type6=$(get_num_of_lines $target  'integer register expected')
    type7=$(get_num_of_lines $target  'not support requested special purpose register')
    type8=$(get_num_of_lines $target  'invalid barrier type')
    type9=$(get_num_of_lines $target  'invalid floating-point constant')
    type10=$(get_num_of_lines $target  'predicate register')


    type11=$(get_num_of_lines $target  'cannot represent SMC relocation')
    type12=$(get_num_of_lines $target  'cannot represent')
    type13=$(get_num_of_lines $target  'bad expression')
    type14=$(get_num_of_lines $target  'invalid operand')
    type15=$(get_num_of_lines $target  'operand mismatch')
    type16=$(get_num_of_lines $target  'selected processor does not support')

    type16=$(get_num_of_lines $target  'different section')

    type=$(expr $type1 + $type2 + $type3 + $type4 + $type5 + $type6 + $type7 + $type8 + $type9 + $type10 + $type11 + $type12 + $type13 + $type14 + $type15 + $type16 )

    echo "$arch - $org gas $op $num $size $type "

}

function clang_arm_err()
{
    target=$1
    arch=$2
    org=$3

    #mneonic
    op1=$(get_num_of_lines $target  'invalid instruction')
    op2=$(get_num_of_lines $target  'instruction requires')

    #num of operands
    num1=$(get_num_of_lines $target  'too few')
    num2=$(get_num_of_lines $target  'too many operands')

    #size
    size1=$(get_num_of_lines $target  'immediate must be an integer in range')
    size2=$(get_num_of_lines $target  'operand must be an immediate in the range')
    size3=$(get_num_of_lines $target  'index must be an integer in range')

    #type
    type1=$(get_num_of_lines $target  'register expected')
    type2=$(get_num_of_lines $target  'prefetch hint expected')
    type3=$(get_num_of_lines $target  'invalid operand')
    type4=$(get_num_of_lines $target  'unrecognized instruction mnemonic')
    type5=$(get_num_of_lines $target  'expected label or encodable integer pc offset')
    type6=$(get_num_of_lines $target  'expected compatible register, symbol or integer in range')
    type7=$(get_num_of_lines $target  'expected compatible register or logical immediate')

    op=$(expr $op1 + $op2)
    num=$(expr $num1 + $num2)
    size=$(expr $size1 + $size2 + $size3)
    type=$(expr $type1 + $type2 + $type3 + $type4 + $type5 + $type6 + $type7)

    echo "$arch - $org clang $op $num $size $type "


}


function clang_mips_err()
{
    target=$1
    arch=$2
    org=$3

    #mneonic
    op1=$(get_num_of_lines $target  'unknown instruction')
    op2=$(get_num_of_lines $target  'instruction requires a CPU feature not currently')

    #num of operands
    num=$(get_num_of_lines $target  'too few')

    #type
    type1=$(get_num_of_lines $target  'invalid operand')
    type2=$(get_num_of_lines $target  'expected 32-bit signed immediate')

    op=$(expr $op1 + $op2)
    type=$(expr $type1 + $type2)

    echo "$arch - $org clang $op $num $size $type "

}

echo 'x86 assemblytesting'

gas_intel_err "asfuzzer_data/clang/i386/log/gas" 'x86' 'clang'
icc_intel_err "asfuzzer_data/clang/i386/log/icc" 'x86' 'clang'
masm_intel_err "asfuzzer_data/clang/i386/log/masm" 'x86' 'clang'

clang_intel_err "asfuzzer_data/gas/i386/log/clang" 'x86' 'gas'
icc_intel_err "asfuzzer_data/gas/i386/log/icc" 'x86' 'gas'
masm_intel_err "asfuzzer_data/gas/i386/log/masm" 'x86' 'gas'

clang_intel_err "asfuzzer_data/icc/i386/log/clang" 'x86' 'icc'
gas_intel_err "asfuzzer_data/icc/i386/log/gas" 'x86' 'icc'
masm_intel_err "asfuzzer_data/icc/i386/log/masm" 'x86' 'icc'

clang_intel_err "asfuzzer_data/masm/i386/log/clang" 'x86' 'masm'
gas_intel_err "asfuzzer_data/masm/i386/log/gas" 'x86' 'masm'
icc_intel_err "asfuzzer_data/masm/i386/log/icc" 'x86' 'masm'

echo 'x86-64 assembly testing'

gas_intel_err "asfuzzer_data/clang/intel/log/gas" 'x86-64' 'clang'
icc_intel_err "asfuzzer_data/clang/intel/log/icc" 'x86-64' 'clang'
masm_intel_err "asfuzzer_data/clang/intel/log/masm" 'x86-64' 'clang'

clang_intel_err "asfuzzer_data/gas/intel/log/clang" 'x86-64' 'gas'
icc_intel_err "asfuzzer_data/gas/intel/log/icc" 'x86-64' 'gas'
masm_intel_err "asfuzzer_data/gas/intel/log/masm" 'x86-64' 'gas'

clang_intel_err "asfuzzer_data/icc/intel/log/clang" 'x86-64' 'icc'
gas_intel_err "asfuzzer_data/icc/intel/log/gas" 'x86-64' 'icc'
masm_intel_err "asfuzzer_data/icc/intel/log/masm" 'x86-64' 'icc'

clang_intel_err "asfuzzer_data/masm/intel/log/clang" 'x86-64' 'masm'
gas_intel_err "asfuzzer_data/masm/intel/log/gas" 'x86-64' 'masm'
icc_intel_err "asfuzzer_data/masm/intel/log/icc" 'x86-64' 'masm'

echo 'arm assembly testing'

clang_arm_err "asfuzzer_data/gas/arm/log/clang" 'arm' 'gas'
gas_arm_err "asfuzzer_data/clang/arm/log/gas" 'arm' 'clang'

echo 'aarch64 assembly testing'

clang_arm_err "asfuzzer_data/gas/aarch64/log/clang" 'aarch64' 'gas'
gas_arm_err "asfuzzer_data/clang/aarch64/log/gas" 'aarch64' 'clang'


echo "mips assembly testing"

clang_mips_err "asfuzzer_data/gas/mips/log/clang" 'mips' 'gas'
gas_arm_err "asfuzzer_data/clang/mips/log/gas" 'mips' 'clang'
