    loadi r0 127
    loadi r1 127
loop:
    loadi r3 0
busy_loop:
    addi r3 r3 1
    comparei.eq r3 0
    branch.eq break
    jump busy_loop
break:
    input r2 0x01
    comparei.eq r2 'w'
    branch.eq w_pressed
    comparei.eq r2 's'
    branch.eq s_pressed
    comparei.eq r2 'a'
    branch.eq a_pressed
    comparei.eq r2 'd'
    branch.eq d_pressed
    jump move

w_pressed:
    loadi r2 0x00
    store r2 dir
    jump move
s_pressed:
    loadi r2 0x01
    store r2 dir
    jump move
a_pressed:
    loadi r2 0x02
    store r2 dir
    jump move
d_pressed:
    loadi r2 0x03
    store r2 dir

move:
    load r2 dir
    comparei.eq r2 0x00
    branch.eq up
    comparei.eq r2 0x01
    branch.eq down
    comparei.eq r2 0x02
    branch.eq left
    comparei.eq r2 0x03
    branch.eq right

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

dir:
    .bytes 0x00
color:
    .bytes 0b00011100
