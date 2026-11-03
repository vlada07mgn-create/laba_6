import json

from people import AnketaError, Student, Teacher
from registry import Registry
from client import (
    ServerNedostupen,
    poluchit_ankety,
    poluchit_statistiku,
    proverit_pochtu,
)

def sobrat_person(d, rej):
    nomer = d.get("nomer", "?")
    tip = d.get("tip", "")
    try:
        if tip == "s":
            rej.add(Student(d["fio"], d["mail"], d["phone"], d.get("gruppa", "")))
        elif tip == "t":
            rej.add(Teacher(d["fio"], d["mail"], d["phone"], d.get("kafedra", "")))
        else:
            raise AnketaError(f"неизвестный тип: {tip}")
    except AnketaError as e:
        rej.rejected.append((nomer, str(d), str(e)))
    except KeyError as e:
        rej.rejected.append((nomer, str(d), f"нет обязательного поля {e}"))

def pechat_tablitsy(rej):
    print()
    print("=" * 108)
    print(f"{'№':>3}  {'ФИО':<32}{'Почта':<27}{'Телефон':<22}{'Роль':<14}{'Доп.'}")
    print("-" * 108)
    for i, p in enumerate(rej.accepted, start=1):
        print(f"{i:>3}  {p.fio:<32}{p.mail:<27}{p.masked_phone():<22}{p.role():<14}{p.extra()}")
    print("=" * 108)

def main():
    rej = Registry()
    istochnik = None

    dannye = None
    try:
        dannye = poluchit_ankety()
    except ServerNedostupen as e:
        print("Сервер недоступен:", e)

    if dannye is not None:
        istochnik = "сервер"
        print("Источник данных: сервер http://127.0.0.1:5000")
        for d in dannye:
            sobrat_person(d, rej)
        rej.accepted.sort()
    elif rej.load("anketa.txt"):
        istochnik = "запасной файл"
        print("Источник данных: запасной файл anketa.txt")
    else:
        print("Нет ни сервера, ни запасного файла anketa.txt.")
        print("Запустите сервер (python server.py) или положите anketa.txt рядом с программой.")
        return

    pechat_tablitsy(rej)
    print(f"\nПринято: {len(rej)} | Отклонено: {len(rej.rejected)}")

    if rej.rejected:
        print("\nОтклонённые анкеты:")
        for nomer, zapis, prichina in rej.rejected:
            print(f"  анкета {nomer}: {zapis}")
            print(f"    причина: {prichina}")
    print("\nСводка по ролям:", rej.get_stats_by_roles())

    try:
        print("Статистика сервера:", poluchit_statistiku())
        print("  Сервер считает все свои анкеты — он их не проверяет.")
        print("  Мы считаем только принятые, поэтому наши числа меньше.")
    except ServerNedostupen as e:
        print("Статистику сервера получить не удалось:", e)

    print("\nПроверка почты на сервере:")
    for p in rej.accepted:
        try:
            otvet = proverit_pochtu(p.mail)
        except ServerNedostupen as e:
            print(f"  {p.mail} — сервер недоступен ({e})")
        else:
            print(f"  {p.mail} — {'принята' if otvet else 'отклонена'}")

    otchet = {
        "istochnik": istochnik,
        "prinyato": len(rej),
        "otkloneno": len(rej.rejected),
        "prinjatye": [
            {"fio": p.fio, "mail": p.mail, "phone": p.phone,
             "rol": p.role(), "dopolnenie": p.extra()}
            for p in rej.accepted
        ],
        "otklonennye": [
            {"nomer": n, "zapis": z, "prichina": pr}
            for n, z, pr in rej.rejected
        ],
        "svodka_po_rolam": rej.get_stats_by_roles(),
    }
    with open("otchet.json", "w", encoding="utf-8") as f:
        json.dump(otchet, f, ensure_ascii=False, indent=4)
    print("\nОтчёт сохранён в otchet.json")


if __name__ == "__main__":
    main()
