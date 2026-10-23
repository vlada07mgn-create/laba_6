from people import Student, Teacher, AnketaError
class Registry:
    def __init__(self):
        self.accepted = []  # Список объектов (Student или Teacher)
        self.rejected = []  # Список кортежей (номер строки, текст строки, причина)
    def add(self, person):
        self.accepted.append(person)
    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            return False
        for num, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                person = self.parse_line(line)
                self.add(person)
            except AnketaError as e:
                # Если ошибка — записываем в брак
                self.rejected.append((num, line, str(e)))
        self.accepted.sort()
        return True
    @staticmethod
    def parse_line(line):
        parts = [p.strip() for p in line.split(";")]
        if len(parts) != 5:
            raise AnketaError(f"не 5 полей, а {len(parts)}")
        p_type, fio, mail, phone, extra = parts
        if p_type == "s":
            return Student(fio, mail, phone, extra)
        elif p_type == "t":
            return Teacher(fio, mail, phone, extra)
        else:
            raise AnketaError(f"неизвестный тип: {p_type}")
    # Методы для статистики
    def get_stats_by_roles(self):
        stats = {}
        for p in self.accepted:
            role = p.role()
            stats[role] = stats.get(role, 0) + 1
        return stats
    def get_stats_by_groups(self):
        stats = {}
        for p in self.accepted:
            if p.role() == "студент":
                group = p.extra()
                stats[group] = stats.get(group, 0) + 1
        return stats
    def __len__(self):
        return len(self.accepted)
    def save(self, ok_file="ok.txt", errors_file="errors.txt"):
        with open(ok_file, "w", encoding="utf-8") as f:
            for p in self.accepted:
                f.write(f"{p.fio}; {p.mail}; {p.phone}; {p.extra()}\n")
        with open(errors_file, "w", encoding="utf-8") as f:
            for num, line, reason in self.rejected:
                f.write(f"строка {num}: {line}\n  причина: {reason}\n")