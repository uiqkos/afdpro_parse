#!/usr/bin/python
import sys
import re
import openpyxl


registers = [
        'AX', 'SI', 'CS', 'Stack +0',
        'BX', 'DI', 'DS', 'Stack +2',
        'CX', 'BP', 'ES', 'Stack +4',
        'DX', 'SP', 'SS', 'Stack +6'
]
flags = [
        'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF'
]
equals = {
    'tfp' : 'trace_file_path',
    'efp' : 'excel_file_path',
    'sn'  : 'sheet_name',
    'tt'  : 'tab_top',
    'tl'  : 'tab_left',
}

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

def parse_args(args):
    result = dict()
    for arg in args:
        key, value = arg.split('=')
        if key in equals.keys():
            key = equals[key]
        result[key] = value
    return result

def parse_afdpro(
    trace_file_path='trace.txt', 
    excel_file_path='trace.xlsx', 
    sheet_name='trace', 
    tab_top=0, 
    tab_left=0, 
    mask=['curr_addr', 'command', 'AX', 'BX', 'CX', 'DX', 'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF', 'Stack +0']
):

    file = open(trace_file_path, 'r')
    lines = file.readlines()[3:-2]
    commands = [''.join(lines[i:i + 4]) for i in range(0, len(lines), 4)]

    iterations = []

    for i, command in enumerate(commands):
        temp = re.findall('\w+', command[:12])
        iterations.append( Iteration(
            reg_values   = re.findall('[0-9A-F]{4}', command[42:]), # hex number ignore first 42 chars
            flags_values = re.findall('[0-1]', command[-63:-40]), # 0 or 1
            curr_addr    = temp[0],
            command      = temp[1]
        ))
    
    try:
        excel_file = openpyxl.load_workbook(filename = excel_file_path)
    except:
        excel_file = openpyxl.Workbook()

    if sheet_name not in excel_file.sheetnames:
        excel_file.create_sheet(sheet_name)
    sheet = excel_file[sheet_name]

    tab_left, tab_top = int(tab_left), int(tab_top)

    for i in range(len(iterations)):
        for k, arg in enumerate(mask):
            sheet.cell(row=tab_top+i+1, column=k+tab_left+1).value = iterations[i].__getattr__(mask[k])

    excel_file.save(excel_file_path)
    file.close()

if __name__ == '__main__':
    parse_afdpro(**parse_args(sys.argv[1:]))
    # parse_afdpro(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), mask=['curr_addr', 'command', 'SI', 'AX', 'BX', 'CX', 'DX', 'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF', 'Stack +0'])