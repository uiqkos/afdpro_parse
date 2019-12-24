# Мануал
1. Зайти в afdpro
2. Написать: tr on
3. Нажимая F1 дойти до выхода из проги
4. Написать: tr off
5. Написать: pt <начало>,<количество>,<имя файла>
6. Создать файл с нужным расширением
7. Запустить скрипт 
### Аргументы
1. trace_file_path (tfp) - путь к исходному файлу
2. table_file_path (tbfp) - путь к итоговому файлу (если файла не существует, то скрипт его создаст)
3. sheet_name (sn) - имя листа
4. tab_top (tt) - отступ сверху
5. type - тип таблицы (csv/excel)
# Примеры
1. python main.py trace_file_path=TRACE.TXT table_file_path=books/trace1.xlsx sheet_name=trace tt=10 type=excel
2. python main.py (Аргументы по умолчанию: trace_file_path='trace.txt', table_file_path='trace.csv', sheet_name='trace', tab_top=0, type='csv')