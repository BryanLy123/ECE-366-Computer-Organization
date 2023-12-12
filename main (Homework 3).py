#Author: Bryan Ly
#UIN: 661646792
#ECE 366 Rao
#13 September 2022

#Overview: Homework 3

#Initial boolean condition
finished = False

#Loop until initial condition is met
while(not(finished)):
  #Predefined variables
  bit = 32
  val = val1 = val2 = 0
  y_int = z_int = zval = 0

  #Prompt user for input
  usr = input("Please enter Hex Machine Code:\n")

  #Check when to quit program
  if usr == 'q':
    print("Code Ended.\n")
    finished = True

  #Check for Hex input
  elif usr[0:2] == '0x':
    
    #Hex to Binary conversion
    print("\n","Hex String:", usr)
    Int = int(usr,0)
    Tbinary = bin(Int)
    Tbinary = Tbinary[2:]
    Binary = Tbinary.zfill(bit)
    print(" 32-bit Binary Translation:",Binary,"\n")

    #Check for R-Type Instruction
    if Binary[0:6] == '000000': 
      print ("R- Type Instruction = 000000")

      if Binary[26:] == '100000':

        #Identifies Register S
        reg = list(Binary[6:11])
        rx = len(reg)
        for i in range(rx):
          last_element = reg.pop()
          if last_element == '1':
            val += pow(2,i)
        print("rs =",f'r{val}',"=",Binary[6:11])
  
        #Identifies Register T
        reg1 = list(Binary[11:16])
        ry = len(reg1)
        for j in range(ry):
          last_element = reg1.pop()
          if last_element == '1':
            val1 += pow(2,j)
        print("rt =",f'r{val1}',"=",Binary[11:16])
  
        #Identifies Register D
        reg2 = list(Binary[16:21])
        rz = len(reg2)
        for z in range(rz):
          last_element = reg2.pop()
          if last_element == '1':
            val2 += pow(2,z)
        print("rd =", f'r{val2}',"=",Binary[16:21])

        print("Function = Add = 100000", '\n')
  
        #Assembly output
        print(f'Assembly Code: Add ${val2}, ${val}, ${val1}\n')

      elif Binary[26:] == '100010':

        #Identifies Register S
        reg = list(Binary[6:11])
        rx = len(reg)
        for i in range(rx):
          last_element = reg.pop()
          if last_element == '1':
            val += pow(2,i)
        print("rs =",f'r{val}',"=",Binary[6:11])
  
        #Identifies Register T
        reg1 = list(Binary[11:16])
        ry = len(reg1)
        for j in range(ry):
          last_element = reg1.pop()
          if last_element == '1':
            val1 += pow(2,j)
        print("rt =",f'r{val1}',"=",Binary[11:16])
  
        #Identifies Register D
        reg2 = list(Binary[16:21])
        rz = len(reg2)
        for z in range(rz):
          last_element = reg2.pop()
          if last_element == '1':
            val2 += pow(2,z)
        print("rd =", f'r{val2}',"=",Binary[16:21])

        print("Function = Sub = 100010", '\n')
  
        #Assembly output
        print(f'Assembly Code: Sub ${val2}, ${val}, ${val1}\n')
      
      elif Binary[26:] =='101010':

        #Identifies Register S
        reg = list(Binary[6:11])
        rx = len(reg)
        for i in range(rx):
          last_element = reg.pop()
          if last_element == '1':
            val += pow(2,i)
        print("rs =",f'r{val}',"=",Binary[6:11])
  
        #Identifies Register T
        reg1 = list(Binary[11:16])
        ry = len(reg1)
        for j in range(ry):
          last_element = reg1.pop()
          if last_element == '1':
            val1 += pow(2,j)
        print("rt =",f'r{val1}',"=",Binary[11:16])
  
        #Identifies Register D
        reg2 = list(Binary[16:21])
        rz = len(reg2)
        for z in range(rz):
          last_element = reg2.pop()
          if last_element == '1':
            val2 += pow(2,z)
        print("rd =", f'r{val2}',"=",Binary[16:21])

        print("Function = Slt = 101010","\n");
  
        #Assembly output
        print(f'Assembly Code: Slt ${val2}, ${val}, ${val1}\n')

    #Check for inc function
    elif Binary[0:6] == '001000':
      print ("I- Type Instruction",'\n')
      
      print("Function = Addi = 001000")
      
      #Identify Register S
      reg = list(Binary[6:11])
      rx = len(reg)
      for i in range(rx):
        last_element = reg.pop()
        if last_element == '1':
          val += pow(2,i)
      print("rs =",f'r{val}',"=",Binary[6:11])

      #Identify Register T
      reg1 = list(Binary[11:16])
      ry = len(reg1)
      for j in range(ry):
        last_element = reg1.pop()
        if last_element == '1':
          val1 += pow(2,j)
      print("rt =",f'r{val1}', "=", Binary[11:16])

      #Identifies when the immediate value is negative
      if (Binary[16] == '1'):
        y = ''
        #Flips values of 1's and 0's
        for i in range(16,32,1):
          if (Binary[i] == '0'):
            y = y + '1'
          else: 
            y = y + '0'

        y_int = int(y, base = 2) #converts from binary to integer
        z_int = y_int + 1 #increments y by 1
        zval = bin(z_int) #converts from integer to binary
        zval = zval[2:]
      
        imm = list(zval)
        dec = len(imm)
        for k in range(dec):
          last_element = imm.pop()
          if last_element == '1':
            val2 += pow(2,k)
        print("imm =",Binary[16:], "=",f'-{val2}',"\n")
        #Assembly output
        print(f'Assembly Code: Addi ${val1}, ${val}, -{val2} \n')
      elif (Binary[16] == '0'):
        #Identify Immediate Positive Value
        imm = list(Binary[16:])
        dec = len(imm)
        for z in range(dec):
          last_element = imm.pop()
          if last_element == '1':
            val2 += pow(2,z)
        print("imm =",val2,"=",Binary[16:],"\n")

        #Assembly output
        print(f'Assembly Code: Addi ${val1}, ${val}, {val2}\n')
      
    #Check for other values
    else:
      print("Function Not Available\n")

  #Check for valid input
  else: 
    print("Invalid Input.\n")

   

  
  
