
# main.py
from validators import parse_line
from report import print_table
from storage import read_file, save_results
input_file = "anketa.txt"
ok_file = "ok.txt"
errors_file = "errors.txt"
print(f"--- Начинаем обработку файла: {input_file} ---")
def main():
    lines = read_file(input_file)
    if lines is None:
        return
    accepted = []  # Список пар (строка, словарь)
    rejected = []  # Список кортежей (номер, строка, причина)
    for num, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        # Вызываем функцию из модуля validators
        result = parse_line(line, num)

        if isinstance(result, dict):
            accepted.append((line, result))
        else:
            rejected.append((num, line, result))

    accepted.sort(key=lambda item: item[1]["fio"])
    # Таблица
    records = [rec for _, rec in accepted]
    print_table(records)
    # Отклонённые
    print(f"\nотклонено строк: {len(rejected)}")
    for num, line, reason in rejected:
        print(f"  Cтрока {num}: {line}")
        print(f"    Причина: {reason}")
    # Итог
    print(f"\nВсего строк в файле: {len(lines)}")
    print(f"Принято: {len(accepted)} | Отклонено: {len(rejected)}")
    # По группам
    stat = {}
    for _, rec in accepted:
        stat[rec["group"]] = stat.get(rec["group"], 0) + 1
    print("\nПо группам: ")
    for g in sorted(stat):
        print(f"  {g}: {stat[g]}")
    # Сохранение (вызываем функцию из storage)
    save_results(ok_file, errors_file, accepted, rejected)
# Защита от запуска при импорте
if __name__ == "__main__":
    main()