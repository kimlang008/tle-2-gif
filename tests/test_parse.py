import pytest
from main import extract_tle, TleFormatError
from datetime import datetime

SAMPLE_TLE="""ISS (ZARYA)   
1 25544U 98067A   26273.85230731  .00003748  00000+0  76931-4 0  9990
2 25544  51.6316 137.1559 0007005 207.6272 152.4345 15.48699564588139"""


def test_name():
    Para=extract_tle(SAMPLE_TLE)
    assert Para.name=="ISS (ZARYA)"
def test_inclination():
    Para=extract_tle(SAMPLE_TLE)
    assert Para.inclination==51.6316
def test_eccentricity():
    Para=extract_tle(SAMPLE_TLE)
    assert Para.eccentricity==0.0007005
def test_epoch():
    Para=extract_tle(SAMPLE_TLE)
    assert Para.epoch==datetime(2026, 9, 30, 20, 27, 19, 351584)
def test_TleFormatError():
    with pytest.raises(TleFormatError):
        extract_tle("<html>这不是一个有效的TLE格式</html>")