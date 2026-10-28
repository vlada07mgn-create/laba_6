import pytest
from people import Person, Student, Teacher, AnketaError
#  ФИО приводится к одному виду
@pytest.mark.parametrize("raw, expected", [
    ("иванов иван петрович", "Иванов Иван Петрович"),
    ("  пЕтРов   пЁтР  петрович", "Петров Пётр Петрович"),
    ("СИДОРОВ алексей", "Сидоров Алексей"),
    ("смирнов а.в.", "Смирнов А.В."),
])
def test_fio_normalization(raw, expected):
    assert Person.check_fio(raw) == expected
#  ФИО из одного слова отклоняется
def test_fio_one_word_error():
    with pytest.raises(AnketaError):
        Person.check_fio("Иванов")
#  Почта приводится к нижнему регистру
@pytest.mark.parametrize("raw, expected", [
    ("IVANOV@MAIL.RU", "ivanov@mail.ru"),
    ("  Petrov@Yandex.Ru  ", "petrov@yandex.ru")
])
def test_mail_lowercase(raw, expected):
    assert Person.check_mail(raw) == expected
#  Плохая почта отклоняется
@pytest.mark.parametrize("bad_mail", [
    "ivanovmail.ru",     # нет @
    "ivanov@@mail.ru",   # две @
    "@mail.ru",          # пустой логин
    "ivanov@",           # пустой домен
    "ivanov@mail",       # нет точки в домене
    "ivanov@.mail.ru",   # точка в начале домена
])
def test_mail_bad(bad_mail):
    with pytest.raises(AnketaError):
        Person.check_mail(bad_mail)
#  Телефон приводится к одному виду (все 4 записи дают один результат)
@pytest.mark.parametrize("phone_raw", [
    "+7 (921) 111-22-33",
    "89211112233",
    "8 921 111 22 33",
    "+79211112233"
])
def test_phone_normalization(phone_raw):
    assert Person.check_phone(phone_raw) == "79211112233"
#  Плохой телефон отклоняется
@pytest.mark.parametrize("bad_phone", [
    "123",              # мало цифр
    "+7 (921) 111-22-33 4", # много цифр
    "+6 (921) 111-22-33",   # неверный код страны (не 7 и не 8)
])
def test_phone_bad(bad_phone):
    with pytest.raises(AnketaError):
        Person.check_phone(bad_phone)
#  Телефон выводится с маской
def test_phone_mask():
    p = Person("Иванов Иван", "ivanov@mail.ru", "+79211112233")
    assert p.masked_phone() == "+7 (921) ***-***-33"
# ФИО сокращается до инициалов
def test_short_fio():
    p = Person("Иванов Иван Петрович", "ivanov@mail.ru", "+79211112233")
    assert p.short_fio() == "Иванов И. П."
#  Студент и преподаватель отвечают по-разному
def test_roles():
    s = Student("Иванов Иван", "ivanov@mail.ru", "+79211112233", "09с33")
    t = Teacher("Петров Петр", "petrov@mail.ru", "+79212223344", "Кафедра И9")
    assert s.role() == "студент"
    assert t.role() == "преподаватель"
    assert s.extra() == "09с33"
    assert t.extra() == "Кафедра И9"
#  Студент без группы отклоняется
def test_student_no_group():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "ivanov@mail.ru", "+79211112233", "")
def test_fio_dvoynaya_familiya():
    assert Person.check_fio("петров-водкин кузьма") == "Петров-Водкин Кузьма"
def test_mail_with_space():
    with pytest.raises(AnketaError):
        Person.check_mail("iv anov@mail.ru")
def test_sort_with_yo():
    p1 = Person("Яковлева Анна", "y@mail.ru", "79211112233")
    p2 = Person("Ёлкина Мария", "e@mail.ru", "79211112233")
    p3 = Person("Абрамова Ольга", "a@mail.ru", "79211112233")
    # Сортируем список объектов
    people = sorted([p1, p2, p3])
    result_names = [p.fio for p in people]
    assert result_names == ["Абрамова Ольга", "Ёлкина Мария", "Яковлева Анна"]