#PART A
addi $7, $0, 1

addi $5, $0, 0
addi $8, $0, 0
addi $31, $0, 35

loop:
sw $7, 0x2000($8)
addi $5, $5, 1
addi $8, $8, 4
blt $7, $0, negative
nor $7, $7, $7
blt $5, $31, loop

negative:
nor $7, $7, $7
addi $7, $7, 2
blt $5, $31, loop
