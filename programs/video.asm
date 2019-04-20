loop:
    output r0 0x1
    output r1 0x1
    output r1 0x1
    addi r0 r0 1
    compare.eq r0 r3
    branch.eq next_line
    jump loop
next_line:
    addi r1 r1 1
    compare.eq r1 r3
    branch.eq end
    jump loop
end:
    input r0 0x0
    halt
