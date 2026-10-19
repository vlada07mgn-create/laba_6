def print_table(records):
    print(f"{'№':<4}{'ФИО':<28}{'Почта':<30}{'Телефон':<20}{'Группа'}")
    print("-"*90)
    for i, rec in enumerate(records,start=1):
        fio=rec["fio"][:27]
        mail=rec["mail"][:28]
        print(f"{i:<4}{fio:<28}{mail:<30}{rec['phone']:<20}{rec['group']}")