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
