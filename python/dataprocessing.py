"""
This script processes meteorological data from GVC logger files
(both roof and bridge) performs a quality check and produces
monthly .csv files that can be downloaded from web.

Contact: juliakukulies@gu.se
"""


###############################################################################

# import libraries
from pathlib import Path
from shutil import copyfile
from datetime import date, datetime, timedelta
import pandas as pd

# import plotting module and functions for preprocessing
from plotting import bridge_plot, roof_plot, roof_table, bridge_table
from utils import get_radiation, get_data, quality_control

# target directory for web files
web_files = Path("//130.241.159.111/UCG/WebFiles")


###############################################################################

# Get current year, month and dates of today and tomorrow
month = int(date.today().month)

MONTH = "0" + str(month)
if month > 9:
    MONTH = str(month)

year = int(date.today().year)
tomorrow = date.today() + timedelta(days=1)

##################### Roof data ###############################################


oldcolumns_roof = [
    "Wd_avg_Avg",
    "Ws_min_Avg",
    "Ws_avg_Avg",
    "Ws_max_Avg",
    "Ta_Avg",
    "RH_Avg",
    "P_Avg",
    "Ri_intens_Avg",
    "Hd_intens_Avg",
    "SPN1_Total_Avg",
    "SPN1_diff_Avg",
    "temp_L_K_Avg",
    "L_sig_Avg",
]


newcolumns_roof = [
    "wd",
    "ws_min",
    "ws",
    "ws_max",
    "Ta",
    "RH",
    "P",
    "Rain",
    "Hail",
    "K_down_SPN1",
    "K_diff_SPN1",
    "L_down",
    "K_down_Knz",
]


############## process  .dat files for 10 minutes #############################


f = Path("C:/DATA/Taket/Roof_meteo_10min.dat")
# backup copy
copyfile(f, Path("//store-lyk-2.it.gu.se/Nf/GVC/Klimatst/Nya/Roof_meteo_10min.dat"))

table = pd.read_table(f, sep=",", header=1, low_memory=False)
# skip first two rows
table = table.iloc[2::, :]
# replace nan values with empty field
table = table.replace("NAN", "", regex=True)

# Extract only data for corresponding month and year
# to reduce size of dataframe for each update
table["dtime"] = pd.to_datetime(table.TIMESTAMP)
data = table[(table.dtime.dt.year == year) & (table.dtime.dt.month == month)]


# Call processing functions
df_roof = get_data(data, oldcolumns_roof, newcolumns_roof)
df_roof = quality_control(df_roof)

# calculate downwelling longwave-radiation with Stefan Boltzmann law
L_down = get_radiation(data)
# replace body temperature with L_down
df_roof["L_down"] = L_down
# remove signal and replace with empty column for old radiation data
df_roof["K_down_KnZ"] = ""

# Saving monthly .csv file
OUTPUT10 = "gvc_roof_10mindata_" + str(year) + "_" + MONTH + ".csv"
# save locally
df_roof.to_csv(
    Path("C:/DATA/Files/", OUTPUT10),
    index=False,
    sep=",",
    encoding="utf-8",
    na_rep="",
    header=df_roof.columns,
)


# send to .csv file to RCG server via shared drive
target = web_files / "GVCdata" / OUTPUT10
copyfile(Path("C:/DATA/Files/", OUTPUT10), target)


########### process  .dat files for 5 minutes ##############
f = Path("C:/DATA/Taket/Roof_meteo_5min.dat")
# backup copy
copyfile(f, Path("//store-lyk-2.it.gu.se/Nf/GVC/Klimatst/Nya/Roof_meteo_5min.dat"))

table = pd.read_table(f, sep=",", header=1, low_memory=False)
# skip first two rows
table = table.iloc[2::, :]
# replace nan values with empty field
table = table.replace("NAN", "", regex=True)

# Extract only data for corresponding month and year to reduce size of dataframe for each update
table["dtime"] = pd.to_datetime(table.TIMESTAMP)
data = table[(table.dtime.dt.year == year) & (table.dtime.dt.month == month)]

# Call processing functions
df_roof = get_data(data, oldcolumns_roof, newcolumns_roof)
df_roof = quality_control(df_roof)

# calculate downwelling longwave-radiation with Stefan Boltzmann law
L_down = get_radiation(data)
# replace body temperature with L_down
df_roof["L_down"] = L_down
# remove signal and replace with empty column for old radiation data
df_roof["K_down_KnZ"] = ""

# Saving monthly .csv file
OUTPUT5 = "gvc_roof_5mindata_" + str(year) + "_" + MONTH + ".csv"
# save locally
df_roof.to_csv(
    "C:/DATA/Files/" + OUTPUT5,
    index=False,
    sep=",",
    encoding="utf-8",
    na_rep="",
    header=df_roof.columns,
)


# send to .csv file to RCG server via shared drive
target = web_files / "GVCdata" / OUTPUT5
copyfile(Path("C:/DATA/Files/", OUTPUT5), target)


#############################plotting #########################################


# create plot of last 4 days and table image of last measurement
# and send to RCG server for display on webpage
end = datetime.today()
start = datetime.today() - timedelta(days=4)

df_roof["dtime"] = pd.to_datetime(df_roof.TIMESTAMP)
df_roof["TIMESTAMP"] = pd.to_datetime(df_roof.TIMESTAMP)
# convert time to CEST
df_roof["TIMESTAMP"] = (
    df_roof["TIMESTAMP"].dt.tz_localize("CET").dt.tz_convert("Europe/Stockholm")
)
# extract last four days
mask = (df_roof["dtime"] > start) & (df_roof["dtime"] <= end)
roof = df_roof.loc[mask]


LOCAL_NAME = roof_plot(roof)
copyfile(LOCAL_NAME, web_files / "GVC_plot.png")

LOCAL_NAME = roof_plot(roof, swedish=True)
copyfile(LOCAL_NAME, web_files / "GVC_plot_sv.png")

LOCAL_NAME = roof_table(roof)
copyfile(LOCAL_NAME, web_files / "GVCtable_plot.png")

LOCAL_NAME = roof_table(roof, swedish=True)
copyfile(LOCAL_NAME, web_files / "GVCtable_plot_sv.png")

################### Bridge data################################################

oldcolumns_bridge = [
    "Wd_avg_Avg",
    "Ws_min_Avg",
    "Ws_avg_Avg",
    "Ws_max_Avg",
    "Ta_Avg",
    "RH_Avg",
    "P_Avg",
    "Ri_intens_Avg",
    "Hd_intens_Avg",
]
newcolumns_bridge = ["wd", "ws_min", "ws", "ws_max", "Ta", "RH", "P", "Rain", "Hail"]


############################# process .dat files for 10 minutes################
f = Path("C:/DATA/Bron/Bridge_meteo_10min.dat")
# backup copy
copyfile(f, Path("//store-lyk-2.it.gu.se/Nf/GVC/Klimatst/Nya/Bridge_meteo_10min.dat"))


table = pd.read_table(f, sep=",", header=1, low_memory=False)
# skip first two rows
table = table.iloc[2::, :]
# replace nan values with empty field
table = table.replace("NAN", "", regex=True)


# Extract only data for corresponding month and year to reduce size of dataframe for each update
table["dtime"] = pd.to_datetime(table.TIMESTAMP)
data = table[(table.dtime.dt.year == year) & (table.dtime.dt.month == month)]

# Call processing functions
df_bridge = get_data(data, oldcolumns_bridge, newcolumns_bridge)
df_bridge = quality_control(df_bridge)


## Saving monthly .csv file

OUTPUT10 = "gvc_bridge_10mindata_" + str(year) + "_" + MONTH + ".csv"
# save locally
df_bridge.to_csv(
    Path("C:/DATA/Files/", OUTPUT10),
    index=False,
    sep=",",
    encoding="utf-8",
    na_rep="",
    header=df_bridge.columns,
)

# send to RCG server via share drive
target = web_files / "Bridgedata" / OUTPUT10
copyfile(Path("C:/DATA/Files/", OUTPUT10), target)


####################### process .dat files for 5 minutes#######################

f = Path("C:/DATA/Bron/Bridge_meteo_5min.dat")
# backup copy
copyfile(f, Path("//store-lyk-2.it.gu.se/Nf/GVC/Klimatst/Nya/Bridge_meteo_5min.dat"))


table = pd.read_table(f, sep=",", header=1, low_memory=False)
# skip first two rows
table = table.iloc[2::, :]
# replace nan values with empty field
table = table.replace("NAN", "", regex=True)


# Extract only data for corresponding month and year
table["dtime"] = pd.to_datetime(table.TIMESTAMP)
data = table[(table.dtime.dt.year == year) & (table.dtime.dt.month == month)]

# Call processing functions
df_bridge = get_data(data, oldcolumns_bridge, newcolumns_bridge)
df_bridge = quality_control(df_bridge)


## Saving monthly .csv file
OUTPUT5 = "gvc_bridge_5mindata_" + str(year) + "_" + MONTH + ".csv"
# save locally
df_bridge.to_csv(
    Path("C:/DATA/Files/", OUTPUT5),
    index=False,
    sep=",",
    encoding="utf-8",
    na_rep="",
    header=df_bridge.columns,
)

# send to RCG server via share drive
target = web_files / "Bridgedata" / OUTPUT5
copyfile(Path("C:/DATA/Files/", OUTPUT5), target)


########################## plotting ###########################################

# create plot and table image and send to RCG server to display on webpage
df_bridge["dtime"] = pd.to_datetime(df_bridge.TIMESTAMP)
df_bridge["TIMESTAMP"] = pd.to_datetime(df_bridge.TIMESTAMP)
# convert time to CEST
df_bridge["TIMESTAMP"] = (
    df_bridge["TIMESTAMP"].dt.tz_localize("CET").dt.tz_convert("Europe/Stockholm")
)

mask = (df_bridge["dtime"] > start) & (df_bridge["dtime"] <= end)
bridge = df_bridge.loc[mask]


LOCAL_NAME = bridge_plot(bridge)
copyfile(LOCAL_NAME, web_files / "Bridge_plot.png")

LOCAL_NAME = bridge_plot(bridge, swedish=True)
copyfile(LOCAL_NAME, web_files / "Bridge_plot_sv.png")

LOCAL_NAME = bridge_table(bridge)
copyfile(LOCAL_NAME, web_files / "Bridgetable_plot.png")

LOCAL_NAME = bridge_table(bridge, swedish=True)
copyfile(LOCAL_NAME, web_files / "Bridgetable_plot_sv.png")
