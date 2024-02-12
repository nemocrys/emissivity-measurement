# Two pyrometers

## About
This script is a rewrite of [exp-T-control-v2_with-stationarity](https://github.com/nemocrys/exp-T-control-v2_with-stationarity). The goal is to get the emissivity of a given probe with the help of a ratio-pyrometer. If you want to determin the factor k use [TwoPyros_determineK](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros_determineK).

---

## Set-Up
### Hardware Set-Up
A ratio-pyrometer and a normal pyrometer should be pointed at the probe. An additional PT100 should be connected to the probe. Finally, a heating plate (IKA) that heats the probe is needed.

![Set-Up](/img.png?raw=true)

### Software Set-Up
The script can be set up with the help of "settings.txt". All values are explained there.
The pyrometers and heating plate can be set up in "config.yaml".
After that, "hauptprogramm.py" can be started, and no further action should be needed. If you see a plot that updates every 2 seconds, the script works as intended.

---
## Results
Results are stored in the data folder. Each measurement generates a plot.png, a data.csv with all recorded data points and values, and a measurment_data.csv that contains the average data and standard deviations of every measurement point.
