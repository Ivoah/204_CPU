    addi r0 r0 127
    addi r1 r1 127
loop:
    input r2 0x00
    load r3 w
    compare.eq r2 r3
    branch.eq up
    load r3 s
    compare.eq r2 r3
    branch.eq down
    load r3 a
    compare.eq r2 r3
    branch.eq left
    load r3 d
    compare.eq r2 r3
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
w:
    .bytes 'w'
s:
    .bytes 's'
a:
    .bytes 'a'
d:
    .bytes 'd'
