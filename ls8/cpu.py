"""CPU functionality."""

import sys

HLT = 0b00000001 # stop
LDI = 0b10000010 # sets a specified register to a value
PRN = 0b01000111 # print
ADD = 0b10100000 # add
SUB = 0b10100001 # subtract
MUL = 0b10100010 # multiply
PUSH = 0b01000101 # push onto the stack
POP = 0b01000110 # pop off the stack
CALL = 0b01010000 # call
RET = 0b00010001 # return
CMP = 0b10100111 # compare
JMP = 0b01010100 # jump
JEQ = 0b01010101 # equal
JNE = 0b01010110 # not equal

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # ram 
        self.reg = [0] * 8 # temp value holder 
        self.pc = 0 #program counter 
        self.sp = 7 #stack pointer 
        self.running = True
        self.flag = 0b00000000 #marker used for comparison  
        #PROGRAM Counter, address of the currently executing instruction 
                    #accept the address to read and return the value stored there. 
    #variables in hardware. known as "registers"
    # there are a fixed number of reigsters 
    #they have fixed names 
    # r0, r1, r2,....r6, r7 

    #accepts the address to read and return the value stored there. 
    def ram_read(self, address):
        return self.ram[address]

    #accepts a value to write, and the address to write it to 
    def ram_write(self, value, address):
        self.ram[address] = value 

         

    def load(self, filename):
        with open(filename, "r") as file:
            address = 0 
            for line in file:
                split_file = line.split("#")[0].strip()
                if split_file  == "":
                    continue
                self.ram[address] = int(split_file, 2)
                address += 1


    def alu(self, op, reg_a, reg_b): #math operations 
        """ALU operations."""
    #were going to put two numbers in the register and compare them 
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        #subtract 
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        #multiply 
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #compare 
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
               
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010

            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b000000100
        else:
            raise Exception("Unsupported ALU operation")
    
    def trace(self): #read back the last things that were run 
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running: 
            instruction_register = self.ram_read(self.pc) #instruction register, copy of the currently executing instruction 

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction_register == HLT: #halt the cpu and exit the emulator 
                self.running = False
            elif instruction_register == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == SUB:
                self.alu("SUB", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == PRN: #print numericc value stored in the given register 
                print(self.reg[operand_a])
                self.pc += 2   
            elif instruction_register == LDI: #set the value of the register to an integer 
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction_register == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3 
            elif instruction_register == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == JMP:
                self.pc = self.reg[operand_a]
            elif instruction_register == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif instruction_register == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif instruction_register == PUSH:
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[operand_a], self.reg[self.sp]) 
                self.pc += 2
            elif instruction_register == POP:
                self.reg[operand_a] = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
                self.pc += 2
            elif instruction_register == CALL:
                self.reg[self.sp] -= 1
                self.ram_write(self.pc + 2, self.reg[self.sp])
                self.pc = self.reg[operand_a]
            elif instruction_register == RET:
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1 
            else:
                print("Instruction not valid")
        
            
