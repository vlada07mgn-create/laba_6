# storage.py

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None


def save_results(ok_file, errors_file, accepted, rejected):
    with open(ok_file, 'w', encoding='utf-8') as f:
        for line, _ in accepted:
            f.write(line + "\n")

    with open(errors_file, "w", encoding='utf-8') as f:
        for num, line, reason in rejected:
            f.write(f"Строка {num}: {line}\n причина: {reason}\n")