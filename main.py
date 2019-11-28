import sys
import re

# arg 0 is name
# arg 1 is path to trace file
#
file = open(sys.argv[1], 'r')
lines = file.readlines()[3:-2]

commands = []
i = 0

while i in range(len(lines)):
    commands.append(''.join(lines[i:i + 4]))
    i +=4

reg_values = []
flag_values = []
current_address_and_command = []

registers = [
    'AX', 'SI', 'CS', 'Stack +0',
    'BX', 'DI', 'DS', 'Stack +2',
    'CX', 'BP', 'ES', 'Stack +4',
    'DX', 'SP', 'SS', 'Stack +6'
]
flags = [
    'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF'
]

for i, command in enumerate(commands):
    current_address_and_command.append(re.findall('\w+', command[:13]))
    reg_values.append(re.findall('[0-9A-F]{4}', command[42:]))
    flag_values.append(re.findall('[0-1]', command[-63:-40]))

for i in range(len(reg_values)):
    for k, reg in enumerate(reg_values[i]):
        print(registers[k], '=', reg)
    for k, flag in enumerate(flag_values[i]):
        print(flags[k], '=', flag)