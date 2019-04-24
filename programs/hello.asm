    loadi r1 hello
loop:
    loadp r0 r1
    comparei.eq r0 0
    branch.eq quit
    output r0 0x00
    addi r1 r1 1
    jump loop
quit:
    addi r0 r0 '\n'
    output r0 0x00
    halt
hello:
    .str Hello World!
