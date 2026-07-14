import siphon
import xarray as xr 
import pandas as pd
from herbie import Herbie
import metpy
import numpy as np
from pathlib import Path
from datetime import timedelta

save_dir = Path("data/soil_moisture")
save_dir.mkdir(parents=True, exist_ok=True)

def get_latest_soil_analysis(date):
    """Return the newest HRRR soil moisture analysis available."""

    for hours_back in range(0, 24):
        test_date = date - timedelta(hours=hours_back)

        try:
            H = Herbie(
                test_date,
                model="hrrr",
                product="nat",
                fxx=0,
                save_dir=save_dir,
                overwrite=False,
                verbose=False,
            )
            H.download()
            ds = H.xarray(r':SOILW:0.01-0.01 m below ground:anl:')
            return ds

        except Exception:
            continue

    raise RuntimeError("No recent HRRR soil moisture analysis found.")

def check_soil_moisture(date):
    '''Checks whether soil moisture for a certain datetime is less than 25%. Returns true if condition is met.'''
    ds = get_latest_soil_analysis(date)
    # H = Herbie(date, model='hrrr', priority=['aws', 'nomads', 'google', 'azure', 'pando', 'pando2'], product='nat', save_dir=save_dir, overwrite=False, verbose=False)
    # H.download()
    # ds = H.xarray(r':SOILW:0.01-0.01 m below ground:')
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
