ZONDEO LINK HERE [![DOI]()]()

# emissivity-measurement

This script is used to experimently determine the emissivity of a probe at different temperatures, using a radiometric technique, as described in [this paper](http://dx.doi.org/10.1615/IHTC17.380-70). In summary, emissivity is iteratively adjusted until the temperature reading of the pyrometer matches the temperature measured with a reference sensor, e.g. contact sensor (Pt100) or ratio pyrometer.

## Referencing

The project is developed and maintained by the Model experiments group at the Leibniz Institute for Crystal Growth (IKZ). If you use this code in your research, please cite our associated publication:

> S. Foroushani, A. Wintzer, K. Dadzis, In-situ measurement of emissivity in crystal growth furnaces, International Heat Transfer Conference (IHTC17), Cape Town, South Africa, Paper 545 (2023).

## Required hardware:
An externally controllable heating plate, one Pt-sensor, a normal and a ratio pyrometer (depending on the used branch). The probe should have a side hole to the center, about 1 mm blow the surface, for inserting the contact sensor. See [here](https://github.com/nemocrys/exp-T-control) for a list of sample devices. 

## Usage overview

The following files are used to change the devices and measurement settings:

- settings.txt can be used to specify the temperature setpoints, at which measurements will be made.  At each step, the script will then steer the heating plate until the probe has reached the desired temperature, within a given threshold.
- Config.yml entails the connection information and parameters of the various devices. 

More details about the script, functions and the user interface can be found [here](https://github.com/nemocrys/exp-T-control).

## Variants

Based on the measurement setup, namely the reference temperature sensor, one of the following variants must be used:

- [exp-T-control-v2_with-stationarity](https://github.com/nemocrys/exp-T-control-v3/tree/exp-T-control-v2_with-stationarity) Is a modification of [exp-T-control](https://github.com/nemocrys/exp-T-control) with the added feature that measurements start after the probe temperature has reached steady state. 

- [TwoPyros](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros) is a rewrite of [exp-T-control-v2_with-stationarity](https://github.com/nemocrys/exp-T-control-v3/tree/exp-T-control-v2_with-stationarity), with a ratio pyrometer used as the reference sensor, thereby eliminating the need for a contact sensor, making the setup purely optical. 

- [TwoPyros_determineK](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros_determineK) is a variant of TwoPyros where the factor k is automatically determined based on comparison with the contact sensor. This can be used for validation of measurements using [TwoPyros](https://github.com/nemocrys/exp-T-control-v3/tree/TwoPyros).

- [OnePyro](https://github.com/nemocrys/exp-T-control-v3/tree/OnePyro) alternates the ratio pyrometer between the normal and ratio modes, thereby eliminating the need for a second pyrometer.

## Acknowledgements

[This project](https://nemocrys.github.io/) has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 851768).

<img src="https://raw.githubusercontent.com/nemocrys/pyelmer/master/EU-ERC.png">
