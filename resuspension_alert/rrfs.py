import requests
import xarray as xr
import numpy as np
from herbie import Herbie
import cfgrib
from datetime import datetime, timedelta
from pathlib import Path

save_dir=Path("data/wind")
save_dir.mkdir(parents=True, exist_ok=True)

def get_rrfs_data(date, max_back=3):
    '''Gets RRFS model data based on a datetime input. Returns a function in the variable ds.'''

    last_error = None

    for hours_back in range(max_back+1):
        run_time = date - timedelta(hours=hours_back)
        fxx = 2 + hours_back

        try:
            H = Herbie(run_time, model="rrfs", priority=['nomads', 'aws', 'google', 'azure', 'pando', 'pando2'], save_dir=save_dir, overwrite=False, verbose=False, fxx=fxx)
            H.download()
            ds = H.xarray(r":(?:UGRD|VGRD):(?:850|825|800|775|750) mb:")
            print(f'Using run {run_time:%Y-%m-%d %H}, {fxx:02d}')
            break

        except Exception as e:
            last_error = e
            print(f'{run_time:%H}Z {fxx:02d} unavailable.')

    else:
        raise RuntimeError('No useable RRFS data found.') from last_error
        
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
            wind speed > 10 kts
            wind direction between 45 and 150 degrees'''
    ds = get_rrfs_data(date)
    
    wind_ok = (
    (ds.wind_speed >= 15) &
    (ds.wind_direction >= 45) &
    (ds.wind_direction <= 160)
    ).any(dim='isobaricInhPa')

    wind_index = ds.wind_speed.argmax(dim='isobaricInhPa')

    max_wind = ds.wind_speed.isel(isobaricInhPa=wind_index)
    max_wind_direction = ds.wind_direction.isel(isobaricInhPa=wind_index)
    max_wind_level = ds.isobaricInhPa.isel(isobaricInhPa=wind_index)

    wind_800 = ds.wind_speed.sel(isobaricInhPa=800)
    wind_direction_800 = ds.wind_direction.sel(isobaricInhPa=800)

    return wind_ok.item(), round(max_wind.item()), round(max_wind_direction.item()), round(max_wind_level.item()), round(wind_800.item()), round(wind_direction_800.item())
