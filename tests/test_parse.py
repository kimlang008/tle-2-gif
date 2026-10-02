import pytest
from main import extract_tle, TleFormatError,download_tle, WebServiceError
from datetime import datetime,timezone
import urllib.error

SAMPLE_TLE_ISS="""ISS (ZARYA)   
1 25544U 98067A   26273.85230731  .00003748  00000+0  76931-4 0  9990
2 25544  51.6316 137.1559 0007005 207.6272 152.4345 15.48699564588139"""
SAMPLE_TLE_CSS="""CSS (WENTIAN)           
1 53239U 22085A   26273.77991928  .00013951  00000+0  17026-3 0  9998
2 53239  41.4697  40.7747 0002425 314.4468  45.6172 15.60186162288231"""
#garbage test
SAMPLE_TLE_GARBAGE="""<html>this is the first line
and this is the second line
then the third line</html>"""
SAMPLE_TLE_EMPTY=""""""
SAMPLE_TLE_ONELINE="""<html>only one line</html>"""
SAMPLE_TLE_THREEEMPTYLINES="\n\n\n"
SAMPLE_TLE_UNIQUE="""<html>A
1
2</html>"""

@pytest.fixture
def sample_data():
    return extract_tle(SAMPLE_TLE_ISS)

def test_name(sample_data):
    assert sample_data.name=="ISS (ZARYA)"

@pytest.mark.parametrize(
        "inclination_get,inclination_standard",
        [(SAMPLE_TLE_ISS, 51.6316), (SAMPLE_TLE_CSS, 41.4697)], 
        ids=["ISS", "CSS"])

def test_inclination(inclination_get, inclination_standard):
    parameter_data=extract_tle(inclination_get)
    assert parameter_data.inclination==inclination_standard

def test_eccentricity(sample_data):
    assert sample_data.eccentricity==0.0007005

def test_epoch(sample_data):
    assert sample_data.epoch==datetime(2026, 9, 30, 20, 27, 19, 351584,tzinfo=timezone.utc)

@pytest.mark.parametrize(
    "TLE_format_get",
    [SAMPLE_TLE_GARBAGE, SAMPLE_TLE_EMPTY, SAMPLE_TLE_ONELINE, 
    SAMPLE_TLE_THREEEMPTYLINES,SAMPLE_TLE_UNIQUE],
    ids=["GARBAGE", "EMPTY", "ONELINE", "THREEEMPTYLINES", "UNIQUE"])
def test_TleFormatError(TLE_format_get):
    with pytest.raises(TleFormatError):
        extract_tle(TLE_format_get)

def test_web_yes(monkeypatch):
    class MockResponse():
        def __enter__(self):
            return self
        def __exit__(self,exc_type,exc_value,tb):
            return None
        def read(self):
            return SAMPLE_TLE_ISS.encode('utf-8')
    monkeypatch.setattr("main.urllib.request.urlopen",lambda *args, **kwargs: MockResponse())
    assert download_tle("https://fakeone.com")==SAMPLE_TLE_ISS
def test_web_network_error(monkeypatch):
    def FailMockResponse(*args,**kwargs):
        raise urllib.error.URLError("网络连接失败")
    monkeypatch.setattr("main.urllib.request.urlopen", FailMockResponse)
    with pytest.raises(WebServiceError):
        download_tle("https://fakeone.com")