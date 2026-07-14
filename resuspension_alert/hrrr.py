import requests
import xarray as xr
import numpy as np
from herbie import Herbie
import cfgrib
from datetime import datetime
from pathlib import Path

save_dir=Path("data/wind")
save_dir.mkdir(parents=True, exist_ok=True)

def get_hrrr_data(date):
    '''Gets HRRR model data based on a datetime input. Returns a function in the variable ds.'''
    H = Herbie(date, model="hrrr", priority=['nomads', 'aws', 'google', 'azure', 'pando', 'pando2'], save_dir=save_dir, overwrite=False, verbose=False, fxx=2)
    H.download()
    ds = H.xarray(r":(?:UGRD|VGRD):850 mb:") #hrrr only has 850mb

    distance =(
        (ds.latitude - 46.24178)**2 +
        (ds.longitude - 237.80817)**2)

    y, x = np.unravel_index(
        distance.argmin(),
        distance.shape
        )

    wind_point = ds.isel(
        y=y,
        x=x
        )

    ds = wind_point
    ds = ds.assign(wind_speed=np.sqrt(ds.u**2 + ds.v**2)*1.94384)
    ds = ds.assign(wind_direction=(270 - np.degrees(np.arctan2(ds.v, ds.u))) % 360)

    return ds

def check_wind(date):
    '''Checks to see if wind meets the criteria:
            wind speed > 15 kts
            wind direction between 45 and 150 degrees'''
    ds = get_hrrr_data(date)
    
    wind_mask = (
    (ds.wind_speed >= 1) &
    (ds.wind_direction >= 45) &
    (ds.wind_direction <= 150)
    )

    wind_ok = wind_mask.any()

    return wind_ok.item(), round(ds.wind_speed.item()), round(ds.wind_direction.item())
