import sys
from logstats import count_levels, format_report, top_errors

def main():
    # Читаем имя файла журнала из первой строки ввода
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return

    path = input_data[0].strip()
    if not path:
        return

    total_lines = 0
    error_count = 0
    broken_count = 0

    # Первый проход: считаем общее число разобранных строк, ERROR и BROKEN через построчное чтение with open
    try:
        with open(path, encoding="utf-8") as f:
            counts = count_levels(f)
            
        # Общее число разобранных строк = сумма всех успешных уровней (без BROKEN)
        total_lines = sum(counts.values())
        error_count = counts.get("ERROR", 0)
        broken_count = counts.get("BROKEN", 0)
    except FileNotFoundError:
        print(f"Файл {path} не найден.")
        return

    # Печать трёх требуемых чисел в stdout
    print(total_lines)
    print(error_count)
    print(broken_count)

    # Второй проход: собираем топ частых ошибок и генерируем текст отчёта
    with open(path, encoding="utf-8") as f:
        errors_top = top_errors(f, n=3)

    report_text = format_report(counts, errors_top)

    # Записываем отчёт в report.txt рядом с скриптом в кодировке UTF-8
    with open("report.txt", "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

if __name__ == "__main__":
    main()
