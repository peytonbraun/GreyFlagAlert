import requests
import xarray as xr
import numpy as np
from herbie import Herbie
import cfgrib
from datetime import datetime

def get_gfs_data(date):
    '''Gets GFS model data based on a datetime input. Returns a function in the variable ds.'''
    H = Herbie(date, model="gfs", save_dir="/AshResuspension", overwrite=False, verbose=False, fxx=1)
    ds = H.xarray(r":(?:UGRD|VGRD):(?:850|825|800|775|750) mb:").sel(latitude=46.15, longitude=238, method='nearest')
    ds = ds.assign(wind_speed=np.sqrt(ds.u**2 + ds.v**2))
    ds = ds.assign(wind_direction=(270 - np.degrees(np.arctan2(ds.v, ds.u))) % 360)

    return ds

def check_wind(date):
    '''Checks to see if wind meets the criteria:
            wind speed > 15 kts
            wind direction between 45 and 150 degrees'''
    ds = get_gfs_data(date)
    
    wind_mask = (
    (ds.wind_speed >= 1) &
    (ds.wind_direction >= 45) &
    (ds.wind_direction <= 150)
    )

    wind_ok = wind_mask.any(dim="isobaricInhPa")

    max_wind = ds.wind_speed.values.max()
    max_wind_index = np.where(ds.wind_speed.values.max())
    max_wind_direction = ds.wind_direction[max_wind_index]

    return wind_ok.item(), round(max_wind), round(max_wind_direction.item())
