def check_fio(s):
    parts=s.split()
    if len(parts)<2:
        return None
    return " ".join(w.capitalize() for w in parts)
def check_mail(s):
    s=s.strip().lower()
    if s.count("@")!=1:
        return None
    login,domain=s.split("@")
    if not login or not domain:
        return None
    if "." not in domain:
        return None
    if domain.startswith(".") or domain.endswith("."):
        return None
    return s
def check_phone(s):
    digits="".join(ch for ch in s if ch.isdigit())
    if len(digits)!=11:
        return None
    if digits[0] not in ("7","8"):
        return None
    if digits[0]=="8":
        digits="7"+digits[1:]
    return f"+{digits[0]} ({digits[1:4]}) ***-**-{digits[-2:]}"
def check_group(s):
    g=s.strip().lower()
    if not g:
        return None
    return g
def parse_line(line, num):
    parts = line.split(";")
    if len(parts) != 4:
        return f"строка {num}: не 4 поля, а {len(parts)}"
    fio_raw, mail_raw, phone_raw, group_raw = [p.strip() for p in parts]
    fio = check_fio(fio_raw)
    if fio is None:
        return f"строка {num}: неверное ФИО: {fio_raw}"
    mail=check_mail(mail_raw)
    if mail is None:
        return f"Строка {num}: неправильная почта: {mail_raw}"
    phone=check_phone(phone_raw)
    if phone is None:
        return f"Строка {num}: неверный номер: {phone_raw}"
    group=check_group(group_raw)
    if group is None:
        return f"Строка {num}: пустая группа"
    return {"fio": fio, "mail": mail, "phone": phone, "group": group}