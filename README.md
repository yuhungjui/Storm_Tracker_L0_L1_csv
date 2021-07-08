# Storm Tracker L0-L1 CSV

Convert Level-0 Storm Tracker (ST) data to Level-1 csv format for general usage.
The output ascii file can be directly imported to ASPEN for further QC procedures.

More information on **ASPEN**, please see: https://www.eol.ucar.edu/software/aspen & https://ncar.github.io/aspendocs/index.html

Last update - 20210707 - Hungjui Yu

## Dependencies

This script uses **pandas** for data management, and **metpy** for calculating meteorological variables.
More information on **metpy**, please see: https://unidata.github.io/MetPy/latest/index.html

## How to run?

### In single ST mode:
```
python3 ST_L0_L1_csv.py path_to_ST_file log_launch_time_YYYYMMDDHHmmss path_to_output
```

### In batch mode for multiple STs:
```
python3 ST_L0_L1_csv_batch.py
```

The scripit us supported by python3.
The input launch time is a 14-digits UTC date and time from year to second, YYYYMMDDHHmmss.

For example,

```
python3 ST_L0_L1_csv.py ./Example/no_2968.csv 20210503184852
```
