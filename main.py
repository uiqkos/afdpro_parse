import sys
import re
import openpyxl

# arg 0 is name
# arg 1 is path to trace file
# arg 2 path to excel file
# arg 3 tab from left
# arg 4 tab from top

def parse_afdpro(trace_file_path, excel_file_path, tab_top, tab_left, mask=['curr_addr']):
    registers = [
        'AX', 'SI', 'CS', 'Stack +0',
        'BX', 'DI', 'DS', 'Stack +2',
        'CX', 'BP', 'ES', 'Stack +4',
        'DX', 'SP', 'SS', 'Stack +6'
    ]
    flags = [
        'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF'
    ]

    class Iteration:
        def __init__(self, reg_values, flags_values, curr_addr, command):
            self.regs = dict()
            self.flags = dict()
            self.curr_addr = curr_addr
            self.command = command
            for i, reg in enumerate(registers):
                self.regs[reg] = reg_values[i]
            for i, flag in enumerate(flags):
                self.flags[flag] = flags_values[i]

        def __getattr__(self, item):
            if item in registers:
                return self.regs[item]
            if item in flags:
                return self.flags[item]
            return self.__dict__[item]

    file = open(trace_file_path, 'r')
    lines = file.readlines()[3:-2]
    commands = [''.join(lines[i:i + 4]) for i in range(0, len(lines), 4)]

    iterations = []

    for i, command in enumerate(commands):
        temp = re.findall('\w+', command[:12])
        iterations.append(Iteration(
            re.findall('[0-9A-F]{4}', command[42:]),
            re.findall('[0-1]', command[-63:-40]),
            temp[0],
            temp[1]
        ))

    excel_file = openpyxl.load_workbook(filename = excel_file_path)
    excel_file.create_sheet('trace')
    sheet = excel_file['trace']

    for i in range(len(iterations)):
        for k, arg in enumerate(mask):
            sheet.cell(row=tab_top+i+1, column=k+tab_left+1).value = iterations[i].__getattr__(mask[k])

    excel_file.save(excel_file_path)
    file.close()

if __name__ == '__main__':
    parse_afdpro(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), mask=['curr_addr', 'command', 'SI', 'AX', 'BX', 'CX', 'DX', 'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF', 'Stack +0'])