# fhem_read_heating_values
Read out the temperature of a heating device

- This script enables to read analog values (voltages representing temperatures) from a house heating device (e.g. Paradigma) with a raspi.
- The values are handed over to FHEM house automation for further processing and visualization (tracking of temperatures, solar income,...)

# Installation / Prerequisites

- Running Raspi
- Analog -> Digital Device (here: MCP3008 ADC device using the SPI Bus)
- wiring to heating system
- running FHEM for house automation -> calling python script out of fhem in recurring time steps...

# Usage

- Measuring the voltages and calculating back the temperatures


# Issues

- Voltage divider has to be known or to be evalutated while measureing some temperature/voltage tuples
