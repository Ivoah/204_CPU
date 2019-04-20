    load r1 t
    load r2 y
    load r3 n
loop:
    input r0 0x00
    compare.eq r0 r1
    branch.eq yes
    output r3 0x00
    jump loop
yes:
    output r2 0x00
    jump loop
y:
    .str y
n:
    .str n
t:
    .str t
