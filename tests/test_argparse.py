import pytest
import sys
from main import main,TleFormatError,WebServiceError
SAMPLE_TEST="""ISS (ZARYA)   
1 25544U 98067A   26273.85230731  .00003748  00000+0  76931-4 0  9990
2 25544  51.6316 137.1559 0007005 207.6272 152.4345 15.48699564588139"""


def test_no_cmd(monkeypatch):
    monkeypatch.setattr(sys,"argv",["main.py"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code==3

def test_wrong_cmd(monkeypatch):
    monkeypatch.setattr(sys,"argv",["main.py","fake_cmd"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code==2

def test_standard_run(monkeypatch):
    gothrough=[]
    def download_gothrough(url):
        gothrough.append(url)
        return SAMPLE_TEST
    monkeypatch.setattr("main.download_tle",download_gothrough)     
    monkeypatch.setattr("main.plot_ground_track",lambda *args, **kwargs:None)
    monkeypatch.setattr(sys,"argv",["main.py","draw","htstps://test_address"])
    main()
    assert gothrough

def test_wrongTle(monkeypatch,capsys):
    def fake_download(url):
        return "不是TLE"
    monkeypatch.setattr("main.download_tle",fake_download)
    monkeypatch.setattr(sys,"argv",["main.py","draw","https://test_address"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code==3
    err=capsys.readouterr().err
    assert "TLE" in err

def test_fail_web(monkeypatch,capsys):
    def fail_download(url):
        raise(WebServiceError("网络异常，无法获取TLE数据"))
    monkeypatch.setattr("main.download_tle",fail_download)
    monkeypatch.setattr(sys,"argv",["main.py","draw","https://test_address"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code==3
    err=capsys.readouterr().err
    assert "网络"in err

def test_debug_on(monkeypatch,capsys):
    monkeypatch.setattr("main.plot_ground_track", lambda *a, **k: None)
    monkeypatch.setattr("main.download_tle", lambda url: SAMPLE_TEST)
    monkeypatch.setattr(sys,"argv",["main.py","--debug","draw",
            "https://test_address"])
    main()
    out=capsys.readouterr().out
    assert "inclination" in out

def test_debug_close(monkeypatch,capsys):
    monkeypatch.setattr("main.plot_ground_track", lambda *a, **k: None)
    monkeypatch.setattr("main.download_tle", lambda url: SAMPLE_TEST)
    monkeypatch.setattr(sys,"argv",["main.py","draw",
            "https://test_address"])
    main()
    out=capsys.readouterr().out
    assert "inclination" not in out
        