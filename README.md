# 204_CPU
Emulator and assembler for CPU designed in ELEE 204

Instruction set can be found in `specs.txt`.

By default the emulator has two devices connected.
Device `0x00` is a simple I/O device connected to stdin/stdout.
Reading a byte from it will block until the user presses a key and writing a byte will print it to stdout.
Device `0x01` is a screen implemented in pygame. Reading from this device returns the currently held key, or 0 if no key is held.
Displaying a pixel requires 3 separate writes.
The first write is the x coordinate, the second write is the y coordinate, and the third write is the pixel color.
Colors are in RGB332 format, with the first three bits assigned to red, the second three green, and the last two blue.

Look at [devices.py](devices.py) to add more devices.

## Requirements
You will need Python 3.6+ and pygame in order to run the emulator and assembler.

The latest version of python can be obtained from [the python website](https://www.python.org/downloads/)

Once python is installed pygame can be installed with pip: `pip install pygame`

## Assembling
`python3 assembler.py <input.asm> <output.204>`

## Running
`python3 cpu.py <program.204>`
