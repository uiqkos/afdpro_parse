import sys, subprocess, csv

objdump = subprocess.run(['objdump', sys.argv[1],
                    '-D',
                    '-m', 'i8086',
                    '-b', 'binary',
                    '-M', 'intel',
                    '--adjust-vma=0x100'], stdout=subprocess.PIPE)

lines = objdump.stdout.decode('ascii').split('\n')


fieldnames = [
    'Адрес',
    'Код команды',
    'Мнемоника'
]

csv_table = open(sys.argv[1].split('.')[0] + '_disasm.csv', 'w')
writer = csv.DictWriter(csv_table, fieldnames = fieldnames, quoting=csv.QUOTE_ALL)
writer.writeheader()

for i in range(7, len(lines)-1):
    writer.writerow({
        'Адрес': lines[i].split('\t')[0].strip(':').replace(' ', '0').upper(),
        'Код команды': lines[i].split('\t')[1].replace(' ', '').upper(),
        'Мнемоника': lines[i].split('\t')[2].replace(' '*4, ' ').replace(' '*3, ' ')
    })

csv_table.close()
