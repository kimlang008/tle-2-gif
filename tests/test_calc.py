import math

import pytest

from main import extract_tle, para_calc

SAMPLE_TLE_ISS = """ISS (ZARYA)   
1 25544U 98067A   26273.85230731  .00003748  00000+0  76931-4 0  9990
2 25544  51.6316 137.1559 0007005 207.6272 152.4345 15.48699564588139"""


@pytest.fixture
def track():
    lon, lat, height, span = para_calc(SAMPLE_TLE_ISS)
    return lon, lat, height, span


def test_height(track):
    mean_motion = extract_tle(SAMPLE_TLE_ISS).mean_motion
    T = 86400 / mean_motion
    miu = 398600.4418
    a = math.cbrt(miu * (T**2) / (4 * math.pi**2))
    expect_height = a - 6371
    delta = abs(expect_height - track[2])
    assert (delta < 20).all()


def test_lat(track):
    inclination = extract_tle(SAMPLE_TLE_ISS).inclination
    assert (abs(track[1]) <= inclination + 0.3).all()  # 0.3 大地纬度与地心纬度的差异


def test_span(track):
    assert abs(5370 - track[3]) <= 1
