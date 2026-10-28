import pytest
from wordcount import chastota

@pytest.fixture
def fayl_s_textom(tmp_path):
    p = tmp_path / "text.txt"
    p.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return p

def test_chastota_slov(fayl_s_textom):
    res = chastota(fayl_s_textom)
    assert res["мама"] == 2
    assert res["рама"] == 2

def test_net_znakov_prepinaniya(fayl_s_textom):
    res = chastota(fayl_s_textom)
    assert "рама," not in res
    assert "раму." not in res

def test_kolichestvo_unikalnyh(fayl_s_textom):
    res = chastota(fayl_s_textom)
    assert len(res) == 4