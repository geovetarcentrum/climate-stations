# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:46:13 2021

This python module holds basic functions needed for data preprocessing of
meteorological measurements from LoggerNet (in the form of .dat files ).
The main utilities are to calculate downwelling longwave radiation from
measured body temperature, to extract and redefine column names and
to performq quality control of the measured values.

@author: Julia Kukulies, see GitHub for history
"""

import numpy as np
import pandas as pd

from pathlib import Path
from shutil import copyfile
from datetime import date, datetime, timedelta
import pytz
import warnings

# import plotting module and functions for preprocessing
from plotting import bridge_plot, roof_plot, roof_table, bridge_table


############################### Define functions ##############################


def load_logger_data(f):
    """Top-level function to load a table from a logger output file.

    f - filename
    """
    table = pd.read_table(f, sep=",", header=1, low_memory=False)
    # skip first two rows
    table = table.iloc[2::, :]
    # replace nan values with empty field
    table = table.replace("NAN", "", regex=True)
    # add a datetime.
    table["dtime"] = pd.to_datetime(table.TIMESTAMP)
    return table


def make_csv(table, pset, year, month):
    """Write out a CSV file

    Inputs:
    table - as output from load_logger_data
    station - "roof" or "bridge"
    interval - "10" or "5"
    year & month as int

    Output:
    filename Local that was written to.
    """

    output_dir = pset["csv_output_dir"]
    do_QC = pset["do_QC"]
    station = pset["station"]
    interval = pset["interval"]

    MONTH = "0" + str(month)
    if month > 9:
        MONTH = str(month)
    YEAR = str(year)

    data = table[(table.dtime.dt.year == year) & (table.dtime.dt.month == month)]

    # Call processing functions
    df_ = get_data(data, pset)

    # Saving monthly .csv file
    OUTPUT10 = (
        "gvc_" + station + "_" + interval + "mindata_" + YEAR + "_" + MONTH + ".csv"
    )
    # save locally
    source = Path(output_dir, OUTPUT10)
    df_.to_csv(
        source,
        index=False,
        float_format="%.5g",
        sep=",",
        encoding="utf-8",
        na_rep="",
        header=df_.columns,
    )

    return source


def make_plot(table, pset):
    """Create a plot for the last 4 days, copy to web directory"""
    # create plot of last 4 days and table image of last measurement
    # and send to RCG server for display on webpage
    end = datetime.today()
    # take one more hour to plot if it is summer time
    if (
        pd.Timestamp(datetime.today()).tz_localize(tz=pytz.FixedOffset(60)).hour
        == pd.Timestamp(datetime.today()).tz_localize("CET").hour
    ):
        today = datetime.today() + timedelta(hours=1)
    else:
        today = datetime.today()

    start = today - timedelta(days=4)

    # data = table[(table.dtime.dt.year == year) & (table.dtime.dt.month == month)]
    data = table[(table.dtime > start) & (table.dtime <= end)]

    # Call processing functions
    df_ = get_data(data, pset)

    df_["dtime"] = pd.to_datetime(df_.TIMESTAMP)
    df_["TIMESTAMP"] = pd.to_datetime(df_.TIMESTAMP)
    # convert time to CEST
    df_["TIMESTAMP"] = (
        df_["TIMESTAMP"]
        .dt.tz_localize(tz=pytz.FixedOffset(60))
        .dt.tz_convert("Europe/Stockholm")
    )
    # extract last four days
    # mask = (df_roof["dtime"] > start) & (df_roof["dtime"] <= end)
    # roof = df_roof.loc[mask]

    if pset["station"] == "roof":
        LOCAL_NAME = roof_plot(df_, pset["plot_output_dir"])
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "GVC_plot.png")

        LOCAL_NAME = roof_plot(df_, pset["plot_output_dir"], swedish=True)
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "GVC_plot_sv.png")

        LOCAL_NAME = roof_table(df_, pset["plot_output_dir"])
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "GVCtable_plot.png")

        LOCAL_NAME = roof_table(df_, pset["plot_output_dir"], swedish=True)
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "GVCtable_plot_sv.png")

    if pset["station"] == "bridge":
        LOCAL_NAME = bridge_plot(df_, pset["plot_output_dir"])
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "Bridge_plot.png")

        LOCAL_NAME = bridge_plot(df_, pset["plot_output_dir"], swedish=True)
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "Bridge_plot_sv.png")

        LOCAL_NAME = bridge_table(df_, pset["plot_output_dir"])
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "Bridgetable_plot.png")

        LOCAL_NAME = bridge_table(df_, pset["plot_output_dir"], swedish=True)
        copyfile(LOCAL_NAME, pset["plot_web_dir"] / "Bridgetable_plot_sv.png")


def get_radiation(data):
    """This function calculates downwelling longwave radiation
    based on measured body temperature and correction with ."""
    L_down = (
        5.670374419 * 10 ** (-8) * pd.to_numeric(data.temp_L_K_Avg.values) ** 4
    ) + pd.to_numeric(data.L_sig_Avg.values)
    return L_down


def get_data(data, pset):
    """This function extracts usable columns from logger data
    and creates a new dataframe df.

    Input:
    data - pandas dataframe with data from logger file
    oldcolumns - list/array with columns of meteodata which should be used
    newcolumns - list/array with official column names corresponding to oldcolumns

    Returns:
    df- pandas dataframe with extracted data
    """
    station = pset["station"]

    if station == "roof":
        oldcolumns = [
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

        newcolumns = [
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
    else:
        oldcolumns = [
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

        newcolumns = ["wd", "ws_min", "ws", "ws_max", "Ta", "RH", "P", "Rain", "Hail"]

    # Get columns for Code, Year, DOY, HHMM
    df = pd.DataFrame()
    df["Code"] = data.RECORD.values.astype(str)
    df["Year"] = data.dtime.dt.year.values.astype(str)
    df["DOY"] = data.dtime.dt.dayofyear.values.astype(str)
    # time formatting
    hours = data.dtime.dt.hour.values.astype(str)
    minutes = data.dtime.dt.minute.values.astype(str)
    # zero padding
    for i, h in enumerate(hours):
        if int(h) < 10:
            hours[i] = "0" + h
    for i, m in enumerate(minutes):
        if int(m) < 10:
            minutes[i] = "0" + m

    df["hours"] = hours
    df["minutes"] = minutes
    df["HHMM"] = df["hours"] + df["minutes"]
    df["TIMESTAMP"] = data.TIMESTAMP.values.astype(str)
    df = df.drop(columns=["hours", "minutes"])

    # Get columns for meteorological data

    for i, col in enumerate(oldcolumns):
        newname = newcolumns[i]
        newcol = pd.to_numeric(data[col].values)
        df[newname] = newcol

    if pset["do_QC"]:
        with warnings.catch_warnings():
            # suppress warnings for this specific function
            warnings.simplefilter("ignore")
            df = quality_control(df)

    if station == "roof":
        # calculate downwelling longwave-radiation with Stefan Boltzmann law
        L_down = get_radiation(data)
        # replace body temperature with L_down
        df["L_down"] = L_down
        # remove signal and replace with empty column for old radiation data
        df["K_down_KnZ"] = ""

    return df


def quality_control(df):
    """This function performs a quality check on the meteorological measurements and
    adds quality flags for the main meteorological variables.

    Input: pandas dataframe containing meteorological data
    Returns: pandas dataframe with the following flags:
    0 = passed all controls
    1 = not in plausible range, 2 = inconsistency
    3 = too big jumps
    4 = dead band (too small changes over time)
    """

    # relative humidity (%)
    df["RH_QC"] = 0
    # pressure (hPa)
    df["P_QC"] = 0
    # mean air temperature (degC)
    df["Ta_QC"] = 0
    # mean wind speed (m/s)
    df["ws_QC"] = 0
    # min wind speed (m/s)
    df["ws_max_QC"] = 0
    # max wind speed (m/s)
    df["ws_min_QC"] = 0
    # mean wind direction (deg)
    df["wd_QC"] = 0

    # quality checks for each value
    for i in df.index.values:
        rh = df[df.index == i].RH.values[0]
        pr = df[df.index == i].P.values[0]
        ta = float(df[df.index == i].Ta.values[0])
        wd = df[df.index == i].wd.values[0]
        ws = df[df.index == i].ws.values[0]
        ws_min = df[df.index == i].ws_min.values[0]
        ws_max = df[df.index == i].ws_max.values[0]

        # plausible ranges
        if rh < 0 or rh > 100:
            df.loc[i, "RH_QC"] = 1
        if pr < 500 or pr > 1100:
            df.loc[i, "P_QC"] = 1
        if wd < 0 or wd > 360:
            df.loc[i, "wd_QC"] = 1
        if ws < 0 or ws > 75:
            df.loc[i, "ws_QC"] = 1
        if ws_min < 0 or ws_min > 75:
            df.loc[i, "ws_min_QC"] = 1
        if ws_max < 0 or ws_max > 75:
            df.loc[i, "ws_max_QC"] = 1
        if ta < -50 or ta > 50:
            df.loc[i, "Ta_QC"] = 1

        # internal inconsistencies
        if wd == 0 and ws > 0:
            df.loc[i, "wd_QC"] = 2
        if ws == 0 and wd > 0:
            df.loc[i, "wd_QC"] = 2

        # comparison with surrounding values
        if i > 2 and i < np.shape(df.index.values)[0] - 1:
            p = i - 1  # index previous value
            rh_p = df[df.index == p].RH.values[0]
            pr_p = df[df.index == p].P.values[0]
            ta_p = float(df[df.index == p].Ta.values[0])
            wd_p = df[df.index == p].wd.values[0]
            ws_p = df[df.index == p].ws.values[0]

            n = i + 1  # index next value
            rh_n = df[df.index == n].RH.values[0]
            pr_n = df[df.index == n].P.values[0]
            ta_n = float(df[df.index == n].Ta.values[0])
            wd_n = df[df.index == n].wd.values[0]
            ws_n = df[df.index == n].ws.values[0]

            # set maximum variance to check time consistency (detect big jumps in data)

            # define limits
            lim_T = 3  # Cdeg
            lim_RH = 15  # %
            lim_P = 2  # hpa
            lim_ws = 20  # m/s
            lim_irr = 800  # W/m^2

            if np.absolute(ta - ta_p) >= lim_T:
                df.loc[i, "Ta_QC"] = 3
            if np.absolute(rh - rh_p) >= lim_RH:
                df.loc[i, "RH_QC"] = 3
            if np.absolute(pr - pr_p) >= lim_P:
                df.loc[i, "P_QC"] = 3
            if np.absolute(ws - ws_p) >= lim_ws:
                df.loc[i, "ws_QC"] = 3

            # check instantanous values (ts) with standard deviation for each variable
            ts = np.absolute(wd - wd_p) + np.absolute(wd - wd_n)
            # get std of last 12 hours
            std_wd = np.nanstd(df.loc[i - 1 : i - 6 * 12, "wd"].values)
            if ts > 4 * std_wd:
                df.loc[i, "wd_QC"] = 3

            ts = np.absolute(ws - ws_p) + np.absolute(ws - ws_n)
            std_ws = np.nanstd(df.loc[i - 1 : i - 6 * 12, "ws"].values)
            if ts > 4 * std_ws:
                df.loc[i, "ws_QC"] = 3

            ts = np.absolute(pr - pr_p) + np.absolute(pr - pr_n)
            std_pr = np.nanstd(df.loc[i - 1 : i - 6 * 12, "P"].values)
            if ts > 4 * std_pr:
                df.loc[i, "P_QC"] = 3

            ts = np.absolute(rh - rh_p) + np.absolute(rh - rh_n)
            std_rh = np.nanstd(df.loc[i - 1 : i - 6 * 12, "RH"].values)
            if ts > 4 * std_rh:
                df.loc[i, "RH_QC"] = 3

            ts = np.absolute(ta - ta_p) + np.absolute(ta - ta_n)
            std_ta = np.nanstd(df.loc[i - 1 : i - 6 * 12, "Ta"].values)
            if ts > 4 * std_ta:
                df.loc[i, "Ta_QC"] = 3

            # persistence test (minimum required variability of instaneous value during two hours)
            avg_wd = np.nanmean(df.loc[i - 1 : i - 12, "wd"].values)
            if np.absolute(wd - avg_wd) < 10:
                df.loc[i, "wd_QC"] = 4

            avg_ws = np.nanmean(df.loc[i - 1 : i - 12, "ws"].values)
            if np.absolute(ws - avg_ws) < 0.1:
                df.loc[i, "ws_QC"] = 4

            avg_pr = np.nanmean(df.loc[i - 1 : i - 12, "P"].values)
            if np.absolute(pr - avg_pr) < 0.1:
                df.loc[i, "P_QC"] = 4

            avg_rh = np.nanmean(df.loc[i - 1 : i - 12, "RH"].values)
            if np.absolute(rh - avg_rh) < 0.1:
                df.loc[i, "RH_QC"] = 4

            avg_ta = np.nanmean(df.loc[i - 1 : i - 12, "Ta"].values)
            if np.absolute(ta - avg_ta) < 0.1:
                df.loc[i, "Ta_QC"] = 4

            # minimum standard deviation of last 12 hours to detect blocking of sensor ("dead band")
            if std_ta < 0.1:
                df.loc[i - 1 : i - 6 * 12, "Ta_QC"] = 4

            if std_pr < 0.1:
                df.loc[i - 1 : i - 6 * 12, "P_QC"] = 4

            if std_ws < 0.5:
                df.loc[i - 1 : i - 6 * 12, "ws_QC"] = 4

            if std_wd < 10:
                df.loc[i - 1 : i - 6 * 12, "wd_QC"] = 4

            if std_rh < 1:
                df.loc[i - 1 : i - 6 * 12, "RH_QC"] = 4

    return df
