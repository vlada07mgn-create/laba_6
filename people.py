class AnketaError(Exception):
    pass
class Person:
    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_mail(mail)
        self.phone = self.check_phone(phone)
    @staticmethod
    def check_fio(fio):
        parts = fio.split()
        if len(parts) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        return " ".join(w.capitalize() for w in parts)
    @staticmethod
    def check_mail(mail):
        mail = mail.strip().lower()
        if mail.count("@") != 1:
            raise AnketaError(f"неверная почта: {mail}")
        login, domain = mail.split("@")
        if not login or not domain or "." not in domain:
            raise AnketaError(f"неверная почта: {mail}")
        if domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"неверная почта: {mail}")
        return mail
    @staticmethod
    def check_phone(phone):
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) != 11 or digits[0] not in ("7", "8"):
            raise AnketaError(f"неверный телефон: {phone}")
        if digits[0] == "8":
            digits = "7" + digits[1:]
        return digits
    def masked_phone(self):
        return f"+7 ({self.phone[1:4]}) ***-***-{self.phone[-2:]}"
    def short_fio(self):
        parts = self.fio.split()
        if len(parts) == 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        return self.fio
    def role(self):
        return "неизвестно"
    def extra(self):
        return ""
    def __lt__(self, other):
        return self.fio < other.fio
class Student(Person):
    def __init__(self, fio, mail, phone, group):
        super().__init__(fio, mail, phone)
        group = group.strip().lower()
        if not group:
            raise AnketaError("пустая группа")
        self.group = group
    def role(self):
        return "студент"
    def extra(self):
        return self.group
class Teacher(Person):
    def __init__(self, fio, mail, phone, department):
        super().__init__(fio, mail, phone)
        department = department.strip()
        if not department:
            raise AnketaError("пустая кафедра")
        self.department = department
    def role(self):
        return "преподаватель"
    def extra(self):
        return self.department