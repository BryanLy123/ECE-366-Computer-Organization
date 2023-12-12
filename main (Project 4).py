# Project 4 program for ECE 366 Computer Organization
# This program utilizes the files of P4.asm and P4.txt as inputs 
# log.txt displays the overall output of the program

import math
import random

hits = 0
misses = 0
count = 0

# DM
class cache1:  # tag = 23, id = 3, offset = 6
  num_sets = 8
  block_size = 64
  num_ways = 1

# DM
class cache2:  # tag = 25, id = 2, offset = 5
  num_sets = 4
  block_size = 32
  num_ways = 1

# 4-way FA
class cache3:  # tag = 25, id = 2, offset = 5
  num_sets = 1
  block_size = 32
  num_ways = 4

# 4-way SA
class cache4:  # tag = 23, id = 3, offset = 6
  num_sets = 2
  block_size = 64
  num_ways = 4

class block_in_cache:
  tag = 0
  v = 0

class block1:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block2:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block3:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block4:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block5:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block6:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block7:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

class block8:
  tag = -1
  set = -1
  v = -1
  count = 0
  way = -1

def blocklist_debugging(blocklist):
  for block in blocklist:
    print("Tag: %s\nSet: %s\n" % (block.tag, block.set))

def LRU_block_index(blocklist, cache, set):
  if (cache == 1 or cache == 2):
    return set
  elif (cache == 3):
    mindex = 0
    for i in range(len(blocklist) - 1):
      if (blocklist[i + 1].count < blocklist[mindex].count):
        mindex = i + 1
    return mindex
  elif (cache == 4):
    if (set == 0):
      mindex = 0
      for i in range(0,3):
        if (blocklist[i+1].count < blocklist[mindex].count):
          mindex = i+1
    elif(set == 1):
      mindex = 4
      for i in range(4,7):
        if (blocklist[i+1].count < blocklist[mindex].count):
          mindex = i+1
    return mindex

def addr_div(num_sets, block_size):

  num_bits_offset = math.log(block_size, 2)
  num_bits_id = math.log(num_sets, 2)
  num_bits_tag = 32 - num_bits_id - num_bits_offset

  return int(num_bits_tag), int(num_bits_id), int(num_bits_offset)

def cacheprint(cache, f):
  cache = int(cache)
  f.write("Cache Data\n")

  blocklist = []

  if (cache == 1):
    blocklist.append(block1)
    blocklist.append(block2)
    blocklist.append(block3)
    blocklist.append(block4)
    blocklist.append(block5)
    blocklist.append(block6)
    blocklist.append(block7)
    blocklist.append(block8)
    print("DM Cache with 8 sets, block size of 64 Bytes\n")
    f.write("DM Cache with 8 sets, block size of 64 Bytes\n")
  elif (cache == 2):
    blocklist.append(block1)
    blocklist.append(block2)
    blocklist.append(block3)
    blocklist.append(block4)
    print("DM Cache with 4 sets, block size of 32 Bytes\n")
    f.write("DM Cache with 4 sets, block size of 32 Bytes\n------------------------------------------\n")
  elif (cache == 3):
    blocklist.append(block1)
    blocklist.append(block2)
    blocklist.append(block3)
    blocklist.append(block4)
    print("4-way FA Cache with block size of 32 Bytes\n")
    f.write("4-way FA Cache with block size of 32 Bytes\n")
  elif (cache == 4):
    blocklist.append(block1)
    blocklist.append(block2)
    blocklist.append(block3)
    blocklist.append(block4)
    blocklist.append(block5)
    blocklist.append(block6)
    blocklist.append(block7)
    blocklist.append(block8)
    print("4-way SA Cache with 2 sets, block size of 64 Bytes\n")
    f.write("4-way SA Cache with 2 sets, block size of 64 Bytes\n")
  return blocklist

def cacheprint2(cache, code2bin, f, blocklist):
  global hits
  global misses
  cache = int(cache)
  rt = registers[code2bin[6:11]]
  imm = int(code2bin[16:], 2)
  mem_int = rt + imm
  mem_hex = hex(mem_int)[2:].zfill(8)
  mem_bin = bin(mem_int)[2:].zfill(32)
  print(
    "\nCache Data\n------------------------------------------\nMemory in...\nhex: 0x%s\nbinary: %s\n" %
    (mem_hex, mem_bin))
  f.write("Memory Address\nhex: 0x%s\nbinary: %s\n" % (mem_hex, mem_bin))
  if (cache == 1):
    tag = mem_bin[:23]
    set = mem_bin[23:26]
    way = 0
    offset = mem_bin[26:]
    print("Tag: %s\nSet: %s\nOffset: %s\n" %
          (mem_bin[:23], mem_bin[23:26], mem_bin[26:]))
    f.write("Tag: %s\nSet: %s\nOffset: %s\n" %
            (mem_bin[:23], mem_bin[23:26], mem_bin[26:]))
  elif (cache == 2):
    tag = mem_bin[:25]
    set = mem_bin[25:27]
    way = 0
    offset = mem_bin[27:]
    print("Tag: %s\nSet: %s\nOffset: %s\n" %
          (mem_bin[:25], mem_bin[25:27], mem_bin[27:]))
    f.write("Tag: %s\nSet: %s\nOffset: %s\n" %
            (mem_bin[:25], mem_bin[25:27], mem_bin[27:]))
  elif (cache == 3):
    tag = mem_bin[:27]
    set = "0"
    offset = mem_bin[27:]
    print("Tag: %s\nOffset: %s\n" % (mem_bin[:27], mem_bin[27:]))
    f.write("Tag: %s\nOffset: %s\n" % (mem_bin[:27], mem_bin[27:]))
  elif (cache == 4):
    tag = mem_bin[:26]
    set = mem_bin[26]
    offset = mem_bin[27:]
    print("Tag: %s\nTag Int: %s\nSet: %s\nOffset: %s\n" %
          (mem_bin[:26], int(mem_bin[:26], 2), mem_bin[26], mem_bin[27:]))
    f.write("Tag: %s\nSet: %s\nOffset: %s\n" %
            (mem_bin[:26], mem_bin[26], mem_bin[27:]))
  hitbool = False
  for block in blocklist:
    if (int(tag, 2) == block.tag and (int(set, 2) == block.set or cache == 4)):
      hitbool = True
      hits += 1
      block.v = 1
      block.count = hits + misses
      print("HIT!\nReading from offset %s\n\nLRU Bookkeeping: Hit in block %s\nTag: %s\nSet: %s\nUpdating LCU count...\n" %
            (offset, blocklist.index(block), block.tag, block.set))
      f.write("HIT!\nReading from offset %s\n\nLRU Bookkeeping: Hit in block %s\nTag: %s\nSet: %s\nUpdating LCU count...\n" %
            (offset, blocklist.index(block), block.tag, block.set))
      break
  if (not hitbool):
    misses = misses + 1
    index = LRU_block_index(blocklist, cache, int(set, 2))
    blocklist[index].tag = int(tag, 2)
    blocklist[index].set = int(set, 2)
    blocklist[index].count = hits + misses
    blocklist[index].v = 1
    print(blocklist[index].set)
    if (cache == 3):
      way = index
    elif (cache == 4):
      way = index % 2
    blocklist[index].way = way
    print(
      "Miss!:(\nBlock offset: %s\nInto way %s\nTag: %s\nSet: %s\nValid Bit: %s\nLRU Bookkeeping: Replacing Block %s at;\nTag: %s/nSet: %s\nOffset: %s\nWay = %s"
      % (offset, blocklist[index].way, blocklist[index].tag,blocklist[index].set, blocklist[index].v, index, blocklist[index].tag, blocklist[index].set, offset, blocklist[index].way))
    print(
      "With Block;\nTag: %s/nSet: %s\nOffset: %s\nWay = %s"
      % (block.tag, block.set, offset, blocklist[index].way))
  print("Hits/Misses: %s/%s\nHit Percentage: %s%%" %
          (hits, misses, round(hits*100 / (hits + misses), 2)))
  f.write("Hits/Misses: %s/%s\nHit Percentage: %s%%" %
          (hits, misses, round(hits*100 / (hits + misses), 2)))
  f.write("\n---------\n")
  return blocklist

def components(code2bin):
  tag = code2bin[:23]
  id = code2bin[23:26]
  offset = code2bin[26:]

def components2(code2bin):
  tag = code2bin[:25]
  id = code2bin[25:27]
  offset = code2bin[27:]

# A function to classify machine code

def identification(code2bin):
  if (code2bin[:6] == "001000"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: addi ${rt_int}, ${rs_int}, {imm_int}')

  elif (code2bin[:6] == "000100"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: beq ${rt_int}, ${rs_int}, {imm_int}')

  elif (code2bin[:6] == "000101"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: bne ${rt_int}, ${rs_int}, {imm_int}')

  elif (code2bin[:6] == "101011"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: sw ${rt_int}, 0x{hex(imm_int)[2:].zfill(4)}(${rs_int})')

  elif (code2bin[:6] == "100011"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: lw ${rt_int}, 0x{hex(imm_int)[2:].zfill(4)}(${rs_int})')

  elif (code2bin[:6] == "101010"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: blt ${rt_int}, ${rs_int}, {imm_int}')

  elif (code2bin[:6] == "001100"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    imm_int = int(imm, 2)
    if imm_int > 32767:
      imm_int = imm_int - 65536

    print(f'Instruction: andi ${rt_int}, ${rs_int}, {imm_int}')

  elif (code2bin[:6] == "000000" and code2bin[26:] == "101010"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    rd = code2bin[16:21]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    rd_int = int(rd, 2)

    print(f'Instruction: slt ${rd_int}, ${rs_int}, ${rt_int}')

  elif (code2bin[:6] == "000000" and code2bin[26:] == "100111"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    rd = code2bin[16:21]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    rd_int = int(rd, 2)

    print(f'Instruction: nor ${rd_int}, ${rs_int}, ${rt_int}')

  elif (code2bin[:6] == "000000" and code2bin[26:] == "100010"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    rd = code2bin[16:21]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    rd_int = int(rd, 2)

    print(f'Instruction: sub ${rd_int}, ${rs_int}, ${rt_int}')

  elif (code2bin[:6] == "000000" and code2bin[26:] == "100000"):
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    rd = code2bin[16:21]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    rd_int = int(rd, 2)

    print(f'Instruction: add ${rd_int}, ${rs_int}, ${rt_int}')

  elif (code2bin[:6] == "000000" and code2bin[26:] == "000010"):
    rt = code2bin[11:16]
    rd = code2bin[16:21]
    sh = code2bin[21:26]

    rt_int = int(rt, 2)
    sh_int = int(sh, 2)
    rd_int = int(rd, 2)

    if sh_int > 32767:
      sh_int = sh_int - 65536

    print(f'Instruction: srl ${rd_int}, ${rt_int}, {sh_int}')

# A function to compute assembly instructions
def function(PC,
             typeInstr,
             op="000000",
             rs="00000",
             rt="00000",
             rd="00000",
             sh="00000",
             func="000000",
             imm=0):
  if op == "001000":  # addi
    registers[rt] = registers[rs] + imm
    return registers[rt]

  elif func == "101010":  # slt
    if registers[rs] < registers[rt]:
      registers[rd] = 1
    else:
      registers[rd] = 0
    return registers[rd]

  elif op == "000100":  # beq
    if registers[rs] == registers[rt]:
      PC = PC + imm_int
      return PC
    else:
      return PC

  elif op == "000101":  # bne
    if registers[rs] != registers[rt]:
      PC = PC + imm_int
      return PC
    else:
      return PC

  elif op == "101011":  # sw

    dest_memory_bin = bin(registers[rs] + imm_int)[2:].zfill(32)
    num_bits_tags, num_bits_id, num_bits_offset = addr_div(
      myCache.num_sets, myCache.block_size)

    tag = dest_memory_bin[:num_bits_tags]
    id = dest_memory_bin[-num_bits_offset - num_bits_id:-num_bits_offset]
    offset = dest_memory_bin[-num_bits_offset:]

    print("Dest Addr: %s" % dest_memory_bin)
    print("Tag: %s" % tag)
    print("id: %s" % id)
    print("offset: %s" % offset)

    Memlist[hex(registers[rs] + imm_int)[2:].zfill(8)] = registers[rt]

    print(f' Updated Memory: {hex(imm_int + registers[rs])} = {registers[rt]}')

  elif op == "101010":  # blt
    if registers[rt] < registers[rs]:
      PC = PC + imm_int
      return PC
    else:
      return PC

  elif func == "100111":  # nor
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

  elif func == "100010":  # sub
    registers[rd] = registers[rs] - registers[rt]
    return registers[rd]

  elif func == "100000":  # add
    registers[rd] = registers[rs] + registers[rt]
    return registers[rd]

  elif op == "100011":  # lw
    print("Testing, rt: %s, rs: %s, in mem %s" % (registers[rt], registers[rs], Memlist[hex(registers[rs] + imm_int)[2:].zfill(8)]))
    registers[rt] = Memlist[hex(registers[rs] + imm_int)[2:].zfill(8)]

    print(f' Updated Memory: {hex(imm_int + registers[rs])} = {registers[rt]}')

  elif func == "000010":  # srl
    sh = int(sh, base=2)

    if sh > 32767:
      sh = registers[rs] - 65536

    registers[rd] = (registers[rs] % 0x100000000) >> sh

    return registers[rd]

  elif op == "001100":  # andi

    registers[rt] = registers[rs] & imm

    return registers[rt]

# A function to read a .txt file
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
rd = ""
sh = ""
func = ""
imm = 0
pop = 0
b = 0
run = False
stats = ALU = J = B = M = O = 0
RT = IT = JT = 0
tag = ""
id = ""
offset = ""

# Creating a list for PC addresses
for i in range(0x0000, 0x0000 + 50 * 4, 4):
  PClist.append(i)
for i in range(0x2000, 0x2000 + 128 * 4, 4):
  Memlist[hex(i)[2:].zfill(8)] = 0

# Initializing registers 0-31 with 0
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
# declaration of instructions
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

# """***********Project4****************"""
cache = input("Enter Cache Type (1-4): ")

myCache = cache1()

if cache == "1":
  myCache = cache1()
elif cache == "2":
  myCache = cache2()
elif cache == "3":
  myCache = cache3()
elif cache == "4":
  myCache = cache4()

tags, id, offset = addr_div(myCache.num_sets, myCache.block_size)

print("Tag: %d, Id: %d, Offset: %d" % (tags, id, offset))

cacheConfig = [[0 for x in range(myCache.num_ways)]
               for y in range(myCache.num_sets)]

for i in cacheConfig:
  print(i)

name = input("Enter Filename to assemble: ")
filename = input("Enter the file you want to log cache data in: ")
file = open(filename, "w")
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

# identification of labels when present
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
blocklist = cacheprint(cache, file)
# loop to run through list of instructions
while PC <= int(hex(InstrMem[len(InstrMem) - 1][0])[2:], base=16) / 4:
  b += 1

  # while loop for user input
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
  code2bin = code2bin[2:].zfill(32)  # op code
  print(code2bin)
  new = identification(code2bin)

  print(new)

  if (cache == "1"):
    check = components(code2bin)
  elif (cache == "4"):
    check = components(code2bin)
  elif (cache == "2"):
    check = components2(code2bin)
  elif (cache == "3"):
    check = components2(code2bin)

  # beq, bne, blt
  if code2bin[:
              6] == '000100' or code2bin[:
                                         6] == '101010' or code2bin[:
                                                                    6] == '000101':
    brnch = True
  if code2bin[:6] == "100011" or code2bin[0:6] == "101011":  # sw and lw
    store = True

  if code2bin[26:] == "000010":  # srl
    srl = True

  if (code2bin[:6] == '000000'):
    typeInstr = "R"
  else:
    typeInstr = "I"

  if typeInstr == "I":
    print("I-Type\n")

    rd = 0
    sh = 0
    func = 0
    op = code2bin[0:6]
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    imm = code2bin[16:]
    rt_int = int(rt, 2)
    rs_int = int(rs, 2)

    if (imm[0] == '1'):
      tryingstuff = imm.replace('0', '2')
      tryingstuff = tryingstuff.replace('1', '0')
      tryingstuff = tryingstuff.replace('2', '1')
      imm_int = (int(tryingstuff, 2) + 1) * -1
    else:
      imm_int = int(imm, 2)

    if store == True:
      memPart = imm_int
      imm = bin(imm_int)[2:].zfill(16)

    if brnch == True:
      PC = function(PC, typeInstr, op, rs, rt, '000000', '00000', '000000',
                    imm_int)

    else:
      update = function(PC, typeInstr, op, rs, rt, '00000', '00000', '000000',
                        imm_int)

    machineCode = op + rs + rt + imm
    #store = False

    IT += 1
    if op == "101010":
      O += 1
    # condition for beq, bne, and blt
    if op == "000100" or op == "000101" or op == "101010":
      B += 1
    # condition for sw and lw
    elif op == "101011" or op == "100011":
      M += 1
    else:
      ALU += 1

  elif typeInstr == "R":
    print("R-Type\n")

    op = "00000"
    op = code2bin[0:6]
    rs = code2bin[6:11]
    rt = code2bin[11:16]
    rd = code2bin[16:21]
    func = code2bin[26:]

    rt_int = int(rt, 2)
    rs_int = int(rs, 2)
    rd_int = int(rd, 2)

    if srl == False:
      sh = "00000"
    else:
      sh = code2bin[21:26]

    update = function(PC, typeInstr, op, rs, rt, rd, sh, func)
    machineCode = op + rs + rt + rd + sh + func
    srl = False

    RT += 1
    # condtiion for slt
    if func == "101010":
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
  if (store):
    blocklist = cacheprint2(cache, code2bin, file, blocklist)
    store = False
  print("**********************************")
file.close()
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
