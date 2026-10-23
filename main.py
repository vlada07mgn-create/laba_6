from registry import Registry
def main():
    reg = Registry()
    if not reg.load("anketa.txt"):
        print("Ошибка: файл anketa.txt не найден.")
        return
    print(f"{'№':<3}{'ФИО':<35}{'Роль':<15}{'Группа/Кафедра':<18}{'Телефон'}")
    print("-" * 95)
    for i, person in enumerate(reg.accepted, start=1):
        print(f"{i:<3}{person.fio:<35}{person.role():<15}{person.extra():<18}{person.masked_phone()}")
    if reg.rejected:
        print(f"\nВсего отклонено: {len(reg.rejected)}")
        for num, line, reason in reg.rejected:
            print(f"  строка {num}: {reason}")
    print(f"\nПринято: {len(reg)} | Отклонено: {len(reg.rejected)}")
    print("\nПо ролям:")
    for role, count in reg.get_stats_by_roles().items():
        print(f"  {role}: {count}")
    print("\nПо группам:")
    for group, count in reg.get_stats_by_groups().items():
        print(f"  {group}: {count}")
    reg.save()
    print("\nДанные сохранены в ok.txt и errors.txt")
if __name__ == "__main__":
    main()