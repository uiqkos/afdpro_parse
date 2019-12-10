#!/usr/bin/python
import sys
import re
import csv
import openpyxl

variables = [
    'AX', 'SI', 'CS', 'Stack +0',
    'BX', 'DI', 'DS', 'Stack +2',
    'CX', 'BP', 'ES', 'Stack +4',
    'DX', 'SP', 'SS', 'Stack +6',
    'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF',
    'current', 'command'
]
equals = {
    'tfp' : 'trace_file_path',
    'cfp' : 'csv_file_path',
    'sn'  : 'sheet_name',
    'tl'  : 'tab_left',
}

class Iteration:
    def __init__(self, reg_values, flags_values, curr_addr, command):
        values = reg_values+flags_values+curr_addr+command
        self.values = dict.fromkeys(variables)
        for index, key in enumerate(self.values.keys()):
            self.values[key] = values[index]

    def get(self, key):
        return self.values[key]

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
    csv_file_path='trace.csv',
    sheet_name='trace',
    tab_top=0,
    mask=['current', 'command', 'AX', 'BX', 'CX', 'DX', 'OF', 'DF', 'IF', 'SF', 'ZF', 'AF', 'PF', 'CF', 'Stack +0']
):

    with open(trace_file_path, 'r') as file:
        lines = file.readlines()[3:-2]
    commands = [''.join(lines[i:i + 4]) for i in range(0, len(lines), 4)]

    iterations = []

    for i, command in enumerate(commands):
        temp = re.findall('\w+', command[:12])
        iterations.append( Iteration(
            reg_values   = re.findall('[0-9A-F]{4}', command[42:]), # hex number ignore first 42 chars
            flags_values = re.findall('[0-1]', command[-63:-40]), # 0 or 1
            curr_addr    = temp[:1],
            command      = temp[1:]
        ))

    csv_file = open(csv_file_path, 'w')
    writer = csv.DictWriter(csv_file, fieldnames=mask, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for iteration in iterations:
        writer.writerow({key: iteration.get(key) for key in mask})

    csv_file.close()

if __name__ == '__main__':
    parse_afdpro(**parse_args(sys.argv[1:]))