    addi r0 r0 127
    addi r1 r1 127
loop:
    input r2 0x00
    comparei.eq r2 'w'
    branch.eq up
    comparei.eq r2 's'
    branch.eq down
    comparei.eq r2 'a'
    branch.eq left
    comparei.eq r2 'd'
    branch.eq right
    jump print
up:
    addi r1 r1 255
    jump print
down:
    addi r1 r1 1
    jump print
left:
    addi r0 r0 255
    jump print
right:
    addi r0 r0 1
print:
    output r0 0x01
    output r1 0x01
    load r2 color
    output r2 0x01
    jump loop
color:
    .bytes 0b00011100
