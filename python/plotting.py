## This python script contains two plotting functions to create subplots for meteorological measurements from GVC roof and Bridge data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import ftplib
import datetime 


def bridge_plot(df, swedish = False):
    '''This function plots GVC roof date the four last days at 5 min resolution.

    Parameter:

    swedish(bool): set to True for swedish axis labels, standard is english
    
    Returns:
    local_name - name the file is written to.

    '''
    plt.figure(figsize= (20,45))


    # fontsize
    s= 36
    #linewidth
    lw = 3.0
    #label pad
    lp = 40

    # x tick formatting
    xticks = df.index.values[::6*8]
    xticklabels = df.dtime.dt.hour.values[::6*8]

    # language for labelling
    if swedish is True:
        ylabels = ['[hPa]', '[$^\circ$C]', '[%]', '[m/s]', '[$^\circ$] true', '[mm/timme]','[traeff/cm$^2$/timme]']
        labels = ['Lufttryck', 'Lufttemperatur', 'Relativ fuktighet', 'Vindhastighet', 'Vindriktning', 'Regn','Hagel']
    else:
        labels = ['Air pressure', 'Air temperature', 'Relative humidity', 'Wind speed' , 'Wind direction', 'Rain','Hail']
        ylabels = ['[hPa]', '[$^\circ$C]', '[%]', '[m/s]', '[$^\circ$] true', '[mm/hour]','[hits/cm$^2$/hour]']

    # pressure
    fig = plt.subplot(7,1,1)
    ax1= df.P.plot(color ='k', linewidth = lw , grid= True)
    ax1.set_ylabel(ylabels[0], fontsize = s, labelpad = lp)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax1.get_yticks()
    ax1.set_title(labels[0], fontsize= s*1.5)
    ax1.set_yticklabels(yticks.astype(int), fontsize= s)
    ax1.get_yaxis().set_label_coords(-0.07,0.5)
    ax1.set_xlim(df.index.values.min(), df.index.values.max())

    # temperature
    fig = plt.subplot(7,1,2)
    ax2 = df.Ta.plot(color='red', linewidth = lw, grid= True)
    ax2.set_ylabel(ylabels[1], fontsize = s, labelpad = lp)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax2.get_yticks()
    ax2.set_title(labels[1], fontsize= s*1.5)
    ax2.set_yticklabels(yticks.astype(int), fontsize= s)
    ax2.get_yaxis().set_label_coords(-0.07,0.5)
    ax2.set_xlim(ax1.get_xlim())

    # relative humidity
    fig = plt.subplot(7,1,3)
    ax3 = df.RH.plot(color ='darkblue', linewidth = lw, grid= True)
    ax3.set_ylabel(ylabels[2], fontsize = s, labelpad = lp)
    ax3.set_xticks(xticks)
    ax3.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax3.get_yticks()
    ax3.set_title(labels[2], fontsize= s*1.5)
    ax3.set_yticklabels(yticks.astype(int), fontsize= s)
    ax3.get_yaxis().set_label_coords(-0.07,0.5)
    ax3.set_xlim(ax1.get_xlim())

    
    # wind speed
    fig = plt.subplot(7,1,4)
    ax4 = df.ws.plot(color ='teal', linewidth = lw, grid= True)
    ax4.set_ylabel(ylabels[3], fontsize = s, labelpad = lp)
    ax4.set_xticks(xticks)
    ax4.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax4.get_yticks()
    ax4.set_title(labels[3], fontsize= s*1.5)
    ax4.set_yticklabels(yticks.astype(int), fontsize= s)
    ax4.get_yaxis().set_label_coords(-0.07,0.5)
    ax4.set_xlim(ax1.get_xlim())


    # wind direction
    fig = plt.subplot(7,1,5)
    ax5 = df.wd.plot(color ='darkgreen', linewidth = lw, grid= True)
    ax5.set_ylabel(ylabels[4], fontsize = s, labelpad = lp)
    ax5.set_xticks(xticks)
    ax5.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax5.get_yticks()
    ax5.set_title(labels[4], fontsize= s*1.5)
    ax5.set_yticklabels(yticks.astype(int), fontsize= s)
    ax5.get_yaxis().set_label_coords(-0.07,0.5)
    ax5.set_xlim(ax1.get_xlim())

    # rain
    fig = plt.subplot(7,1,6)
    ax6 = df.Rain.plot(color = 'grey', linewidth = lw, grid= True)
    ax6.set_ylabel(ylabels[5], fontsize = s, labelpad = lp)
    ax6.set_xticks(xticks)
    ax6.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax6.get_yticks()
    ax6.set_title(labels[5], fontsize= s*1.5)
    ax6.set_yticklabels(np.round(yticks, decimals= 4), fontsize= s)
    ax6.get_yaxis().set_label_coords(-0.07,0.5)
    ax6.set_xlim(ax1.get_xlim())

    # extra axis with dates
    ax8 = ax6.twiny()
    ax8.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
    ax8.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
    ax8.spines['bottom'].set_position(('outward', 40))
    newlabel = []
    times = df.TIMESTAMP.values[::6*24].astype(str) # labels of the xticklabels: the position in the new x-axis
    for t in times: 
        newlabel.append(t[0:10]) 
    newpos   = df.index.values[::6*24]  # position of the xticklabels in the old x-axis
    ax8.set_xticks(newpos)
    ax8.set_xticklabels(newlabel, rotation = 45, fontsize = s)
    ax8.set_xlim(ax1.get_xlim())

    plt.xlabel('time [hour]', fontsize= s*2)
    plt.tight_layout()
    

    # send to RCG server for plotting on WEB
    name = 'Bridge_plot'
    if swedish is True:
        name  = 'Bridge_plot_sv'

    # save locally
    local_name = 'C:/DATA/Figures/' +name  + str(datetime.date.today()) + '.png'
    plt.savefig(local_name, facecolor=fig.get_facecolor(), transparent=True)
  

    return(local_name)



def roof_plot(df, swedish = False ):
    '''This function plots GVC roof date of the four last days at 10 min resolution.

    Parameter:

    swedish(bool): set to True for swedish axis labels, standard is english

    '''

    # language for labelling
    if swedish is True:
      ylabels = ['[hPa]', '[$^\circ$C]', '[%]', '[m/s]', '[$^\circ$] true', '[mm/timme]','[traeff/cm$^2$/timme]', '[W/m$^2$]', '[W/m$^2$]']
      labels = ['Lufttryck', 'Lufttemperatur', 'Relativ fuktighet', 'Vindhastighet', 'Vindriktning', 'Regn','Hagel', 'Inkommande långvågig strålning',  'Inkommande kortvågig strålning']
    else:
      ylabels = ['[hPa]', '[$^\circ$C]', '[%]', '[m/s]', '[$^\circ$] true', '[mm/hour]','[hits/cm$^2$/hour]', '[W/m$^2$]', '[W/m$^2$]']
      labels = ['Air pressure', 'Air temperature', 'Relative humidity', 'Wind speed' , 'Wind direction', 'Rain','Hail', 'Incoming longwave radiation' ,'Incoming shortwave radiation']


    plt.figure(figsize= (20,35))

    # fontsize
    s= 32
    #linewidth
    lw = 3.0
    #label pad
    lp = 40

    # x tick formatting
    xticks = df.index.values[::6*8]
    xticklabels = df.dtime.dt.hour.values[::6*8]

    # pressure
    fig = plt.subplot(9,1,1)
    ax1= df.P.plot(color ='k', linewidth = lw , grid= True)
    ax1.set_ylabel(ylabels[0], fontsize = s, labelpad = lp)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax1.get_yticks()
    ax1.set_yticklabels(yticks.astype(int), fontsize= s)
    ax1.get_yaxis().set_label_coords(-0.07,0.5)
    ax1.set_title(labels[0], fontsize= s*1.5)
    ax1.set_xlim(df.index.values.min(), df.index.values.max())
    #ax1.set_xlim(xticks.min(), xticks.max())

    # temperature
    fig = plt.subplot(9,1,2)
    ax2 = df.Ta.plot(color='red', linewidth = lw, grid= True)
    ax2.set_ylabel(ylabels[1], fontsize = s, labelpad = lp)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax2.get_yticks()
    ax2.set_yticklabels(yticks.astype(int), fontsize= s)
    ax2.get_yaxis().set_label_coords(-0.07,0.5)
    ax2.set_title(labels[1], fontsize= s*1.5)
    ax2.set_xlim(ax1.get_xlim())

    # relative humidity
    fig = plt.subplot(9,1,3)
    ax3 = df.RH.plot(color ='darkblue', linewidth = lw, grid= True)
    ax3.set_ylabel(ylabels[2], fontsize = s, labelpad = lp)
    ax3.set_xticks(xticks)
    ax3.set_xticklabels(xticklabels, fontsize= s)
    yticks= ax3.get_yticks()
    ax3.set_yticklabels(yticks.astype(int), fontsize= s)
    ax3.get_yaxis().set_label_coords(-0.07,0.5)
    ax3.set_title(labels[2], fontsize= s*1.5)
    ax3.set_xlim(ax1.get_xlim())

    # wind speed
    fig = plt.subplot(9,1,4)
    ax4 = df.ws.plot(color ='teal', linewidth = lw, grid= True)
    ax4.set_ylabel(ylabels[3], fontsize = s, labelpad = lp)
    ax4.set_xticks(xticks)
    ax4.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax4.get_yticks()
    ax4.set_title(labels[3], fontsize= s*1.5)
    ax4.set_yticklabels(yticks.astype(int), fontsize= s)
    ax4.get_yaxis().set_label_coords(-0.07,0.5)
    ax4.set_xlim(ax1.get_xlim())

    # wind direction
    fig = plt.subplot(9,1,5)
    ax5 = df.wd.plot(color ='darkgreen', linewidth = lw, grid= True)
    ax5.set_ylabel(ylabels[4], fontsize = s, labelpad = lp)
    ax5.set_xticks(xticks)
    ax5.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax5.get_yticks()
    ax5.set_title(labels[4], fontsize= s*1.5)
    ax5.set_yticklabels(yticks.astype(int), fontsize= s)
    ax5.get_yaxis().set_label_coords(-0.07,0.5)
    ax5.set_xlim(ax1.get_xlim())

    # rain
    fig = plt.subplot(9,1,6)
    ax6 = df.Rain.plot(color = 'grey', linewidth = lw, grid= True)
    ax6.set_ylabel(ylabels[5], fontsize = s, labelpad = lp)
    ax6.set_xticks(xticks)
    ax6.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax6.get_yticks()
    ax6.set_title(labels[5], fontsize= s*1.5)
    ax6.set_yticklabels(np.round(yticks, decimals= 4), fontsize= s)
    ax6.get_yaxis().set_label_coords(-0.07,0.5)
    ax6.set_xlim(ax1.get_xlim())


    # hail
    fig =plt.subplot(9,1,7)
    ax7 = df.Hail.plot(color = 'lightblue', linewidth = lw, grid= True)
    ax7.set_ylabel(ylabels[6], fontsize = s, labelpad = lp)
    ax7.set_xticks(xticks)
    ax7.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax7.get_yticks()
    ax7.set_title(labels[6], fontsize= s*1.5)
    ax7.set_yticklabels(np.round(yticks, decimals = 4), fontsize= s)
    ax7.get_yaxis().set_label_coords(-0.07,0.5)
    ax7.set_xlim(ax1.get_xlim())
    
    # L down
    fig =plt.subplot(9,1,8)
    ax8 = df.L_down.plot(color = 'orange', linewidth = lw, grid= True)
    ax8.set_ylabel(ylabels[7], fontsize = s, labelpad = lp)
    ax8.set_xticks(xticks)
    ax8.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax8.get_yticks()
    ax8.set_title(labels[7], fontsize= s*1.5)
    ax8.set_yticklabels(yticks.astype(int), fontsize= s)
    ax8.get_yaxis().set_label_coords(-0.07,0.5)
    ax8.set_xlim(ax1.get_xlim())

    # K down
    fig =plt.subplot(9,1,9)
    ax9 = df.K_down_SPN1.plot(color = 'purple', linewidth = lw, label = 'global', grid= True)
    ax9 = df.K_diff_SPN1.plot(color = 'violet', linewidth = lw, label = 'diffus', grid= True)
    ax9.legend(fontsize = s)
    ax9.set_ylabel(ylabels[8], fontsize = s, labelpad = lp)
    ax9.set_xticks(xticks)
    ax9.set_xticklabels(xticklabels, fontsize= s)
    yticks = ax9.get_yticks()
    ax9.set_title(labels[8], fontsize= s*1.5)
    ax9.set_yticklabels(yticks.astype(int), fontsize= s)
    ax9.get_yaxis().set_label_coords(-0.07,0.5)
    ax9.set_xlim(ax1.get_xlim())
    
    
    
    # extra axis with dates
    ax8 = ax9.twiny()
    ax8.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
    ax8.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
    ax8.spines['bottom'].set_position(('outward', 40))
    newlabel = []
    times = df.TIMESTAMP.values[::6*24].astype(str) # labels of the xticklabels: the position in the new x-axis
    for t in times: 
        newlabel.append(t[0:10]) 
    newpos   = df.index.values[::6*24]  # position of the xticklabels in the old x-axis
    ax8.set_xticks(newpos)
    ax8.set_xticklabels(newlabel, rotation = 45, fontsize = s)
    ax8.set_xlim(ax1.get_xlim())

    plt.xlabel('time [hour]', fontsize= s*2)
    plt.tight_layout()
    

    # send to RCG server for plotting on WEB
    name = 'GVC_plot'
    if swedish is True:
        name  = 'GVC_plot_sv'

    # save locally
    local_name = 'C:/DATA/Figures/' +name + str(datetime.date.today()) + '.png'
    plt.savefig(local_name, facecolor=fig.get_facecolor(), transparent=True)

    return(local_name)
    
def roof_table(df, swedish = False):
    '''This function creates an image showing a table with the latest measurement for meteorological data from the bridge. 

    Parameter:

    df: dataframe containing data of the latest four days   
    swedish(bool): optional choice for labels, True for swedish, standard is English 

    '''

   # extract latest measurement 
    subset = df.iloc[-1, :]
    time = subset.TIMESTAMP

    # language for labelling
    if swedish is True:
        name  = 'GVCtable_plot_sv'
        labels = ['Tid','Lufttryck', 'Lufttemperatur', 'Relativ fuktighet', 'Vindhastighet', 'Vindriktning', 'Regn','Hagel', 'Inkommande långvågig strålning',  'Inkommande kortvågig strålning global',  'Inkommande kortvågig strålning diffus']
        ylabels= ['CEST', 'hPa', 'gradC', '%', 'm/s', 'grad', 'mm/timme','traeff/cm$^2$/timme', 'W/m$^2$', 'W/m$^2$', 'W/m$^2$']

    else:
        name = 'GVCtable_plot'
        labels = ['Time','Air pressure', 'Air temperature', 'Relative humidity', 'Wind speed' , 'Wind direction', 'Rain','Hail', 'Incoming longwave radiation' ,'Incoming shortwave radiation global', 'Incoming shortwave radiation diffuse']
        ylabels = ['CEST','hpa', 'degC', '%', 'm/s', 'deg', 'mm/hour','hits/cm$^2$/hour', 'W/m$^2$', 'W/m$^2$', 'W/m$^2$']
      
    # fill table with values 
    values =[time, subset.P, np.round(subset.Ta, decimals =2), subset.RH, subset.ws, subset.wd, subset.Rain, subset.Hail, np.round(subset.L_down, decimals=2), subset.K_down_SPN1, subset.K_diff_SPN1]
    table = pd.DataFrame(columns = ['variable', 'value', 'units'])
    table['value'] = values
    table['variable'] = labels
    table['units'] = ylabels

    # save pandas dataframe as image (locally)
    local_name = 'C:/DATA/Figures/' + name + str(datetime.date.today()) + '.png'
    df = table
    from pandas.plotting import table
    fig, ax = plt.subplots(figsize=(12,5))
    ax.axis('off')
    table(ax, df, loc = "center")
    plt.savefig(local_name)
 
    return(local_name)

    
def bridge_table(df, swedish = False):
    '''This function creates an image showing a table with the latest measurement for meteorological data from the bridge. 

    Parameter:

    df: dataframe containing data of the latest four days  
    swedish: optional choice for language of labels, True for swedish, standard is English 

    '''

    # extract latest measurement 
    subset = df.iloc[-1, :]
    time = subset.TIMESTAMP

    # language for labelling
    if swedish is True:
        name  = 'Bridgetable_plot_sv'
        ylabels = ['LCT', 'hPa', 'gradC', '%', 'm/s', 'grad', 'mm/5min','traeff/cm$^2$/5min']
        labels = ['Tid', 'Lufttryck', 'Lufttemperatur', 'Relativ fuktighet', 'Vindhastighet', 'Vindriktning', 'Regn','Hagel']
    else:
        labels = ['Time', 'Air pressure', 'Air temperature', 'Relative humidity', 'Wind speed' , 'Wind direction', 'Rain','Hail']
        name = 'Bridgetable_plot'
        ylabels = ['LCT', 'hPa', 'degC', '%', 'm/s', 'deg', 'mm/5min','hits/cm$^2$/5min']

    # fill table with values 
    values =[time, subset.P, subset.Ta, subset.RH, subset.ws, subset.wd, subset.Rain, subset.Hail]
    table = pd.DataFrame(columns = ['variable', 'value', 'units'])
    table['variable'] = labels
    table['units'] = ylabels
    table['value'] = values

    # save pandas dataframe as image (locally)
    local_name = 'C:/DATA/Figures/' + name +  str(datetime.date.today()) + '.png'
    df = table
    from pandas.plotting import table
    fig, ax = plt.subplots(figsize=(12,5))
    ax.axis('off')
    table(ax, df, loc = "center")
    plt.savefig(local_name)

    return(local_name)

