import argparse
import re
import sys

opcodes = {
    'addi': '001000', 'beq': '000100', 'bne': '000101', 'lw': '100011', 'sw': '101011'
}

funct_codes = {
    'add': '100000', 'sub': '100010', 'sll': '000000', 'srl': '000010', 'slt': '101010'
}

register_aliases = {
    '$zero': '00000', '$v0': '00010', '$v1': '00011', '$a0': '00100',
}

def parse_instruction(instruction):
    """Parse a single instruction and convert it to binary."""
    instruction = instruction.strip()

    match = re.match(r'(\w+)\s+(.+)', instruction)
    if not match:
        return '!!! Invalid Input !!!'

    opcode, args = match.groups()

    if opcode in funct_codes:
        return process_r_type(opcode, args)
    elif opcode in opcodes:
        return process_i_type(opcode, args)
    else:
        return '!!! Invalid Input !!!'

def process_r_type(opcode, args):
    """Process R-Type instructions."""
    try:
        rd, rs, rt = args.split(',')
        rd = register_to_bin(rd)
        rs = register_to_bin(rs)
        rt = register_to_bin(rt)
        return f"000000{rs}{rt}{rd}00000{funct_codes[opcode]}"
    except Exception:
        return '!!! Invalid Input !!!'

def process_i_type(opcode, args):
    """Process I-Type instructions."""
    try:
        rt, rs, imm = args.split(',')
        rt = register_to_bin(rt)
        rs = register_to_bin(rs)
        imm = imm_to_bin(imm)
        return f"{opcodes[opcode]}{rs}{rt}{imm}"
    except Exception:
        return '!!! Invalid Input !!!'

def register_to_bin(reg):
    """Convert a register to its binary representation."""
    if reg in register_aliases:
        return register_aliases[reg]
    elif re.match(r'\$\d+', reg):
        reg_num = int(reg[1:])
        return f"{reg_num:05b}"
    else:
        raise ValueError('Invalid register')

def imm_to_bin(imm):
    """Convert an immediate value to 16-bit binary (two's complement if needed)."""
    imm_val = int(imm)
    if imm_val < 0:
        imm_val = (1 << 16) + imm_val
    return f"{imm_val:016b}"

def main():
    parser = argparse.ArgumentParser(description='MIPS to Machine Code Converter.')
    parser.add_argument('--file', type=str, required=True, help='Input file containing MIPS instructions.')
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as infile, open('out_code.txt', 'w') as outfile:
            for line in infile:
                binary_code = parse_instruction(line)
                if 'Invalid Input' in binary_code:
                    outfile.write(binary_code + '\n')
                    sys.exit()
                outfile.write(binary_code + '\n')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

if __name__ == '__main__':
    main()
