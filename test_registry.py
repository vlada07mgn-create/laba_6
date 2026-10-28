import pytest
from registry import Registry
# Фикстура создаёт временный файл и загружает его в журнал
@pytest.fixture
def test_registry(tmp_path):
    p = tmp_path / "anketa_test.txt"
    # 3 правильные строки и 3 с ошибками
    p.write_text(
        "s; Иванов Иван; ivanov@mail.ru; +79211112233; 09с33\n"
        "t; Петров Петр; petrov@mail.ru; 89212223344; Кафедра И9\n"
        "s; Сидоров Алексей; sidorov@mail.ru; +79213334455; 09с34\n"
        "x; Неверный тип; bad@mail.ru; +79211112233; 09с33\n"
        "s; Смирнов; smirnov@mail.ru; +79211112233; 09с33\n"
        "s; Кузнецов Павел; kuznetsov.mail.ru; +79211112233; 09с33\n",
        encoding="utf-8"
    )
    reg = Registry()
    reg.load(str(p))
    return reg
#  Пустой журнал имеет длину ноль
def test_registry_empty():
    assert len(Registry()) == 0
#  После загрузки в журнале ровно три анкеты
def test_registry_load_ok(test_registry):
    assert len(test_registry) == 3
#  В списке брака ровно три записи
def test_registry_load_errors(test_registry):
    assert len(test_registry.rejected) == 3
#  У записей брака правильные номера строк (4, 5, 6)
def test_registry_error_lines(test_registry):
    lines = [item[0] for item in test_registry.rejected]
    assert lines == [4, 5, 6]
#  Загрузка несуществующего файла возвращает False
def test_registry_no_file(tmp_path):
    reg = Registry()
    assert reg.load(str(tmp_path / "no_file.txt")) is False
#  Счётчик ролей даёт верный словарь
def test_stats_roles(test_registry):
    stats = test_registry.get_stats_by_roles()
    assert stats == {"студент": 2, "преподаватель": 1}
#  Счётчик групп считает только студентов
def test_stats_groups(test_registry):
    stats = test_registry.get_stats_by_groups()
    assert stats == {"09с33": 1, "09с34": 1}
#  Журнал перебирается циклом for
def test_registry_iter(test_registry):
    count = 0
    for person in test_registry.accepted:
        count += 1
    assert count == 3
#  Сортировка по алфавиту ставит фамилии в правильном порядке
def test_registry_sort(test_registry):
    names = [p.fio for p in test_registry.accepted]
    assert names == ["Иванов Иван", "Петров Петр", "Сидоров Алексей"]
#  Сохранение в файлы
def test_save_ok(test_registry, tmp_path):
    ok_file = tmp_path / "ok.txt"
    test_registry.save(str(ok_file), str(tmp_path / "err.txt"))
    lines = ok_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3
def test_save_errors(test_registry, tmp_path):
    err_file = tmp_path / "errors.txt"
    test_registry.save(str(tmp_path / "ok.txt"), str(err_file))
    content = err_file.read_text(encoding="utf-8")
    assert "неизвестный тип" in content