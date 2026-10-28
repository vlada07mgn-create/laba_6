def summa(a, b):
    return a + b
def skidka(cena, procent):
    if procent < 0 or procent > 90:
        raise ValueError("Скидка должна быть от 0 до 90%")
    return round(cena * (1 - procent / 100), 2)
def srednee(spisok):
    if not spisok:
        raise ValueError("Пустой список")
    return sum(spisok) / len(spisok)