# Quality control of meteorological data 


All meteorological data produced by the GVC stations is quality checked based on the following tests (number indicates the quality flag code in the generated .txt files). If a variable did not pass one of the following tests, the source of the error is indicated by the number. If a variable successfully passed all tests, the quality flag is 0.




## Plausible ranges (1) 

Plausible ranges for different meteorological variables: 


- Air temperature: -50 - 50 degC
- Relative humidity: 0 - 100 %
- Wind direction : 0 - 360 deg
- Wind speed: 0 - 75  m-s
- Air pressure: 500 - 1100 hpa 


## Mutual exclusion (2)

Check for inconsistencies in data:

- wind speed == 0, but wind direction > 0 
- wind direction > 0, but wind speed == 0


## Time consistency (maximum variance) (3)


Instantanous value must not deviate more than these threshold compared to previous time steps: 

- Air temperature: 3  Cdeg
- Relative humidity: 15  %
- Air pressure: 2  hpa
- Wind speed: 20  m/s
- Irradiation: 800  W/m^2


Comparison with previous measurements (e.g. last 1-  2 hours ) to avoid big jumps in data. 

| x_1 - x_0 | + | x - x_2 | > 4 * std |
                                      

where x_0 is the previous and x_2 is the next measured value. 


## Time persistence (minimum variance)   (4)


Check for minimum variance to detect dead bands and sensor blocking. Instantanous value compared to past hours values and standard variation of past hour values should be more than: 



- Air temperature: 0.1°C 
- Relative humidity: 1% 
- Atmospheric pressure: 0.1 hPa 
- Wind direction: 10 deg
- Wind speed: 0.5 ms -1 



**The quality control is based on  the suggested WMO standards for quality control of meteorological data:** 

Zahumensky, Igor. (2004). Guidelines on Quality Control Procedures for Data from Automatic Weather Stations. 
