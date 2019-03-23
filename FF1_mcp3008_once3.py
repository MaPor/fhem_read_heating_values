#!/usr/bin/python
#--------------------------------------
# MCP3008 ADC device using the SPI bus.
#
# http://www.raspberrypi-spy.co.uk/

import spidev
import time
import datetime
import os
import math

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Define voltage devider
feeding_voltage = 5 	#Volts from Paradigma Heating System
resistance_upper_PT1000 = 1265 #1165 #1265 #1165Ohm from upper resistor of voltage devider, bottom R is NTC
resistance_upper_NTC = 2100 #1950 #Ohm from upper resistor of voltage devider, bottom R is NTC

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data


def readadc(adcnum):
    ## read SPI data from MCP3208 chip, 8 possible adc's (0 thru 7)
    #if adcnum > 7 or adcnum < 0:
    #    return -1
    #print '10bit ', [1, 8 + adcnum << 4, 0]
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

def readadc12(adcnum):
    if adcnum > 7 or adcnum < 0:
    #just to check if adcnum is out of the A/D converters channel range
     return -1
    r = spi.xfer2([4 | 2 | (adcnum >> 2), (adcnum & 3) << 6, 0])
    #send the three bytes to the A/D in the format the A/D's datasheet explains(take time to
    #doublecheck these
    adcout = ((r[1] & 15) << 8) + r[2]
    #use AND operation with the second byte to get the last  4 bits, and then make way
    #for the third data byte with the "move 8 bits to left" << 8 operation
    return adcout



# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places,adc_bits):
    volts = (data * feeding_voltage) / float(adc_bits) #1023#3.3
    volts = round(volts,places)
    #print volts , data
    return volts



for i in range(0,7):
    adc_value = readadc12(i)
    volts = ConvertVolts(adc_value,6,4095)
    #print volts
    current = (feeding_voltage-volts)/resistance_upper_NTC
    NTC_raw = volts/current
    NTC_R = round((volts/current),1)
    #print NTC_raw
    Temp = round((math.log(NTC_raw/12832)/(-0.038)),1)

    anzahl_ntc_whd = 8

    if i == 5:
	Temp_Summe = 0
        for j in range(0,anzahl_ntc_whd):
		adc_value = readadc12(i)
		volts = ConvertVolts(adc_value,6,4095)
		current = (feeding_voltage-volts)/resistance_upper_PT1000
		NTC_raw = volts/current
        	NTC_R = round((volts/current),1)
		a=0.0077
		b=2.965
		c=994.12-NTC_raw
		d=((b*b)-(4*a*c))
                if d > 0:
                  #print("d={}".format(d))
                  d=math.sqrt((b*b)-(4*a*c))
		  Temp = round(((-b+d)/(2*a)),1)
		else:
		  Temp=-33
		Temp_Summe = Temp + Temp_Summe 
		#print("i={}, j={}, Digital={}, V={}, R={}, Temp={}, Temp_Summe={},".format(i,j,adc_value,volts,NTC_R,Temp,Temp_Summe))
		time.sleep(0.135)
	Temp=Temp_Summe/anzahl_ntc_whd;
    print("{}".format(Temp))
    #print("i={}, Digital={}, V={}, R={}, Temp={},".format(i,adc_value,volts,NTC_R,Temp))

