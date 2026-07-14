import siphon
import xarray as xr 
import pandas as pd
from herbie import Herbie
import metpy
import numpy as np

def check_soil_moisture(date):
    '''Checks whether soil moisture for a certain datetime is less than 25%. Returns true if condition is met.'''
    H = Herbie(date, model='hrrr', product='nat', save_dir='/AshResuspension', overwrite=False, verbose=False, fxx=2)
    ds = H.xarray(r':SOILW:0.01-0.01 m below ground:anl:')

    distance =(
        (ds.latitude - 46.2456657)**2 +
        (ds.longitude - 237.8154585)**2)

    y, x = np.unravel_index(
        distance.argmin(),
        distance.shape
        )

    soil_point = ds.isel(
        y=y,
        x=x
        )

    soil_value = soil_point['soilw'].values

    soil_percent = round(soil_value.item()*100)

    if soil_value <= 0.25:
        return True, soil_percent
    else:
        return False
