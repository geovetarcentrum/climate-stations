# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:46:13 2021

This python module holds basic functions needed for data preprocessing of meteorological measurements
from LoggerNet (in the form of .dat files ). The main utilities are to calculate downwelling longwave radiation from 
measured body temperature, to extract and redefine column names and to performq quality control of the measured values. 

@author: Julia Kukulies 
"""


import pandas as pd
import numpy as np
from datetime import date, timedelta

############################### Define functions ##########################################################

def get_radiation(data):
    """ This function calculates downwelling longwave radiation based on measured body temperature and correction with ."""
    L_down = (5.670374419 * 10**(-8) * pd.to_numeric(data.temp_L_K_Avg.values)**4 ) + pd.to_numeric(data.L_sig_Avg.values)
    return L_down

def get_data(data, oldcolumns, newcolumns):
    """ This function extracts usable columns from logger data and creates a new dataframe df.

    Input:
    data - pandas dataframe with data from logger file
    oldcolumns - list/array with columns of meteodata which should be used
    newcolumns - list/array with official column names corresponding to oldcolumns

    Returns:
    df- pandas dataframe with extracted data 
    """
    
    # Get columns for Code, Year, DOY, HHMM
    df= pd.DataFrame()
    df['Code'] = data.RECORD.values.astype(str)
    df['Year'] = data.dtime.dt.year.values.astype(str)
    df['DOY'] = data.dtime.dt.dayofyear.values.astype(str)
    # time formatting
    hours = data.dtime.dt.hour.values.astype(str)
    minutes = data.dtime.dt.minute.values.astype(str)
    # zero padding
    for i, h in enumerate(hours):
        if int(h) < 10:
            hours[i] = '0' + h
    for i, m in enumerate(minutes):
        if int(m) < 10:
            minutes[i] = '0' + m
            
    df['hours'] = hours
    df['minutes'] = minutes
    df['HHMM'] = df['hours'] + df['minutes']
    df['TIMESTAMP'] = data.TIMESTAMP.values.astype(str)
    df = df.drop(columns = ['hours', 'minutes'])




    # Get columns for meteorological data
 
    for i, col in enumerate(oldcolumns):
        newname = newcolumns[i]
        newcol = pd.to_numeric(data[col].values)
        df[newname] = newcol
    return df



def quality_control(df):
    """ This function performs a quality check on the meteorological measurements and adds quality flags for the main meteorological variables.

    Input: pandas dataframe containing meteorological data
    Returns: pandas dataframe with the following flags:
    0 = passed all controls
    1 = not in plausible range, 2 = inconsistency
    3 = too big jumps
    4 = dead band (too small changes over time)
    """

    # relative humidity (%)
    df['RH_QC'] = 0
    # pressure (hPa)
    df['P_QC'] = 0
    # mean air temperature (degC)
    df['Ta_QC']  = 0
    # mean wind speed (m/s)
    df['ws_QC']  = 0
    # min wind speed (m/s)
    df['ws_max_QC']  = 0
    # max wind speed (m/s)
    df['ws_min_QC']  = 0
    # mean wind direction (deg)
    df['wd_QC']  = 0
  

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
             df.loc[i, 'RH_QC'] = 1
        if  pr < 500 or pr > 1100:
            df.loc[i, 'P_QC'] = 1
        if wd < 0 or wd > 360:
            df.loc[i, 'wd_QC'] = 1
        if ws < 0 or ws > 75:
            df.loc[i, 'ws_QC'] = 1
        if ws_min < 0 or ws_min > 75:
            df.loc[i, 'ws_min_QC'] = 1
        if ws_max < 0 or ws_max > 75:
            df.loc[i, 'ws_max_QC'] = 1
        if ta < -50 or ta > 50:
            df.loc[i, 'Ta_QC'] = 1


        # internal inconsistencies
        if wd == 0 and ws > 0:
            df.loc[i, 'wd_QC'] = 2
        if ws == 0 and wd > 0:
            df.loc[i, 'wd_QC'] = 2

        # comparison with surrounding values
        if i > 2 and i < np.shape(df.index.values)[0] -1 :
            p = i - 1 # index previous value
            rh_p = df[df.index == p ].RH.values[0]
            pr_p = df[df.index == p ].P.values[0]
            ta_p = float(df[df.index == p].Ta.values[0]) 
            wd_p = df[df.index == p].wd.values[0]
            ws_p = df[df.index == p].ws.values[0]

            n= i+1 # index next value
            rh_n = df[df.index == n].RH.values[0]
            pr_n = df[df.index == n].P.values[0]
            ta_n = float(df[df.index == n].Ta.values[0]) 
            wd_n = df[df.index == n].wd.values[0]
            ws_n = df[df.index == n].ws.values[0]

            # set maximum variance to check time consistency (detect big jumps in data)

            # define limits
            lim_T = 3 # Cdeg
            lim_RH = 15 # %
            lim_P = 2 # hpa
            lim_ws = 20 # m/s
            lim_irr= 800 # W/m^2

            if np.absolute(ta - ta_p) >= lim_T:
                df.loc[i, 'Ta_QC'] =  3
            if np.absolute(rh - rh_p) >= lim_RH:
                df.loc[i, 'RH_QC'] = 3
            if np.absolute(pr - pr_p) >= lim_P:
                df.loc[i, 'P_QC'] = 3
            if np.absolute(ws - ws_p) >= lim_ws:
                df.loc[i, 'ws_QC'] = 3

            # check instantanous values (ts) with standard deviation for each variable 
            ts= np.absolute(wd - wd_p) + np.absolute(wd - wd_n)
            # get std of last 12 hours 
            std_wd = np.nanstd(df.loc[i-1:i-6*12, 'wd'].values) 
            if  ts > 4 * std_wd :
                df.loc[i, 'wd_QC'] = 3

            ts= np.absolute(ws - ws_p) + np.absolute(ws - ws_n)
            std_ws = np.nanstd(df.loc[i-1:i-6*12, 'ws'].values)
            if  ts > 4 * std_ws :
                df.loc[i, 'ws_QC'] = 3

            ts= np.absolute(pr - pr_p) + np.absolute(pr - pr_n) 
            std_pr = np.nanstd(df.loc[i-1:i-6*12, 'P'].values)
            if  ts > 4 * std_pr :
                df.loc[i, 'P_QC'] = 3

            ts= np.absolute(rh - rh_p) + np.absolute(rh - rh_n) 
            std_rh = np.nanstd(df.loc[i-1:i-6*12, 'RH'].values)
            if  ts > 4 * std_rh :
                df.loc[i, 'RH_QC'] = 3

            ts= np.absolute(ta - ta_p) + np.absolute(ta - ta_n)
            std_ta = np.nanstd(df.loc[i-1:i-6*12, 'Ta'].values)
            if  ts > 4 * std_ta :
                df.loc[i, 'Ta_QC'] = 3


            # persistence test (minimum required variability of instaneous value during two hours)
            avg_wd = np.nanmean(df.loc[i-1:i-12, 'wd'].values)
            if np.absolute(wd - avg_wd) < 10:
                df.loc[i, 'wd_QC']= 4

            avg_ws = np.nanmean(df.loc[i-1:i-12, 'ws'].values)
            if np.absolute(ws - avg_ws) < 0.1:
                df.loc[i, 'ws_QC']= 4

            avg_pr = np.nanmean(df.loc[i-1:i-12, 'P'].values)
            if np.absolute(pr - avg_pr) < 0.1:
                df.loc[i, 'P_QC']= 4

            avg_rh = np.nanmean(df.loc[i-1:i-12, 'RH'].values)
            if np.absolute(rh - avg_rh) < 0.1:
                df.loc[i, 'RH_QC']= 4

            avg_ta = np.nanmean(df.loc[i-1:i-12, 'Ta'].values)
            if np.absolute(ta - avg_ta) < 0.1:
                df.loc[i, 'Ta_QC']= 4

            # minimum standard deviation of last 12 hours to detect blocking of sensor ("dead band")
            if std_ta < 0.1:
                df.loc[i-1:i-6*12, 'Ta_QC'] = 4

            if std_pr < 0.1:
                df.loc[i-1:i-6*12, 'P_QC'] = 4

            if std_ws < 0.5:
                df.loc[i-1:i-6*12, 'ws_QC'] = 4

            if std_wd < 10:
                df.loc[i-1:i-6*12, 'wd_QC'] = 4

            if std_rh < 1:
                df.loc[i-1:i-6*12, 'RH_QC'] = 4

    return df
