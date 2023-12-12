#Author: Bryan Ly
#ECE 366 Rao
#Homework 6: MIPS ASM Simulator
#05 October 2022

selection = val = PC = currPC = 0
instr_id = {}
label_id = {}
reg_id = []
target_PC = []
loop_id = []
machine_c = {}
PC_Count = 0

print("Displaying MIPS Assembly Codes from files to list...")
input("\n...press any key to continue...\n")

f = open('trail.asm')
mips = f.readlines()
print(mips)
f.close()

input("\n...press any key to continue...\n")

print("Removing 'next line' from list...")
for i in range(len(mips)): #removes next line function in list
  mips[i] = mips[i].replace("\n", "")
print(mips)

input("\n...press any key to continue...\n")

for i in range(0,32): #creates an array of registers
  reg_id.append(0)

print('Identifying PC with Corresponding Instruction:\n')
for i, ln in enumerate(mips): #differentiates between labels and instructions and outputs identification
    pos = ln.find(":")
    print(f'PC = {PC:2} = {hex(PC):10} line [{i}] is {ln:20}')

    if pos >= 0:    
        label_id[ln[:pos]] = PC
        input(f'Label identified -> addr {PC}. Press any key to continue... \n')
    else:  
        instr_id[PC]=ln
        PC += 4
        input(f'Instruction Identified. Press any key to continue... \n')

print('\nBelow are the PC with MIPS instructions:\n')
for PC, instr in instr_id.items(): #outputs the PC with corresponding instruction from file
    print(f' 0x{hex(PC)[2:].zfill(2):<2}: {instr}')

input("\n...press any key to continue...\n")

print('\nBelow are all the labels:\n')
if(len(label_id) != 0): #outputs the labels and PC in file
  for label, PC in label_id.items():
      print(f'{label:<5} =  {PC:<5} -> {instr_id[PC]:<5}')
else:
  print('No labels present in this file.\n')    

input("\n...press any key to continue...\n")

print('\nBreaking each instruction into components:')
print('Press any key to continue breakdown\n')

while currPC <= PC:

    i_new = instr_id[currPC].replace(",", "") #separates the individual instructions in list
    i_list = i_new.split(" ")      
  
    if(i_list[0] == 'addi'): #identifies the I-Type addi function in list
      op = '001000'
      rs = bin(int(i_list[2][1:]))[2:].zfill(5)
      rt = bin(int(i_list[1][1:]))[2:].zfill(5)
      imm = int(i_list[3])
      if imm < 0:
        imm = bin(2**16 + imm)[2:].zfill(16)
      else:
        imm = bin(imm)[2:].zfill(16)

      x = op + rs + rt + imm #combines binary
      val = int(reg_id[int(i_list[2][1:])]) + int(i_list[3]) 
      reg_id[int(i_list[1][1:])] = val

      print(f'{instr_id[currPC]:<17} -> {i_new:<15} -> {i_list}\n')
      print(i_list[1],"=" ,val)
      input()
       
    elif(i_list[0] == 'slt'): #identifies the R-Type shift left function in list
      op = '000000'
      rs = bin(int(i_list[2][1:]))[2:].zfill(5)
      rt = bin(int(i_list[3][1:]))[2:].zfill(5)
      rd = bin(int(i_list[1][1:]))[2:].zfill(5)
      sh = '00000'
      func = '101010'

      x = op + rs + rt + rd + sh + func

      if int(reg_id[int(rs,2)])< int(reg_id[int(rt,2)]): #compares the values of two registers 
        reg_id[int(i_list[1][1:])] = '1'
      else:
        reg_id[int(i_list[1][1:])] = '0'

      print(f'{instr_id[currPC]:<17} -> {i_new:<15} -> {i_list}\n')
      print(i_list[1],"=" ,reg_id[int(i_list[1][1:])])
      input()
      
    elif(i_list[0] == 'beq'): #identifies the I-Type branch if equal function in list
      op = '000100'
      rs = '00000'
      rt = bin(int(i_list[1][1:]))[2:].zfill(5)
      imm = ((label_id[i_list[3]] - PC) - 4)/4
      if imm < 0: 
        imm = bin(2**16 + int(imm))[2:].zfill(16)
      else:
        imm = bin(int(imm))[2:].zfill(16)
        
      x = op + rs + rt + imm

      target_PC = label_id[i_list[-1]]   #identifies the PC to branch to
      print(f'Target PC = {target_PC} = 0x{hex(target_PC)[2:].zfill(2):<2} for label: {i_list[-1]}\n')

      PC_Count = loop_id.count(i_list[-1])

      if PC_Count < 1:
        loop_id.append(i_list[3])
      if(int(reg_id[int(i_list[1][1:])]) ==  int(rs,2)):
        currPC = label_id[i_list[3]] - 4

      input()
        
    machine_c[currPC] = '0x' + (hex(int(x,2))[2:].zfill(8))
    currPC += 4

input("\n...press any key to continue...\n")

print('\nBelow are the hex PC with Machine Code:\n') #output of machine code with corresponding PC in hex
for PC in machine_c:
  print(f'  0x{hex(PC)[2:].zfill(2):<2}: {machine_c[PC]}')
  
input("\n...press any key to continue...\n")

print('\nFinal values of registers $5-$15:\n')
for i in range(5,16): #output of registers $5-$15 with associated final values

  print(f'${i:<2}  = {reg_id[i]:>4}')
  
input("\n...press any key to continue...\n")

print('\nBelow are the labels with their designated instructions:\n') #output of labels with associated PC's and instruction
if(len(label_id) != 0):
  for label, PC in label_id.items():
      print(f'{label:<5} -> 0x{hex(PC)[2:].zfill(2):<2} = {machine_c[PC]:<3}')
else:
  print('No labels present in this file.\n')

input("\n...press any key to continue...\n")

print('...End of Program...')