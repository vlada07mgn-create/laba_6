import string


def chastota(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read().lower()

    # Убираем знаки препинания по краям слов
    words = [w.strip(string.punctuation) for w in text.split()]
    # Убираем пустые строки, если вдруг остались
    words = [w for w in words if w]

    result = {}
    for w in words:
        result[w] = result.get(w, 0) + 1
    return result