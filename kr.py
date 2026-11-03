
class ZapisError(Exception):
    pass
class Izdanie:
    def __init__(self, nazvanie, god):
        if not nazvanie.strip():
            raise ZapisError("Название не может быть пустым")
    @staticmethod
    def check_nazvanie(nazvanie):
        if not str(nazvanie).strip():
            raise ZapisError("Название не может быть пустым")
        return str(nazvanie).strip()
    @staticmethod
    def check_god(god):
        try:
            god_int = int(god)
        except ValueError:
            raise ZapisError("Год должен быть целым числом")
        if not (1800 <= god_int <= 2026):
            raise ZapisError("Год должен быть в диапазоне от 1800 до 2026")
        return god_int
    def vid(self):
        raise NotImplementedError
    def dopolnenie(self):
        raise NotImplementedError

    def __str__(self):
        return f"{self.nazvanie};{self.god};{self.dopolnenie()}"
class Kniga(Izdanie):
    def __init__(self,nazvanie, god, zhanr):
        super().__init__(nazvanie, god)
        self.zhanr = self.chek_zhanr(zhanr)

    @staticmethod
    def check_zhanr(zhanr):
        zhanr_clean = str(zhanr).strip().lower()
        allowed = ["роман", "повесть", "позия", "поэзия", "учебник", "фантастика"]
        if not zhanr_clean:
            raise ZapisError("Отсутствует жанр книги")
        if zhanr_clean not in allowed:
            raise ZapisError(f"Недопустимый жанр: {zhanr}")
        return zhanr_clean
        def vid(self):
            return "книга"
        def dopolnenie(self):
            return self.zhanr
class Zhyrnal(Izdanie):
    def __init__(self, nazvanie, god, nomer):
        super().__init__(nazvanie, god)
        self.nomer = self.check_nomer(nomer)
    def check_nomer(nomer):
        try:
            nomer_int = int(nomer)
        except ValueError:
            raise ZapisError("Номер выпуска должен быть целым числом")
        if not (1 <= nomer_int <= 12):
            raise ZapisError("Номер выпуска должен быть от 1 до 12")
        return nomer_int
    def vid(self):
        return "журнал"
    def dopolnenie(self):
        return f"выпуск {self.nomer}"


def parse_line(line):
    line=line.strip()