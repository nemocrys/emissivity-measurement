[![DOI](https://zenodo.org/badge/464367892.svg)](https://zenodo.org/badge/latestdoi/464367892)

# emissivity-measurement
Emissivity measurements using pyrometers

This script is used to experimently determine the emissivity of a probe at different temperatures.

The project is developed and maintained by the Model experiments group at the Leibniz Institute for Crystal Growth (IKZ).

## Referencing

If you use this code in your research, please cite this repository and our associated publication:

> A. Wintzer, K. Dadzis: github.com/nemocrys/emissivity-measurement, [https://doi.org/10.5281/zenodo.8202759](https://zenodo.org/badge/latestdoi/464367892).
> S. Foroushani, A. Wintzer, K. Dadzis: IHTC.

## Principle

This script can be used to automate emissivity measurement and data aquisition using a radiometric technique, as described in IHTC paper. In summary, emissivity is iteratively adjusted until the temperature reading of the pyrometer matches the temperature measured with a reference sensor, e.g. a contact sensors (thermocouple) or a ratio pyrometer.



## Basic functioning

Use settings.txt to specify at which temperatures and how a measurement should be made. The script heats the plate and reads the temperature of the probe to decide if a measurement can begin. For the measurement, the emissivity value of a pyrometer is adjusted until T_pyro == T_true. After a measurement, the data is stored, and the script goes to the next temperature.

## Required hardware:
An external controllable heating plate, one PT-sensor, a normal and a ratio pyrometer (depended on the used branch). The probe should have a borehole to the center of the probe, 1 mm blow the surface and large enough to insert the pt-sensor.

## Variants

Four branches currently exist.

[exp-T-control-v2_with-stationarity](https://github.com/nemocrys/exp-T-control-v3/tree/exp-T-control-v2_with-stationarity) Is a modification based of [exp-T-control](https://github.com/nemocrys/exp-T-control). The script now waits until temperature is stationary. Otherwise it is identical. 

[TwoPyros](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros) is a rewrite of [exp-T-control-v2_with-stationarity](https://github.com/nemocrys/exp-T-control-v3/tree/exp-T-control-v2_with-stationarity) that is used to utilize a ratio-pyrometer to determine the "true" temperature. A PT100 inside the probe can be used but is not needed.

[TwoPyros_determineK](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros_determineK) is a version of TwoPyros that is used to additionally determine the factor k. A PT100 inside the probe is needed.

[OnePyro](https://github.com/nemocrys/exp-T-control-v3/tree/OnePyro) is a version of TwoPyros that only uses one ratio-pyrometer for the "true" temperature **and** emissivity dependent temperature. PT100 inside the probe can be used but is not needed.


## Acknowledgements

[This project](https://nemocrys.github.io/) has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 851768).

<img src="https://raw.githubusercontent.com/nemocrys/pyelmer/master/EU-ERC.png">
