"""
Config params for dataprocessing.py

These are parameters that need to be changed to run a test config.

@author: David Rayner
"""
from pathlib import Path

# target directory for web files
logger_dir = Path("C:/DATA/")

web_files = Path("//130.241.159.111/UCG/WebFiles")

csv_output_dir = Path("C:/DATA/Files/")

plots_output_dir = Path("C:/DATA/Figures/")

backup_dir = Path("//store-lyk-2.it.gu.se/Nf/GVC/Klimatst/Nya/")

do_QC = True

# leave plot_output_dir empty for no plot
sets_to_process = [
  {"logger_file":logger_dir / "Taket" / "Roof_meteo_5min.dat", 
  "interval":"5", 
  "station":"roof", 
  "backup_dir":backup_dir,
  "csv_output_dir":csv_output_dir,
  "csv_web_dir":web_files/"GVCdata", 
  "plot_output_dir":plots_output_dir,
  "plot_web_dir":web_files,
  "do_QC":do_QC},
   {"logger_file":logger_dir / "Taket" / "Roof_meteo_10min.dat", 
  "interval":"10", 
  "station":"roof", 
  "backup_dir":backup_dir,
  "csv_output_dir":csv_output_dir,
  "csv_web_dir":web_files/"GVCdata", 
  "plot_output_dir":None,
  "plot_web_dir":None,
  "do_QC":do_QC},
  {"logger_file":logger_dir / "Bron" / "Bridge_meteo_5min.dat", 
  "interval":"5", 
  "station":"bridge", 
  "backup_dir":backup_dir,
  "csv_output_dir":csv_output_dir,
  "csv_web_dir":web_files/"Bridgedata", 
  "plot_output_dir":plots_output_dir,
  "plot_web_dir":web_files,
  "do_QC":do_QC},
   {"logger_file":logger_dir / "Bron" / "Bridge_meteo_10min.dat", 
  "interval":"10", 
  "station":"bridge", 
  "backup_dir":backup_dir,
  "csv_output_dir":csv_output_dir,
  "csv_web_dir":web_files/"Bridgedata", 
  "plot_output_dir":None,
  "plot_web_dir":None,
  "do_QC":do_QC}  
   ]

 