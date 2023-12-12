# ECE 366 Computer Organization Homework 4 Program
# Conversion of binary values to integers and distinguishing values and memory addresses

n = r = y = c = d =p = p1 = f = 0
mem = 0x2000 #memory address for alternating values
par = 0x2100 #memory address for parity 
col = 0x2200 #memory address for Column sums

val = input("Please enter a value (i.e. '1' or '-23') for x:\n")

#identifies memory address and parity of input
x = int(val)
tbin = bin(x)
tbin = tbin.zfill(32)
init = 0
k=''
for z in range(len(tbin)): #loops through length of binary
  if (tbin[z] == '0'):
    k = k + '1'
  else: 
    k = k + '0'

y_int = int(k, base = 2) #converts from binary to integer
z_int = y_int + 1 #increments y by 1
zval = bin(z_int)

for r in range(len(zval)):
  if zval[r] == '1':
    f = f + 1
    
if f%2 == 0:
  init = 0
else:
  init = 1

print(f'A[{mem}] = {x}      P[{par}] = {init}') #outputs initial value

if x < 0:
  sum = sum1 = sum2 = sum3 = sum4 = 0
  x = x*(-1)
  while n != 34: #loops for 34 values other than input
    n = n+1
    x = x-1
    
    if n%2 == 0: #find the negative values
      y = x*(-1)
      d = 0
      
      ybin = bin(y)
      ybin = ybin.zfill(32)

      k = ''
      for z in range(len(ybin)):
        if (ybin[z] == '0'):
          k = k + '1'
        else: 
          k = k + '0'

      y_int = int(k, base = 2) #converts from binary to integer
      z_int = y_int + 1 #increments y by 1
      zval = bin(z_int)
      zval = zval.zfill(32)

      for l in range(len(zval)):
        if zval[l] == '1':
          d = d+1

    address = mem + (n*4) #identifies memory address
    address2 = par + (n*4)
    xbin = bin(x)
    xbin = xbin.zfill(32)

    if n%2 != 0:
      c = 0
      for j in range(len(xbin)):     
        if xbin[j] == '1':
          c = c+1
        
    if c%2 == 0:
      p = 0
    else:
      p = 1
      
    if d%2 == 0:
      p1 = 0
    else:
      p1 = 1

    if n%2 == 0:
      print(f'A[{address}] = {y}      P[{address2}] = {p1}')
    else:
      print(f'A[{address}] = {x}     P[{address2}] = {p}')

    if n == 5 or n == 15  or n == 25:
      sum = sum + p
    elif n ==  10 or n == 20 or n == 30:
      sum = sum + p1

    if n == 1 or n == 11 or n == 21 or n == 31:
      sum1 = sum1 + p
    elif n == 6 or n ==16 or n == 26:
      sum1 = sum1 + p1

    if n == 7 or n == 17 or n == 27:
      sum2 = sum2 + p
    elif n == 2 or n ==12 or n == 22 or n == 32:
      sum2 = sum2 + p1

    if n == 3 or n == 13 or n == 23 or n == 33:
      sum3 = sum3 + p
    elif n == 8 or n ==18 or n == 28:
      sum3 = sum3 + p1

    if n == 9 or n == 19 or n == 29:
      sum4 = sum4 + p
    elif n == 4 or n ==14 or n == 24 or n == 34:
      sum4 = sum4 + p1

elif x >= 0:
  sum = sum1 = sum2 = sum3 = sum4 = 0
  while n != 34: #loops for 34 values other than input
    n = n+1
    x = x+1
    
    if n%2 != 0: #determines negative values
      y = x*(-1)
      d = 0
      
      ybin = bin(y)
      ybin = ybin.zfill(32)

      k = ''
      for z in range(len(ybin)):
        if (ybin[z] == '0'):
          k = k + '1'
        else: 
          k = k + '0'

      y_int = int(k, base = 2) #converts from binary to integer
      z_int = y_int + 1 #increments y by 1
      zval = bin(z_int)
      zval = zval.zfill(32)

      for l in range(len(zval)):
        if zval[l] == '1':
          d = d+1
      
    address = mem + (n*4) #identifies memory address for data
    address2 = par + (n*4)
    xbin = bin(x)
    xbin = xbin.zfill(32)

    if n%2 == 0:
      c = 0
      for j in range(len(xbin)):     
        if xbin[j] == '1':
          c = c+1
    
    if c%2 == 0:
      p = 0
    else:
      p = 1
      
    if d%2 == 0:
      p1 = 0
    else:
      p1 = 1
    
    if n%2 != 0:
      print(f'A[{address}] = {y}     P[{address2}] = {p1}')
    else:
      print(f'A[{address}] = {x}      P[{address2}] = {p}')

    if n == 5 or n == 15  or n == 25:
      sum = sum + p1
    elif n ==  10 or n == 20 or n == 30:
      sum = sum + p

    if n == 1 or n == 11 or n == 21 or n == 31:
      sum1 = sum1 + p1
    elif n == 6 or n ==16 or n == 26:
      sum1 = sum1 + p

    if n == 7 or n == 17 or n == 27:
      sum2 = sum2 + p1
    elif n == 2 or n ==12 or n == 22 or n == 32:
      sum2 = sum2 + p

    if n == 3 or n == 13 or n == 23 or n == 33:
      sum3 = sum3 + p1
    elif n == 8 or n ==18 or n == 28:
      sum3 = sum3 + p

    if n == 9 or n == 19 or n == 29:
      sum4 = sum4 + p1
    elif n == 4 or n ==14 or n == 24 or n == 34:
      sum4 = sum4 + p
    



print('\n')
print("Sums of 7x5 Columns:",'\n')
print(f'S[{col}] = {sum + init}', f'S[{col + 4}] = {sum1}', f'S[{col + 8}] = {sum2}', f'S[{col + 12}] = {sum3}', f'S[{col + 16}] = {sum4}') 
