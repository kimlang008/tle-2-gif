import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
import urllib.request

TLE_WRONG_FORMAT_ERROR="所给内容不是TLE参数，应为三行固定宽度文本"

@dataclass
class TlePara:
    name:str
    epoch:datetime
    inclination:float
    raan:float
    eccentricity:float
    arg_perigee:float
    mean_anomaly:float
    mean_motion:float

class TleFormatError(Exception):
    pass

def extract_tle(tle_str:str)->TlePara:
    lines=tle_str.splitlines()
    if (len(lines)!=3)or(not lines[1].startswith("1"))or(not lines[2].startswith("2")):
        raise TleFormatError(TLE_WRONG_FORMAT_ERROR)
    try:
        name=lines[0].strip()
        epoch_year=float(lines[1][18:20].strip())
        epoch_day=float(lines[1][20:32].strip())
        if epoch_year<57:
            epoch_year+=2000
        else:
            epoch_year+=1900
        epoch=datetime(int(epoch_year),1,1)+timedelta(days=(epoch_day)-1)
        inclination=float(lines[2][8:16].strip())
        raan=float(lines[2][17:25].strip())
        eccentricity=float("0."+lines[2][26:33].strip())
        arg_perigee=float(lines[2][34:42].strip())
        mean_anomaly=float(lines[2][43:51].strip())
        mean_motion=float(lines[2][52:63].strip())
        return TlePara(
            name=name,
            epoch=epoch,
            inclination=inclination,
            raan=raan,
            eccentricity=eccentricity,
            arg_perigee=arg_perigee,
            mean_anomaly=mean_anomaly,
            mean_motion=mean_motion
        )
    except (IndexError, ValueError) as e:
        raise TleFormatError(TLE_WRONG_FORMAT_ERROR)from e

class WebServiceError(Exception):
    pass
def download_tle(url):
    try:
        response = urllib.request.urlopen(url,timeout=10)
        return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        raise WebServiceError("无法从指定URL获取TLE数据") from e