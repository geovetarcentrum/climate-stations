"""
This script processes meteorological data from GVC logger files
(both roof and bridge) performs a quality check and produces
monthly .csv files that can be downloaded from web.

> python dataprocessing.py
> python dataprocessing.py 2021 8

If called with command-line arguments year and month, it updates the csv
files for that time (without makeing plots of backup copies). 
If you want to update the plot, then presumably you want the current
month, so you don't need to give any cmd-line args

Contact: juliakukulies@gu.se David.Rayner@gu.se
"""

import sys
from datetime import date
from utils import copyfile, load_logger_data, make_csv, make_plot

import config

################################################################################ Default

if len(sys.argv) == 1:
    default_mode = True
    month = int(date.today().month)
    year = int(date.today().year)
else:
    default_mode = False
    year = int(sys.argv[1])
    month = int(sys.argv[2])

for pset in config.sets_to_process:

    f = pset["logger_file"]
    if default_mode:
        # backup copy
        copyfile(f, pset["backup_dir"] / f.name)

    table = load_logger_data(f)
    source = make_csv(table, pset, year, month)

    if pset["csv_web_dir"]:
        # send to .csv file to RCG server via shared drive
        target = pset["csv_web_dir"] / source.name
        copyfile(source, target)

    if default_mode and pset["plot_output_dir"]:
        make_plot(table, pset)
