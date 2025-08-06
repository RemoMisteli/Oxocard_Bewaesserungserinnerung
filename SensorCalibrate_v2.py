from adc121c021 import ADC121C021
from machine import Pin
import time
from oxobutton import *
from oxocard import *

#Info for calibration, the valuese can be diffren depending on how deep the sensor is
#try to 

# Calibration table: {I2C address: (dry_voltage, wet_voltage)}
calibrations = {
    0x50: (1.77, 1),    # ADC #1: set your measured dry/wet values here (80 in dez)
    0x52: (1.8, 1.18),  # ADC #2: set your measured dry/wet values here (82 in dez)
}

# Choose which ADC you want to use:
adc_address = 0x50   # change to 0x51 if you want to use the other

adc = ADC121C021(scl=Pin(22), sda=Pin(21), addr=adc_address)
dry_voltage, wet_voltage = calibrations[adc_address]

def moisture_percent(voltage):
    percent = 100 * (dry_voltage - voltage) / (dry_voltage - wet_voltage)
    percent = max(0, min(100, percent))
    return percent

while True:
    
    voltage = adc.getValue()  # Should return voltage in V
    percent = moisture_percent(voltage)
    print("Moisture: {:.1f}% (Voltage: {:.3f}V, ADC address: 0x{:02X})".format(
        percent, voltage, adc_address
    ))
    time.sleep(1)
    
        
