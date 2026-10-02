import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta,timezone
import urllib.request
import urllib.error
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from matplotlib.animation import FuncAnimation,PillowWriter
from skyfield.api import EarthSatellite, load, wgs84


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
        epoch=epoch.replace(tzinfo=timezone.utc)
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
        with urllib.request.urlopen(url,timeout=10) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        raise WebServiceError("无法从指定URL获取TLE数据") from e

def plot_ground_track(lon,lat,satellite,path,fps=10):
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False
    fig,ax = plt.subplots(
        figsize=(8,4),
        dpi=100,
        subplot_kw={"projection":ccrs.PlateCarree()})
    ax.coastlines()
    ax.set_extent([-180,180,-90,90],crs=ccrs.PlateCarree())
    gl=ax.gridlines(draw_labels=True)
    gl.top_labels=False
    gl.right_labels=False
    ax.set_title(f"{satellite} TLE 2 GIF")
    lons=lon.copy()
    dif=np.abs(np.diff(lons))>180
    lons[1:][dif]=np.nan

    
    ax.plot(lon,lat,transform=ccrs.PlateCarree())
    点,= ax.plot([],[],"o",transform=ccrs.PlateCarree())


    def update(i):
        点.set_data([lon[i]],[lat[i]])
        return (点,)

    anim = FuncAnimation(fig,update,frames=len(lon),)
    anim.save(path,writer=PillowWriter(fps=fps))
    plt.close(fig)

def para_calc(tletxt:str,start=None,step_s=30,count=180):
    lines=tletxt.splitlines()
    name=lines[0].strip()
    line1=lines[1]
    line2=lines[2]

    ts = load.timescale(builtin=True)
    sat =EarthSatellite(line1,line2,name,ts)
    if start is None:
        start =sat.epoch.utc_datetime()
    t = ts.from_datetime(start)+np.arange(count)*step_s/86400
    dts=t.utc_datetime()
    sub =wgs84.subpoint(sat.at(t))
    span=(dts[-1]-dts[0]).total_seconds()
    
    lat=sub.latitude.degrees
    lon=sub.longitude.degrees
    height=sub.elevation.km
    return lon,lat,height,span    
    
def main():
    #给argparse预留
    #url先用iss的，一会加入arg再改为可输入
    url="https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"
    tle_str=download_tle(url)
    tlePara=extract_tle(tle_str)
    lon,lat,height,span=para_calc(tle_str,start=tlePara.epoch,step_s=30,count=180)
    plot_ground_track(lon,lat,TlePara.name,"out.gif",fps=10)

if __name__=="__main__":
    main()
