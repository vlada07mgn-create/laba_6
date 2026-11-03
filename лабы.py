import requests
BASE="http://127.0.0.1:5000"

mails=["ivanov@mail.ru", "kuznetsov.mail.ru"]
for mail in mails:
    r=requests.post(BASE + "/proverka", json={"mail": mail})
    prinyato=r.json()["prinyato"]
    print(f"почта:{mail} | код ответа: {r.status_code} | принято: {prinyato}" )