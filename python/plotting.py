"""

This python script contains two plotting functions to create subplots for
meteorological measurements from GVC roof and Bridge data


"""


import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
import warnings
warnings.filterwarnings("ignore") 

def bridge_plot(df, output_dir, swedish=False):
    """This function plots GVC roof date the four last days at 5 min resolution.

    Parameter:

    df: pandas dataframe object with meteoroloical measurements of the last four days.

    swedish(bool): set to True for swedish axis labels, standard is english

    Returns:
    LOCAL_NAME - name the file is written to.

    """
    plt.figure(figsize=(20, 30))

    # language for labelling
    if swedish is True:
        ylabels = [
            "[hPa]",
            "[$^\circ$C]",
            "[%]",
            "[m/s]",
            "[$^\circ$] true",
            "[mm/timme]",
            "[traeff/cm$^2$/timme]",
        ]
        labels = [
            "Lufttryck",
            "Lufttemperatur",
            "Relativ fuktighet",
            "Vindhastighet",
            "Vindriktning",
            "Regn",
            "Hagel",
        ]
    else:
        labels = [
            "Air pressure",
            "Air temperature",
            "Relative humidity",
            "Wind speed",
            "Wind direction",
            "Rain",
            "Hail",
        ]
        ylabels = [
            "[hPa]",
            "[$^\circ$C]",
            "[%]",
            "[m/s]",
            "[$^\circ$] true",
            "[mm/hour]",
            "[hits/cm$^2$/hour]",
        ]

    
    columns= ['P', 'Ta' , 'RH', 'ws', 'wd', 'Rain']

    #### colors and label/font sizes ####
    # fontsize
    size = 36
    labelsize= 24
    # linewidth
    linewidth = 3.0
    # label pad
    labelpad = 40
    colors = ['black', 'darkred','coral', 'deeppink', 'violet', 'dodgerblue', 'indigo']

    # get dates in nicer format
    years = df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].TIMESTAMP.dt.year.values
    months = df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].TIMESTAMP.dt.month.values
    days = df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].TIMESTAMP.dt.day.values
    dates = []
    for idx in range(days.size):
        date = str(years[idx]) +'-'+ str(months[idx])  +'-'+ str( days[idx])
        dates.append(date)

    #### subplot ####
    for subplt in np.arange(6):
        subplot_nr = subplt+ 1
        colname = columns[subplt]
        fig = plt.subplot(6, 1, subplot_nr)
        ax1 = df[colname].plot(color= colors[subplt], linewidth=linewidth, grid=True)

        # labels 
        ax1.set_title(labels[subplt], fontsize=size * 1.5)
        ax1.set_ylabel(ylabels[subplt], fontsize=size, labelpad=labelpad)

        # x tick formatting
        df_hour = df[df.TIMESTAMP.dt.minute == 0]
        mask = df_hour[(df.TIMESTAMP.dt.hour == 0) |(df.TIMESTAMP.dt.hour == 4) | (df.TIMESTAMP.dt.hour == 8) | (df.TIMESTAMP.dt.hour == 12) | (df.TIMESTAMP.dt.hour == 16)| (df.TIMESTAMP.dt.hour == 20)]
        xticks = mask.index.values
        xticklabels = mask.TIMESTAMP.dt.hour.values.astype(int)
        ax1.set_xlim(df.index.values.min(), df.index.values.max())
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticklabels, fontsize = labelsize )
        ax = ax1.twiny()
        ax.set_xlim(df.index.values.min(), df.index.values.max())
        ax.set_xticks(df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].index.values)
        ax.set_xticklabels(dates, rotation = 90, ha = 'center', fontsize= labelsize)   
        ax.tick_params(axis="x",direction="in", pad = -150)
        ax.xaxis.set_ticks_position('bottom')

        # ytick formatting 
        yticks = ax1.get_yticks()
        if colname =='Rain':
            ax1.set_yticklabels(np.round(yticks, decimals = 4), fontsize = labelsize)
        else:
            ax1.set_yticklabels(yticks.astype(int), fontsize= labelsize)
        ax1.get_yaxis().set_label_coords(-0.07, 0.5)

    plt.tight_layout()

    # send to RCG server for plotting on WEB
    name = "Bridge_plot"
    if swedish is True:
        name = "Bridge_plot_sv"

    # save locally
    f = name + str(datetime.date.today()) + ".png"
    LOCAL_NAME = output_dir / f
    plt.savefig(LOCAL_NAME, facecolor=fig.get_facecolor(), transparent=True)

    return LOCAL_NAME


def roof_plot(df, output_dir, swedish=False):
    """This function plots GVC roof date of the four last days at 10 min resolution.

    Parameter:

    swedish(bool): set to True for swedish axis labels, standard is english

    """

    # language for labelling
    if swedish is True:
        ylabels = [
            "[hPa]",
            "[$^\circ$C]",
            "[%]",
            "[m/s]",
            "[$^\circ$] true",
            "[mm/timme]",
            "[traeff/cm$^2$/timme]",
            "[W/m$^2$]",
            "[W/m$^2$]",
        ]
        labels = [
            "Lufttryck",
            "Lufttemperatur",
            "Relativ fuktighet",
            "Vindhastighet",
            "Vindriktning",
            "Regn",
            "Hagel",
            "Inkommande långvågig strålning",
            "Inkommande kortvågig strålning",
        ]
    else:
        ylabels = [
            "[hPa]",
            "[$^\circ$C]",
            "[%]",
            "[m/s]",
            "[$^\circ$] true",
            "[mm/hour]",
            "[hits/cm$^2$/hour]",
            "[W/m$^2$]",
            "[W/m$^2$]",
        ]
        labels = [
            "Air pressure",
            "Air temperature",
            "Relative humidity",
            "Wind speed",
            "Wind direction",
            "Rain",
            "Hail",
            "Incoming longwave radiation",
            "Incoming shortwave radiation",
        ]

    plt.figure(figsize=(20, 35))
    columns= ['P', 'Ta' , 'RH', 'ws', 'wd', 'Rain', 'Hail', 'L_down', 'K_down_SPN1']

    #### colors and label/font sizes ####
    # fontsize
    size = 30
    labelsize= 24
    # linewidth
    linewidth = 3.0
    # label pad
    labelpad = 40
    colors = ['black', 'darkred', 'coral', 'deeppink', 'violet', 'dodgerblue','indigo', 'lightseagreen', 'darkslategrey']

    # get dates in nicer format
    years = df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].TIMESTAMP.dt.year.values
    months = df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].TIMESTAMP.dt.month.values
    days = df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].TIMESTAMP.dt.day.values
    dates = []
    for idx in range(days.size):
        date = str(years[idx]) +'-'+ str(months[idx])  +'-'+ str( days[idx])
        dates.append(date)

    #### subplot ####
    for subplt in np.arange(9):
        subplot_nr = subplt+ 1
        colname = columns[subplt]
        fig = plt.subplot(9, 1, subplot_nr)

        if colname == 'K_down_SPN1':
            fig = plt.subplot(9, 1, 9)
            ax1 = df.K_down_SPN1.plot(color=colors[subplt], linewidth=linewidth, label="global", grid=True)
            ax1 = df.K_diff_SPN1.plot(
                color=colors[subplt+ 1 ], linewidth=linewidth, label="diffus", grid=True
            )
            legend = ax1.legend(fontsize=size, edgecolor="black")
            legend.get_frame().set_alpha(None)
            legend.get_frame().set_facecolor((0, 0, 1, 0.1))
        else:
             ax1 = df[colname].plot(color= colors[subplt], linewidth=linewidth, grid=True)

        # labels 
        ax1.set_title(labels[subplt], fontsize=size * 1.5)
        ax1.set_ylabel(ylabels[subplt], fontsize=size, labelpad=labelpad)

        # x tick formatting
        df_hour = df[df.TIMESTAMP.dt.minute == 0]
        mask = df_hour[(df.TIMESTAMP.dt.hour == 0) |(df.TIMESTAMP.dt.hour == 4) | (df.TIMESTAMP.dt.hour == 8) | (df.TIMESTAMP.dt.hour == 12) | (df.TIMESTAMP.dt.hour == 16)| (df.TIMESTAMP.dt.hour == 20)]
        xticks = mask.index.values
        xticklabels = mask.TIMESTAMP.dt.hour.values.astype(int)
        ax1.set_xlim(df.index.values.min(), df.index.values.max())
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticklabels, fontsize = labelsize )
        ax = ax1.twiny()
        ax.set_xlim(df.index.values.min(), df.index.values.max())
        ax.set_xticks(df[(df.TIMESTAMP.dt.hour == 0) & (df.TIMESTAMP.dt.minute == 0  )].index.values)
        ax.set_xticklabels(dates, rotation = 90, ha = 'center', fontsize= labelsize)   
        ax.tick_params(axis="x",direction="in", pad = -150)
        ax.xaxis.set_ticks_position('bottom')

        # ytick formatting 
        yticks = ax1.get_yticks()
        if colname =='Rain' or colname == 'Hail':
            ax1.set_yticklabels(np.round(yticks, decimals = 4), fontsize = labelsize)
        else:
            ax1.set_yticklabels(yticks.astype(int), fontsize= labelsize)
        ax1.get_yaxis().set_label_coords(-0.07, 0.5)

    plt.tight_layout()

    # send to RCG server for plotting on WEB
    name = "GVC_plot"
    if swedish is True:
        name = "GVC_plot_sv"

    # save locally
    f = name + str(datetime.date.today()) + ".png"
    LOCAL_NAME = output_dir / f
    plt.savefig(LOCAL_NAME, transparent=True, bbox_inches="tight")

    return LOCAL_NAME


def roof_table(df, output_dir, swedish=False):
    """This function creates an image showing a table with the latest measurement for meteorological data from the bridge.

    Parameter:

    df: dataframe containing data of the latest four days
    swedish(bool): optional choice for labels, True for swedish, standard is English

    """

    # extract latest measurement
    subset = df.iloc[-1, :]
    time = subset.TIMESTAMP

    # language for labelling
    if swedish is True:
        name = "GVCtable_plot_sv"
        labels = [
            "Tid",
            "Lufttryck",
            "Lufttemperatur",
            "Relativ fuktighet",
            "Vindhastighet",
            "Vindriktning",
            "Regn",
            "Hagel",
            "Inkommande LV strålning",
            "Inkommande KV strålning global",
            "Inkommande KV strålning diffus",
        ]
        ylabels = [
            "CEST",
            "hPa",
            "gradC",
            "%",
            "m/s",
            "grad",
            "mm/timme",
            "traeff/cm$^2$/timme",
            "W/m$^2$",
            "W/m$^2$",
            "W/m$^2$",
        ]

    else:
        name = "GVCtable_plot"
        labels = [
            "Time",
            "Air pressure",
            "Air temperature",
            "Relative humidity",
            "Wind speed",
            "Wind direction",
            "Rain",
            "Hail",
            "Incoming LW radiation",
            "Incoming SW radiation global",
            "Incoming SW radiation diffuse",
        ]
        ylabels = [
            "CEST",
            "hpa",
            "degC",
            "%",
            "m/s",
            "deg",
            "mm/hour",
            "hits/cm$^2$/hour",
            "W/m$^2$",
            "W/m$^2$",
            "W/m$^2$",
        ]

    # fill table with values
    values = [
        time,
        subset.P,
        np.round(subset.Ta, decimals=2),
        subset.RH,
        subset.ws,
        subset.wd,
        subset.Rain,
        subset.Hail,
        np.round(subset.L_down, decimals=2),
        subset.K_down_SPN1,
        subset.K_diff_SPN1,
    ]
    df2 = pd.DataFrame(columns=["variable", "value", "units"])
    df2["value"] = values
    df2["variable"] = labels
    df2["units"] = ylabels

    # save pandas dataframe as image (locally)
    f = name + str(datetime.date.today()) + ".png"
    LOCAL_NAME = output_dir / f
    df = df2

    # alternative table formatting: 
    #df_changed = df.style.set_properties(**{            'background-color': None , 'font-size': '120pt',})
    #import dataframe_image as dfi
    #dfi.export(df_changed,"table.png" )

    # HTML file of table 
    #html = df.to_html()
    #text_file = open("table.html", "w")
    #text_file.write(html)
    #text_file.close()

    fig, ax = plt.subplots(figsize=(36, 12))
    ax.axis("off")
    ta = table(ax, df, loc="center", zorder=5.0)
     # Setting the font size
    ta.auto_set_font_size(False)
    ta.set_fontsize(45) 
    # Rescaling the rows to be more readable
    ta.scale(1, 4)
    plt.tight_layout()
    plt.savefig(LOCAL_NAME, transparent=True, bbox_inches="tight")
    return LOCAL_NAME


def bridge_table(df, output_dir, swedish=False):
    """This function creates an image showing a table with the latest measurement for meteorological data from the bridge.

    Parameter:

    df: dataframe containing data of the latest four days
    output_dir - Path to output file to, no name component.
    swedish: optional choice for language of labels, True for swedish, standard is English

    """

    # extract latest measurement
    subset = df.iloc[-1, :]
    time = subset.TIMESTAMP

    # language for labelling
    if swedish is True:
        name = "Bridgetable_plot_sv"
        ylabels = [
            "CEST",
            "hPa",
            "degC",
            "%",
            "m/s",
            "grad",
            "mm/5min",
            "traeff/cm$^2$/5min",
        ]
        labels = [
            "Tid",
            "Lufttryck",
            "Lufttemperatur",
            "Relativ fuktighet",
            "Vindhastighet",
            "Vindriktning",
            "Regn",
            "Hagel",
        ]
    else:
        labels = [
            "Time",
            "Air pressure",
            "Air temperature",
            "Relative humidity",
            "Wind speed",
            "Wind direction",
            "Rain",
            "Hail",
        ]
        name = "Bridgetable_plot"
        ylabels = [
            "CEST",
            "hPa",
            "degC",
            "%",
            "m/s",
            "deg",
            "mm/5min",
            "hits/cm$^2$/5min",
        ]

    # fill table with values
    values = [
        time,
        subset.P,
        subset.Ta,
        subset.RH,
        subset.ws,
        subset.wd,
        subset.Rain,
        subset.Hail,
    ]
    df2 = pd.DataFrame(columns=["variable", "value", "units"])
    df2["variable"] = labels
    df2["units"] = ylabels
    df2["value"] = values

    # save pandas dataframe as image (locally)
    f = name + str(datetime.date.today()) + ".png"
    LOCAL_NAME = output_dir / f
    df = df2

    fig, ax = plt.subplots(figsize=(32, 12))
    ax.axis("off")
    ta = table(ax, df, loc="center", zorder=5.0)
     # Setting the font size
    ta.auto_set_font_size(False)
    ta.set_fontsize(44) 
    # Rescaling the rows to be more readable
    ta.scale(1, 4)
    plt.tight_layout()

    plt.savefig(LOCAL_NAME)

    return LOCAL_NAME
