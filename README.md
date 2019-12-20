# Установка
## Archlinux
1. Скачиваем архив
2. pacman -U <имя архива>

## Windows, Other
1. Скачиваем исходники
2. Добавляем в патх (не обязательно)

# Подготовка
1. Зайти в afdpro
2. Написать: tr on
3. Нажимая F1 дойти до выхода из проги
4. Написать: tr off
5. Написать: pt <начало>,<количество>,<имя файла>
6. В результате получаем .txt файл

# Использование
## Linux
 - parse_afdpro  disassemble_to_csv  make_trace_csv (если в path)
 - ./parse_afdpro ./disassemble_to_csv ./make_trace_csv (в папке с исходниками)
 ## Windows
 - python parse_afdpro / disassemble_to_csv / make_trace_csv
# Аргументы (для parse_afdpro)
1. trace_file_path (tfp) - путь к исходному файлу
2. table_file_path (tbfp) - путь к итоговому файлу (если файла не существует, то скрипт его создаст)
3. type - тип таблицы (csv/excel)
4. sheet_name (sn) - имя листа (только для excel)
5. tab_top (tt) - отступ сверху (только для excel)
Аргументы по умолчанию: 
  trace_file_path='trace.txt', 
  table_file_path='trace.csv', 
  sheet_name='trace', 
  tab_top=0, 
  type='csv'
  
# Примеры
1. python parse_afdpro trace_file_path=TRACE.TXT table_file_path=books/trace1.xlsx sheet_name=trace tt=10 type=excel
2. disassemble_to_csv file.com
3. parse_afdpro tfp=trace.txt tbfp=trace.csv type=csv
