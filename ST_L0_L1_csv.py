"""
Transform Storm Tracker L0 data to L1 csv format file.
Hungjui Yu
20210706

How to run:
ST_L0_L1_csv path_to_ST_file log_launch_time_YYYYMMDDHHmmss path_to_output
"""

import sys
import pandas as pd
from datetime import datetime
import pytz
# import metpy.calc as mpcalc
from metpy.calc import dewpoint_from_relative_humidity
from metpy.units import units

# %%
# Set L0 ST files path:
ST_file_path = sys.argv[1]

# Set ST node number:
ST_no = sys.argv[1][-8:-4]

# Set ST launch time (UTC):
launch_time_from_log = sys.argv[2]

# Set L1 ST file output path:
output_path = sys.argv[3]

# %%
# Functions:

def load_st_file(ST_no, launch_time_from_log, ST_file_path):

    # Specified timezones:
    # pytz.all_timezones
    tz_utc = pytz.timezone('UTC')
    tz_fc = pytz.timezone('US/Mountain')

    # Specified the launch time in UTC:
    launch_time = datetime.strptime(launch_time_from_log, '%Y%m%d%H%M%S')
    launch_time_utc = tz_utc.localize(launch_time)

    # print(launch_time_utc)
    # print(launch_time_from_log[:8])

    # Load raw data:
    # L0_raw_data = pd.read_csv(ST_file_path + '/no_{}.csv'.format(ST_no))
    L0_raw_data = pd.read_csv(ST_file_path)

    return launch_time_utc, L0_raw_data

def conversion_L0_L1(loaded_ST_file):

    launch_time_utc = loaded_ST_file[0]
    L0_raw_data = loaded_ST_file[1]

    tz_utc = pytz.timezone('UTC')

    # Convert the data time to datetime object:
    L0_raw_data['Time'] = pd.to_datetime(L0_raw_data['Time'], utc=tz_utc)

    # Calculate dew-point temperature in raw data:
    L0_raw_data['dT(degC)'] = dewpoint_from_relative_humidity((L0_raw_data['Temperature(degree C)'].to_numpy() * units.degC).to(units.K), L0_raw_data['Humidity(%)'].to_numpy() / 100.)

    # Convert wind speed in raw data:
    # L0_raw_data['WS(kts)'] = (L0_raw_data['Speed(km/hr)'].to_numpy() * units.kilometer_per_hour).to(units.knot)
    L0_raw_data['WS(m/s)'] = (L0_raw_data['Speed(km/hr)'].to_numpy() * units.kilometer_per_hour).to(units.meter_per_second)

    # Convert wind direction in raw data:
    L0_raw_data.loc[L0_raw_data['Direction(degree)'] <= 180, 'WDIR'] = L0_raw_data['Direction(degree)'] + 180
    L0_raw_data.loc[L0_raw_data['Direction(degree)'] > 180, 'WDIR'] = L0_raw_data['Direction(degree)'] - 180
    L0_raw_data.loc[L0_raw_data['Speed(km/hr)'] == 0, 'WDIR'] = 0

    # Find the index of launch time and convert L0 to L1 data:
    L1_data = L0_raw_data[ ( L0_raw_data['Time'] >= launch_time_utc ) & ( L0_raw_data.index <= L0_raw_data['Pressure(hPa)'].idxmin() ) ].copy()

    # Set Time(sec) in L1 data:
    L1_data['Time(sec)'] = (L1_data['Time']-launch_time_utc).dt.total_seconds()

    return L1_data

def output_L1():

    # Output L1 data (csv format):

    L1_csv_filename = output_path + '/no_{}_L1_aspen.csv'.format(ST_no)

    with open(L1_csv_filename, 'w') as file:

        # Required fields:
        file.write('FileFormat,CSV\n')
        file.write('Year,{}\n'.format(loaded_ST_file[0].year))
        file.write('Month,{:02d}\n'.format(loaded_ST_file[0].month))
        file.write('Day,{:02d}\n'.format(loaded_ST_file[0].day))
        file.write('Hour,{:02d}\n'.format(loaded_ST_file[0].hour))
        file.write('Minute,{:02d}\n'.format(loaded_ST_file[0].minute))
        file.write('Second,{:02d}\n'.format(loaded_ST_file[0].second))

        file.write('Ascending,"true"\n')

        # Optional fields:
        file.write('latitude,40.590000,"units=deg"\n')
        file.write('longitude,-105.141500,"units=deg"\n')
        # file.write('pressure,841.4,"units=hPa"\n')
        # file.write('temperature,21.6,"units=deg C"\n')
        # file.write('rh,56.9,"units=%"\n')
        file.write('altitude,1571.9,"units=m"\n')
        file.write('gpsaltitude,1571.9,"units=m"\n')
        file.write('project,"PRE-CIP-2021"\n')
        file.write('agency,"CSU"\n')
        file.write('sondeid,"{}"\n'.format(ST_no))
        file.write('sondetype,"Storm Tracker"\n')
        file.write('launchsite,"Christman Field"\n')

        # Data headers:
        file.write('Fields,Time,Pressure,Temperature,RH,Speed,Direction,Latitude,Longitude,altitude,sats,gpsalt,SNR,Voltage\n')
        file.write('Units,sec,mb,deg C,%,m/s,deg,deg,deg,m,,m,,V\n')

        # Data fields:

        for index, row in L1_data.iterrows():

            file.write('Data,%6.1f,%7.2f,%5.2f,%5.2f,%6.2f,%6.2f,%9.5f,%9.5f,,%2f,%7.1f,%3f,%5.3f\n'\
                       % (row['Time(sec)']\
                        , row['Pressure(hPa)']\
                        , row['Temperature(degree C)']\
                        , row['Humidity(%)']\
                        , row['WS(m/s)']\
                        , row['Direction(degree)']\
                        , row['Lat']\
                        , row['Lon']\
                        , row['Sat']\
                        , row['Height(m)']\
                        , row['SNR']\
                        , row['Voltage(V)']\
                         )\
                      )

# %%
# Run:

loaded_ST_file = load_st_file(ST_no, launch_time_from_log, ST_file_path)
L1_data = conversion_L0_L1(loaded_ST_file)
output_L1()
