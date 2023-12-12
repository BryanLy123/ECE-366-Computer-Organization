#Author: Bryan Ly
#UIN: 661646792
#ECE 366 Rao
#28 August 2022

#Overview: Homework 1

#Initial boolean condition
finished = False

#Loop until initial condition is met
while(not(finished)):
  #Predefined variables
  bit = 8
  val = val1 = val2 = 0

  #Prompt user for input
  usr = input("Please enter Hex Machine Code:\n")

  #Check when to quit program
  if usr == 'q':
    print("Code Ended.\n")
    finished = True

  #Check for Hex input
  elif usr[0:2] == '0x':
    
    #Hex to Binary conversion
    print("\n", "Hex String:", usr)
    Int = int(usr,0)
    Tbinary = bin(Int)
    Tbinary = Tbinary[2:]
    Binary = Tbinary.zfill(bit)
    print(" 8-bit Binary Translation:",Binary,"\n")

    #Check for init function
    if Binary[0:2] == '00': 
      print ("00 = Init")

      #Identify register 
      reg = list(Binary[2:4])
      rx = len(reg)
      for i in range(rx):
        last_element = reg.pop()
        if last_element == '1':
          val += pow(2,i)
      print(Binary[2:4], "=",f'r{val}')

      #Identify value being stored
      imm = list(Binary[4:])
      dec = len(imm)
      for j in range(dec):
        last_element = imm.pop()
        if last_element == '1':
          val1 += pow(2,j)
      print(Binary[4:], "=", val1,"\n")

      #Assembly output
      print(f'Assembly Code: init r{val}, {val1}\n')

    #Check for inc function
    elif Binary[0:2] == '01':
      print ("01 = Inc")

      #Identify register 
      reg = list(Binary[2:4])
      rx = len(reg)
      for i in range(rx):
        last_element = reg.pop()
        if last_element == '1':
          val += pow(2,i)
      print(Binary[2:4], "=",f'r{val}')

      #Identify incrementation value
      imm = list(Binary[4:])
      dec = len(imm)
      for j in range(dec):
        last_element = imm.pop()
        if last_element == '1':
          val1 += pow(2,j)
      print(Binary[4:], "=", val1,"\n")

      #Assembly output
      print(f'Assembly Code: inc r{val}, {val1}\n')

    #Check for add function
    elif Binary[0:2] == '10':
      print ("10 = Add")

      #Identifies Register X
      reg = list(Binary[2:4])
      rx = len(reg)
      for i in range(rx):
        last_element = reg.pop()
        if last_element == '1':
          val += pow(2,i)
      print(Binary[2:4], "=",f'r{val}')

      #Identifies Register Y
      reg1 = list(Binary[4:6])
      ry = len(reg1)
      for j in range(ry):
        last_element = reg1.pop()
        if last_element == '1':
          val1 += pow(2,j)
      print(Binary[4:6], "=",f'r{val1}')

      #Identifies Register Z
      reg2 = list(Binary[6:])
      rz = len(reg2)
      for z in range(rz):
        last_element = reg2.pop()
        if last_element == '1':
          val2 += pow(2,z)
      print(Binary[6:], "=",f'r{val2}\n')

      #Assembly output
      print(f'Assembly Code: add r{val}, r{val1}, r{val2}\n')
      
    #Check for other values
    else:
      print("Function Not Available\n")

  #Check for valid input
  else: 
    print("Invalid Input.\n")

   

  
  
