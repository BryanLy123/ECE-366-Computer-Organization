addi $7, $0, 1

addi $31, $0, 35
addi $5, $0, 0
addi $8, $0, 0
addi $11, $0, 1

loop:
sw $7, 0x2000($8)
addi $5, $5, 1
addi $8, $8, 4
slt $1, $7, $0
bne $1, $0, negative
nor $7, $7, $7
slt $1, $5, $31
bne $1, $0, loop

negative:
nor $7, $7, $7
addi $7, $7, 2
slt $1, $5, $31
bne $1, $0, loop
sub $8, $8, $8
addi $10, $0, 0

loop1:
lw $7, 0x2000($8)

loop2:
andi $10, $7, 1
add $9, $9, $10
srl $7, $7, 1
bne $7, $0, loop2
andi $9, $9, 1
sw $9, 0x2100($8)
sub $9, $9, $9
addi $8, $8, 4
addi $4, $4, 1
bne $4, $31, loop1
