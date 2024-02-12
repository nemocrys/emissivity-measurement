# exp-T-control with stationarity

## About
This script is a extension of https://github.com/nemocrys/exp-T-control. The goal is to get the emissivity of a given probe with the help of a pyrometer. A ratio-pyrometer is not needed. The Script waits for stationarity before starting a measurment. Therefore this script gives better results then v2. However to set up the stationarity two more values are needed and the script can take longer then v2.

---

## Set-Up
### Hardware Set-Up
A pyrometer should be pointed at the probe. An additional PT100 should be connected to the probe. Finally, a heating plate (IKA) that heats the probe is needed.

![Set-Up](/img.png?raw=true)

### Software Set-Up
The script can be set up with the help of "Messreihe_Rezept.txt". All values are explained there.
The pyrometers and heating plate can be set up in "config.yaml".
After that, "hauptprogramm.py" can be started, and no further action should be needed. If you see a plot that updates every 2 seconds, the script works as intended.

---
## Results
Results are stored in the data folder. Each measurement generates a plot, a file with all recorded data points and values, and a file that contains the average data and standard deviations of every measurement point.
