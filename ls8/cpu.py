"""CPU functionality."""

import sys

# Binary for all operations
ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # General purpose registers
        self.reg = [0] * 8
        # Set the reg at index 7 to the keystroke instruction
        self.reg[7] = 0xFF
        # 256 bit ram
        self.ram = [0] * 256
        # Program Counter
        self.pc = 0
        # Flags
        self.fl = 0
        # Keep track of if the CPU is running for the halt function
        self.running = False

    def load(self, file_to_run):
        """Load a program into memory."""
        address = 0
        # Read the examples and load the instructions into the ram
        # Automatically adds examples/ to the filename in this instance
        # to make it easier, however hardcoding it would not always be
        # the best option.
        with open('examples/' + file_to_run, 'r') as f:
            # For each command...
            for line in f:
                # Ignore comments
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    # Grab the command out of the file
                    command = line.split(' ')[0]
                    # Convert binary command string to int value and load it into the ram
                    self.ram[address] = int(command, 2)
                    # increment the register address for the next command
                    address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        """Read the ram at a given position"""
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        """Write over the ram at a given position"""
        self.ram[mar] = mdr

    def handle_hlt(self):
        """Handle instruction to halt the current set of instructions"""
        print("CPU halted.")
        self.running = False
        self.pc += 1

    def handle_ldi(self, reg_num, imm_int):
        """Handle instruction to load the reg with an 8-bit immediate value"""
        self.reg[reg_num] = imm_int
        self.pc += 3

    def handle_prn(self, reg_num):
        """Handle intruction to print the value of the current reg"""
        print(self.reg[reg_num])
        self.pc += 2

    def run(self):
        """Run the CPU."""
        self.running = True
        # While not halted
        while self.running == True:
            # get the Instruction Register
            ir = self.ram_read(self.pc)
            # store the operands
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # dispatch the proper method based on the instruction
            if ir == HLT:
                self.handle_hlt()
            elif ir == LDI:
                self.handle_ldi(operand_a, operand_b)
            elif ir == PRN:
                self.handle_prn(operand_a)
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            else:
                print("Instruction not found, exiting program with error")
                sys.exit(1)

