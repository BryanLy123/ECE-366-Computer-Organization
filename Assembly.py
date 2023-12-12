#A function to compute assembly instructions

def function(PC,
             typeInstr,
             op="000000",
             rs="00000",
             rt="00000",
             rd="00000",
             sh="00000",
             func="000000",
             imm=0):
  if op == "001000":  #addi
    registers[rt] = registers[rs] + imm
    return registers[rt]

  elif func == "101010":  #slt
    if registers[rs] < registers[rt]:
      registers[rd] = 1
    else:
      registers[rd] = 0
    return registers[rd]

  elif op == "000100":  #beq
    if registers[rs] == registers[rt]:
      PC = PC + imm_int
      return PC
    else:
      return PC

  elif op == "000101":  #bne
    if registers[rs] != registers[rt]:
      PC = PC + imm_int
      return PC
    else:
      return PC

  elif op == "101011":  #sw
    Memlist[hex(registers[rs] + imm_int)[2:].zfill(8)] = registers[rt]

  elif op == "101010":  #blt
    if registers[rt] < registers[rs]:
      PC = PC + imm_int
      return PC
    else:
      return PC

  elif func == "100111":  #nor
    if registers[rs] < 0:
      registers[rs] = registers[rs] & 0b1111111111111111

    if registers[rs] > 32767:
      registers[rs] = registers[rs] - 65536

    binC = registers[rs] | registers[rt]
    binC = -binC - 1

    registers[rd] = binC

    if registers[rd] > 32767:
      registers[rd] = registers[rd] - 65536

    return registers[rd]

  elif func == "100010":  #sub
    registers[rd] = registers[rs] - registers[rt]
    return registers[rd]

  elif func == "100000":  #add
    registers[rd] = registers[rs] + registers[rt]
    return registers[rd]

  elif op == "100011":  #lw
    registers[rt] = Memlist[hex(registers[rs] + imm_int)[2:].zfill(8)]

  elif func == "000010":  #srl
    sh = int(sh, base=2)

    if sh > 32767:
      sh = registers[rs] - 65536

    registers[rd] = (registers[rs] % 0x100000000) >> sh

    return registers[rd]

  elif op == "001100":  #andi
   
    registers[rt] = registers[rs] & imm

    print("rt: %d" % registers[rt])

    return registers[rt]


#A function to read a .asm file
def readASM(name):
  pop = 0
  name += ".asm"
  file = open(name)
  instructions = file.readlines()

  for i in range(len(instructions)):

    firstLetter = instructions[i - pop][0]

    if firstLetter == '#' or firstLetter == '\n':
      instructions.pop(i - pop)
      pop += 1
      continue

    ind = instructions[i - pop].find('\t')
    ind2 = instructions[i - pop].find(' #')
    if ind != -1:
      instructions[i - pop] = instructions[i - pop][:ind]
    elif ind2 != -1:
      instructions[i - pop] = instructions[i - pop][:ind2]
    else:
      ind = instructions[i - pop].find('\n')
      instructions[i - pop] = instructions[i - pop][:ind]

    if instructions[i - pop][-1] == ':':
      labels[instructions[i - pop][:len(instructions[i - pop]) - 1]] = hex(
        PClist[i - pop])
      instructions.pop(i - pop)
      pop += 1

  return instructions

instructions = []
labels = {}
PClist = []
Memlist = {}
brnch = False
store = False
srl = False
PC = 0
op = ""
rs = ""
rt = ""
rd = ""
sh = ""
func = ""
imm = 0
pop = 0
b = 0
run = False
stats = ALU = J = B = M = O = 0
RT = IT = JT = 0

#Creating a list for PC addresses
for i in range(0x0000, 0x0000 + 50 * 4, 4):
  PClist.append(i)
for i in range(0x2000, 0x2000 + 128 * 4, 4):
  Memlist[hex(i)[2:].zfill(8)] = 0

#Initializing registers 0-31 with 0
registers = {
  "00000": 0,
  "00001": 0,
  "00010": 0,
  "00011": 0,
  "00100": 0,
  "00101": 0,
  "00110": 0,
  "00111": 0,
  "01000": 0,
  "01001": 0,
  "01010": 0,
  "01011": 0,
  "01100": 0,
  "01101": 0,
  "01110": 0,
  "01111": 0,
  "10000": 0,
  "10001": 0,
  "10010": 0,
  "10011": 0,
  "10100": 0,
  "10101": 0,
  "10110": 0,
  "10111": 0,
  "11000": 0,
  "11001": 0,
  "11010": 0,
  "11011": 0,
  "11100": 0,
  "11101": 0,
  "11110": 0,
  "11111": 0
}
#declaration of instructions
instrCode = {
  "addi": "I8",
  "slt": "R2a",
  "beq": "I4",
  "sw": "I2b",
  "blt": "I2a",
  "nor": "R27",
  "sub": "R22",
  "add": "R20",
  "lw": "I23",
  "andi": "Ic",
  "srl": "R02",
  "bne": "I5"
}

#name = input("Enter Filename to assemble: ")
#name = "Project1-V2"
name = "Test3"

instructions = readASM(name)

for i in range(len(instructions)):
  if instructions[i - pop][-1] == ":":
    instructions.pop(i - pop)
    pop += 1

InstrMem = list(zip(PClist, instructions))

print("\n")
print("*******Instruction Memory*******")
print("Memory Address || Instructions")
print("--------------------------------")
for i in range(len(instructions)):
  print("0x%s     :  %s" % (hex(InstrMem[i][0])[2:].zfill(8), InstrMem[i][1]))

#identification of labels when present
if len(labels.items()) > 0:
  print("\n")
  print("*******Labels*******")
  print("Labels   ||  Addresses")
  print("---------------------")
  for i, v in labels.items():
    v = v[2:].zfill(8)
    i = i.rjust(8, " ")
    print("%s  :  0x%s" % (i, v))

  print("---------------------")

print("\n")
print("**********************************")

#loop to run through list of instructions
while PC <= int(hex(InstrMem[len(InstrMem) - 1][0])[2:], base=16) / 4:
  b += 1

  #while loop for user input
  while (run == False):
    t = input()
    if t == "s":
      run = False
      break
    elif t == "n":
      run = True
    else:
      print("Invalid Input\n")
      print("Please Try Again\n")

  instruction = InstrMem[PC][1]
  print("    Instruction: %s" % instruction)

  if instruction[0] == 'b':
    brnch = True

  if instruction[:2] == 'sw' or instruction[:2] == 'lw':
    store = True

  if instruction[:3] == 'srl':
    srl = True

  i = instruction.split(" ")
  temp = int(instrCode[i[0]][1:], base=16)

  code2bin = bin(temp)
  code2bin = code2bin[2:].zfill(6)  # op code or func

  typeInstr = instrCode[i[0]][0]  # I or R

  if instruction[0] == 'j':
    J += 1
    JT += 1

  if typeInstr == "I":

    rd = 0
    sh = 0
    func = 0
    op = code2bin

    rt_int = int(i[1][1:len(i[1]) - 1])
    rt = bin(rt_int)[2:].zfill(5)

    if store == False and brnch == False:
      rs_int = int(i[2][1:len(i[2]) - 1])
      rs = bin(rs_int)[2:].zfill(5)

    elif store == True:
      memPart = i[2].split('(')
      print(memPart)
      rs_int = int(memPart[1][1:-1])
      rs = bin(rs_int)[2:].zfill(5)

      if memPart[0][:2] == "0x":
        imm = memPart[0][2:]
        imm_int = int(memPart[0][2:], base=16)
        imm = bin(imm_int)[2:].zfill(16)

      else:
        imm_int = int(memPart[0], base=16)
        imm = bin(imm_int)[2:].zfill(16)

    if brnch == False and store == False:
      imm_int = int(i[3])
      imm = bin(imm_int & 0b1111111111111111)[2:].zfill(16)

    elif brnch == True:

      rs_int = int(i[2][1:len(i[2]) - 1])
      rs = bin(rs_int)[2:].zfill(5)
      imm_int = int(labels[i[3]][2:], base=16) - InstrMem[PC][0] - 4

      imm_int /= 4
      imm = int(imm_int)
      imm = bin(imm & 0b1111111111111111)[2:].zfill(16)

    if brnch == True:
      PC = function(PC, typeInstr, op, rs, rt, imm=imm_int)

    else:
      update = function(PC, typeInstr, op, rs, rt, imm=imm_int)

    machineCode = op + rs + rt + imm
    store = False

    IT += 1
    if op == "101010":
      O += 1
    #condition for beq, bne, and blt
    if op == "000100" or op == "000101" or op == "101010":
      B += 1
    #condition for sw and lw
    elif op == "101011" or op == "100011":
      M += 1
    else:
      ALU += 1

  elif typeInstr == "R":
    print("here in R")
    op = "00000"
    sh = "00000"
    rt = "00000"
    func = code2bin

    rd_int = int(i[1][1:len(i[1]) - 1])
    rd = bin(rd_int)[2:].zfill(5)

    rs_int = int(i[2][1:len(i[2]) - 1])
    rs = bin(rs_int)[2:].zfill(5)

    if srl == False:
      rt_int = int(i[3][1:len(i[3])])
      rt = bin(rt_int)[2:].zfill(5)
    else:
      sh = bin(int(i[3]))[2:].zfill(5)

    update = function(PC, typeInstr, op, rs, rt, rd, sh, func=func)
    machineCode = op + rs + rt + rd + sh + func
    
    srl = False

    RT += 1
    if func == "101010":#condtiion for slt
      O += 1
    else:
      ALU += 1

  PC = int(PC)

  print("            Hex: 0x%s" % hex(int(machineCode, base=2))[2:].zfill(8))
  print("     Current PC: 0x%s" % (hex(InstrMem[PC][0])[2:].zfill(8)))

  if typeInstr == "I":
    if brnch is True:
      brnch = False
    else:
      print("R-%02d updated to: %s" % (rt_int, update))
  elif typeInstr == "R":
    print("R-%02d updated to: %s" % (rd_int, update))

  PC += 1
  
  if PC <= int(hex(InstrMem[len(InstrMem) - 1][0])[2:], base=16) / 4:
    print("      Target PC: 0x%s" % (hex(InstrMem[PC][0])[2:].zfill(8)))
  else:
    print("\n\n")
    print("\t>>>End of Instructions<<<")

  print("op: %s" % op)
  print("rs: %s" % rs)
  print("rt: %s" % rt)
  print("rd: %s" % rd)
  print("sh: %s" % sh)
  print("func: %s" % func)
  print("**********************************")

print("\n")
print("*******Registers*******")
print("Register || Value")
print("-----------------------")
#output of register values
for i, v in registers.items():
  print("R-%02d     :  %3d" % (int(i, base=2), v))

print("--------------------------")
print("**********Memory**********")
print("Address     ||   Value")
print("--------------------------")
#output of memory content
for i, v in Memlist.items():
  print("0x%s   :  %3d" % (i, v))

print("-------------------")
#output of statistics
print("\n")
print("*****Instruction Statistics*****")
print("--------------------------")

stats = ALU + J + B + M + O
print("Total: %d" % stats)
print("ALU: %d" % ALU)
print("Jump: %d" % J)
print("Branch: %d" % B)
print("Memory: %d" % M)
print("Other: %d" % O)
print("--------------------------")

#output of count
TSF = RT + IT + JT
print("\n")
print("*****Instruction Count*****")
print("--------------------------")
print("Instructions so far: %d" % TSF)
print("R-Type: %d" % RT)
print("I-Type: %d" % IT)
print("J-Type: %d" % JT)
print("-------------------")
