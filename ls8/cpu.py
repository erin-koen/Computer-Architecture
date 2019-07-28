"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0]*8
        self.ram = [0]*255
        self.PC = 0x00  # Program Counter
        self.IR = 0X00  # Instruction register

    def ram_read(self, MAR):  # Memory Address Register
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):  # memory data register - what's actually there
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if len(sys.argv) is not 2:
            print(f'Check your syntax. Please run one file and call another.')

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split('#', 1)[0]
                    if num.strip() == '':
                        continue
                    # loaded into memory as base 10
                    self.ram[address] = int(num, 2)
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found.')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        # read memory at address PC, store it in IR

        # opcodes
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        running = True
        while running:
            self.IR = self.PC
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if self.ram[self.IR] == HLT:
                running = False
            elif self.ram[self.IR] == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif self.ram[self.IR] == PRN:
                print(self.reg[operand_a])
                self.PC += 2
            elif self.ram[self.IR] == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.PC += 3
