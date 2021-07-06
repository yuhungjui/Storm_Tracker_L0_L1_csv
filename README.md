# Storm Tracker L0-L1 SHARPpy

Convert Level-0 Storm Tracker (ST) data to Level-1 SHARPpy format for skew-T plot using SHARPpy.
The output ascii file can be directly read by SHARPpy for skew-T diagram.

More information on **SHARPpy**, please see: https://sharppy.github.io/SHARPpy/index.html

Last update - 20210526 - Hungjui Yu

## Dependencies

This script uses **pandas** for data management, and **metpy** for calculating meteorological variables.
More information on **metpy**, please see: https://unidata.github.io/MetPy/latest/index.html

## How to run?

```
python3 ST_L0_L1_SHARPpy.py [/path/to/ST/file/no_XXXX.csv] [log_launch_time_YYYYMMDDHHmmss]
```

The scripit us supported by python3.

Where XXXX is the serial number of the ST.
Specifically for PRE-CIP 2021 field campaign, the ST serial numbers are 2XXX.
The input launch time is a 14-digits UTC date and time from year to second, YYYYMMDDHHmmss.

For example,

```
python3 ST_L0_L1_SHARPpy.py ./Example/no_2968.csv 20210503184852
```

## p.s.

Feel free to play around the scripts and data in the Example folder.
