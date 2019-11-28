import sys
import re
import openpyxl

# arg 0 is name
# arg 1 is path to trace file
# arg 2 is path to excel file

file = open(sys.argv[1], 'r')

lines = file.readlines()[3:-2]

commands = []
i = 0

while i in range(len(lines)):
    commands.append(''.join(lines[i:i + 4]))
    i += 4

reg_values = []
flag_values = []
curr_adr_com = []

registers = [
    'AX', 'SI', 'CS', 'Stack +0',
    'BX', 'DI', 'DS', 'Stack +2',
    'CX', 'BP', 'ES', 'Stack +4',
    'DX', 'SP', 'SS', 'Stack +6'
]
registers = dict().fromkeys(registers)
for i, reg in enumerate(registers.keys()):
    registers[reg] = i

flags = [
    'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF'
]

for i, command in enumerate(commands):
    curr_adr_com.append(re.findall('\w+', command[:13]))
    reg_values.append(re.findall('[0-9A-F]{4}', command[42:]))
    flag_values.append(re.findall('[0-1]', command[-63:-40]))

# for i in range(len(reg_values)):
#     for k, reg in enumerate(reg_values[i]):
#         print(registers[k], '=', reg)
#     for k, flag in enumerate(flag_values[i]):
#         print(flags[k], '=', flag)

excel_file = openpyxl.load_workbook(filename = 'pp.xlsx')
sheet = excel_file['test']

for i in range(len(reg_values)):
    for i in range(1, len(curr_adr_com)):
        sheet.cell(row=i, column=1).value = curr_adr_com[i][0]
        sheet.cell(row=i, column=2).value = curr_adr_com[i][1]
        sheet.cell(row=i, column=3).value = reg_values[i][registers['AX']]
        sheet.cell(row=i, column=4).value = reg_values[i][registers['BX']]
        sheet.cell(row=i, column=5).value = reg_values[i][registers['CX']]
        sheet.cell(row=i, column=6).value = reg_values[i][registers['DX']]
        for k, flag in enumerate(flag_values[i]):
            sheet.cell(row=i, column=7+k).value = flag
excel_file.save('pp.xlsx')
file.close()