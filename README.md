# exp-T-control-v3: One pyrometer

## About
This script is a modification of https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros, which is a rewrite of https://github.com/nemocrys/exp-T-control-v3. The goal is to get the emissivity of a given probe with the help of only one ratio-pyrometer. The ratio-pyrometer measures both in the ratio mode and in the mono mode, so the emissivity can be calculated numerically.

---

## Set-Up
### Hardware Set-Up
A ratio-pyrometer should be pointed at the probe. An additional PT100 can be connected to the probe. Finally, a heating plate (IKA) that heats the probe is needed.

### Software Set-Up
The script can be set up with the help of "settings.txt". All values are explained there.
The pyrometer and heating plate can be set up in "config.yaml".
After that, "hauptprogramm.py" can be started, and no further action should be needed. If you see a plot that updates every 2 seconds, the script works as intended.

---
## Results
Results are stored in the data folder. Each measurement generates a plot.png, a data.csv with all recorded data points and values, and a measurment_data.csv that contains the average data and standard deviations of every measurement point.
