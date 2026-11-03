import requests

BASE = "http://127.0.0.1:5000"   # адрес учебного сервера
TIMEOUT = 3                       # таймаут в секундах на каждый запрос


class ServerNedostupen(Exception):
    """Сервер недоступен или ответил ошибкой 500 и выше."""

def _zapros(metod, adres, **parametry):
    try:
        r = requests.request(metod, BASE + adres, timeout=TIMEOUT, **parametry)
    except requests.ConnectionError:
        raise ServerNedostupen("нет соединения — сервер запущен?")
    except requests.Timeout:
        raise ServerNedostupen(f"сервер не ответил за {TIMEOUT} секунд")
    if r.status_code >= 500:
        raise ServerNedostupen(f"сервер ответил ошибкой {r.status_code}")
    return r
def poluchit_ankety():
    return _zapros("GET", "/anketi").json()
def poluchit_anketu(nomer):
    r = _zapros("GET", "/anketi/" + str(nomer))
    if r.status_code == 404:
        return None
    return r.json()
def proverit_pochtu(mail):
    r = _zapros("POST", "/proverka", json={"mail": mail})
    return r.json()["prinyato"]
def poluchit_statistiku():
    return _zapros("GET", "/statistika").json()
