"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.running = False
        self.branchtable = {
            0b00000001: self.handle_HLT,
            0b10000010: self.handle_LDI,
            0b01000111: self.handle_PRN,
            0b01000101: self.handle_PSH,
            0b01000110: self.handle_POP,
            0b01010000: self.handle_CAL,
            0b00010001: self.handle_RET,
            0b10100000: self.handle_ADD,
            0b10100010: self.handle_MUL,
            # * ------------------------
            
        }

    def load(self, prog):
        prog = "examples/" + prog + ".ls8"
        addr = 0

        with open(prog) as file:

            print(f"file: {prog}")

            for line in file:
                line = line.split("#")
                line = line[0].strip()

                if line == "":
                    continue

                line = int(line, 2)
                self.ram[addr] = line
                addr += 1

        # sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    """
    # * Read, Write
    """

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

    """
    # * Halt, Load, Print
    """

    def handle_HLT(self, operand_a, operand_b):
        self.running = False

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_PRN(self, operand_a, operand_b):
        print(f"prints {self.reg[operand_a]}")

    """
    # * Push, Pop
    """

    def handle_PSH(self, operand_a, operand_b):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[operand_a], self.reg[self.sp])

    def handle_POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    """
    # * Call, Return
    """

    def handle_CAL(self, operand_a, operand_b):
        self.reg[self.sp] -= 1
        self.ram_write(self.pc + 2, self.reg[self.sp])
        self.pc = self.reg[operand_a]

    def handle_RET(self, operand_a, operand_b):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    """
    # * ALU
    """

    def handle_ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

'''
# * Sprint Challenge
'''

    def run(self):
        """Run the CPU."""

        self.running = True

        while self.running:

            inst = self.ram_read(self.pc)
            inst_len = ((inst & 0b11000000) >> 6) + 1

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if inst in self.branchtable:
                self.branchtable[inst](operand_a, operand_b)

            else:
                print(f"unknown instruction {inst}")

            if (
                not inst & 0b00010000
            ):  # ? what is this? --> call/ret doesn't work without it...
                self.pc += inst_len
