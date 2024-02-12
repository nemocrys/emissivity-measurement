# exp-T-control-v3: Two pyrometers and determination of factor k

## About
This script is based on [exp-T-control-v3/tree/TwoPyros,](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros) which is a rewrite of https://github.com/nemocrys/exp-T-control-v3. The goal is to get the emissivity and factor k of a given probe with the help of a ratio-pyrometer.

---

## Set-Up
### Hardware Set-Up
A ratio-pyrometer and a normal pyrometer should be pointed at the probe. An additional PT100 should be connected to the probe. Finally, a heating plate (IKZ) that heats the probe is needed.

### Software Set-Up
The script can be set up with the help of "settings.txt". All values are explained.
The pyrometers and heating plate can be set up in "config.yaml".
After that, "hauptgrogramm.py" can be started, and no further action should be needed. If you see a plot that updates every 2 seconds, the script works as intended.

---
## Results
Results are stored in the data folder. Each measurement generates a plot.png, a measurment_data.csv with all recorded data points and values, and a data.csv that contains the average data and standard deviations of every measurement point.
