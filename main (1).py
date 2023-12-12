#A function to classify machine code

def identification(code2bin):
  if (code2bin[:2] == "00"):  #init
    rt = code2bin[2:4]
    imm = code2bin[4:]

    rt_int = int(rt, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: init ${rt_int}, {imm_int}')
#Init
  elif (code2bin[:4] == "0100"):
    rt = code2bin[4:6]
    rs = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    print(f'Instruction: add ${rt_int}, ${rs_int}')
#add
  elif (code2bin[:4] == "0101"):
    rt = code2bin[4:6]
    rs = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    print(f'Instruction: sub ${rt_int}, ${rs_int}')
#add
#sub
  elif (code2bin[:4] == "0111"):
    rs = code2bin[4:6]
    rt = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)

    print(f'Instruction: st ${rt_int}, (${rs_int})')
#st
  elif (code2bin[:4] == "1000"):
    rt = code2bin[4:6]
    rs = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)

    print(f'Instruction: ld ${rt_int}, (${rs_int})')
  #ld
  elif (code2bin[:4] == "1001"):
    rt = code2bin[4:6]
    imm = code2bin[6:]
    if (imm == '10'): imm_int = -2
    elif (imm == '11'): imm_int = -1
    else: imm_int = int(imm, 2)
    rt_int = int(rt, 2)

    print(f'Instruction: addi ${rt_int}, {imm_int}')
#addi
  elif (code2bin[:4] == "1010"):
    rt = code2bin[4:6]
    rs = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)

    print(f'Instruction: steal  ${rt_int}, ${rs_int}')
#steal
  elif (code2bin[:4] == "1011"):
    rt = code2bin[4:6]
    rs = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)

    print(f'Instruction: set ${rt_int}, ${rs_int}')
#set
  elif (code2bin[:4] == "1100"):
    rt = code2bin[4:6]
    imm = code2bin[6:]

    rt_int = int(rt, 2)
    imm_int = int(imm, 2)

    print(f'Instruction: bgt ${rt_int}, ${imm_int}')
#bgt
  elif (code2bin[:4] == "1101"):
    imm = code2bin[4:]

    imm_int = int(imm, 2)

    print(f'Instruction: bltzr0, {imm_int}')
#bltzr0
  elif (code2bin[:4] == "1111"):
    print('Instruction: Halt ')

#A function to compute assembly

def function(PC, op="0000", rs="00", rt="00", imm=0):
  if op == "00":  #init
    registers[rt] = imm
    return registers[rt]  #Init
  elif op == "0100":  #add
    registers[rt] = registers[rt] + registers[rs]
    return registers[rt]  #add
  elif op == "0101":  #sub
    registers[rt] = registers[rt] - registers[rs]
    return registers[rt]  #sub
  elif op == "0111":  #st
    print(f'R1: {registers["01"]}')
    print(f'R3: {registers["11"]}')
    Memlist[(hex((registers[rs]))[2:].zfill(3))] = registers[rt]

    print(f' Updated Memory: {hex(registers[rs])} = {registers[rt]}')

  #st
  elif op == "1000":  #ld
    registers[rt] = Memlist[hex(registers[rs])[2:].zfill(3)]

    print(f' Updated Memory: {registers[rt]} ={hex(registers[rs])}')
    #ld
  elif op == "1001":  #addi
    registers[rt] = registers[rt] + imm
    return registers[rt]  #addi
  elif op == "1010":  #steal
    if bin(registers[rs])[-1] == '1':
      registers[rt] += 1
    registers[rs] = (registers[rs] % 0x100000000) >> 1
    if (len(bin(registers[rt])) > 16):
      registers[rt] = int(bin(registers[rt])[:16], 2)
    registers[rt] = int(bin(registers[rt])[2:][-1].zfill(16))
    return registers[rt]  #steal
  elif op == "1011":  #set
    registers[rt] = registers[rs]
    return registers[rt]  #set
  elif op == "1100":  #bgt
    if registers[rt] > imm_int:
      PC = PC + 1
    return PC  #bgt
  elif op == "1101":  #bltzr0
    print(registers['00'])
    if registers['00'] >= 0:
      PC = PC - (3 + imm_int)
      return PC
    else:
      return PC  #bltzr0
  elif op == "1111":  #halt
    print("HALT")
    quit()  #halt

#A function to read a .txt file
def readASM(name):
  pop = 0
  name += ".txt"
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
imm = 0
pop = 0
b = 0
run = False
stats = ALU = J = B = M = O = 0
RT = IT = JT = 0

#Creating a list for PC addresses
for i in range(0x0000, 0x0000 + 50 * 4, 4):
  PClist.append(i)
for i in range(0x00, 0x00 + 64, 1):
  Memlist[hex(i)[2:].zfill(3)] = 0

#Initializing registers 0-3 with 0
registers = {"00": 0, "01": 0, "10": 0, "11": 0}

name = input("Enter Filename to assemble: ")
#name = "Project1-V2"

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

  temp = int(instruction, 16)
  code2bin = bin(temp)
  code2bin = code2bin[2:].zfill(8)  # op code
  print(code2bin)
  new = identification(code2bin)

  #print(new)

  #beq, bne, blt
  if code2bin[:4] == '1011' or code2bin[:4] == '1100':
    brnch = True

  if code2bin[:4] == "0111" or code2bin[0:4] == "1000":  #sw and lw
    store = True

  if code2bin[:2] == "00":
    op = code2bin[0:2]
    rt = code2bin[2:4]
    imm = code2bin[4:]
    rt_int = int(rt, 2)
    imm_int = int(imm, 2)

    machineCode = op + rt + imm

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

  elif code2bin[
      0] == "0" or code2bin[:
                            4] == "1000" or code2bin[:
                                                     4] == "1010" or code2bin[:
                                                                              4] == "1011":
    op = code2bin[0:4]
    rt = code2bin[4:6]
    rs = code2bin[6:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)

    machineCode = op + rt + rs
    srl = False
    brnch = False
    RT += 1
    ALU += 1

  elif code2bin[0] == "1":
    if code2bin[:4] == '1111':
      op = code2bin[:4]
      imm = code2bin[4:]
      imm_int = int(imm, 2)
    elif code2bin[:4] == '1101':
      op = code2bin[0:4]
      imm = code2bin[4:]
      imm_int = int(imm, 2)
      brnch = True
    elif code2bin[:4] == '1100':
      op = code2bin[0:4]
      rt = code2bin[4:6]
      imm = code2bin[6:]
      if (imm == "10"): imm_int = -2
      elif (imm == "11"): imm_int = -1
      else: imm_int = int(imm, 2)
      brnch = True
    else:
      op = code2bin[0:4]
      rt = code2bin[4:6]
      imm = code2bin[6:]
      if (imm == "10"): imm_int = -2
      elif (imm == "11"): imm_int = -1
      else: imm_int = int(imm, 2)
      rt_int = int(rt, 2)
      rs_int = int(rs, 2)

      machineCode = op + rt + imm
      srl = False
      ALU += 1
      RT += 1
      
  print("            Hex: 0x%s" % hex(int(machineCode, base=2))[2:].zfill(2))
  print("     Current PC: 0x%s" % (hex(InstrMem[PC][0])[2:].zfill(8)))
  if brnch is True:
    PC = function(PC, op, rs, rt, imm_int)
    brnch = False
  else:
    update = function(PC, op, rs, rt, imm_int)
    print("R-%02d updated to: %s" % (rt_int, update))
  PC += 1

  if PC <= int(hex(InstrMem[len(InstrMem) - 1][0])[2:], base=16) / 4:
    print("      Target PC: 0x%s" % (hex(InstrMem[PC][0])[2:].zfill(8)))

  else:
    print("\n\n")
    print("\t>>>End of Instructions<<<")

  print("op: %s" % op)
  print("rs: %s" % rs)
  print("rt: %s" % rt)
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
