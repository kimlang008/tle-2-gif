import pytest
from PIL import Image
import os
import numpy as np
from main import plot_ground_track

N=3

@pytest.fixture
def gifpath(tmp_path):
    lon=np.linspace(90,00,N)
    lat=np.linspace(00,90,N)
    plot_ground_track(lon,lat,"测试卫星",str(tmp_path/"test.gif"),fps=5)
    return tmp_path/"test.gif"

def test_file_exit(gifpath):
    assert os.path.exists(gifpath)
def test_gif_format(gifpath):
    with Image.open(gifpath) as im:
        assert im.format=="GIF"
        assert im.n_frames==N
        assert im.size==(800,400)