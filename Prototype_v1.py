
from random import randint
from oxocard import *
from oxocardext import *
import time
from oxobutton import *
#a mode so the code can work in the simulator and on the real device
simulatorMode=False

if(not simulatorMode):
    from machine import ADC, Pin
    from music import *
    from adc121c021 import ADC121C021


#red=> no wather
#Blue=>water needed
#green => oke

#the Batterycheck returns false as long the backup batteryis not fully charged, it can take a moment until the battery is loaded

sensorValues = []
#Info for calibration, the valuese can be diffren depending on how deep the sensor is
# Calibration table: {I2C address: (dry_voltage, wet_voltage)}
calibrations = {
    0x50: (1.74, 1),    # ADC #1: set your measured dry/wet values here (80 in dez)
    0x52: (1.8, 1.18),  # ADC #2: set your measured dry/wet values here (82 in dez)
}
dry_voltage, wet_voltage = calibrations[list(calibrations)[0]]

numberOfSensors=2 

#the sensorvalues for lower and upper limit of the OK value
minSensorValue=40
maxSensorValue=80

deactivateBatteryWarning=False

button_L3=Button(BUTTON_L3)
button_L2=Button(BUTTON_L2)

button_R3=Button(BUTTON_R3)
button_R2=Button(BUTTON_R2)
button_R1=Button(BUTTON_R1)



##this updates the sonsor readings to valid results

def updateSensorReadings():
    global sensorValues
    #reset Sensorvalues
    sensorValues=[]
    for i in range(numberOfSensors):
        sensorValues.append(readSensor(i))
    #Here we can hardcode values for testing each value represets one Sensor
    #sensorValues=[10,5]
    
def moisture_percent(voltage):
    percent = 100 * (dry_voltage - voltage) / (dry_voltage - wet_voltage)
    percent = max(0, min(100, percent))
    return percent


def readSensor(sensorId):
    #simulator Mode
    if(simulatorMode):
        return randint(0, 100)
    
    #SensorMode
    adc_address=list(calibrations)[sensorId]
    dry_voltage, wet_voltage = calibrations[adc_address]
    
    voltage = ADC121C021(scl=Pin(22), sda=Pin(21), addr=adc_address).getValue()
    percent = moisture_percent(voltage)
    
    print("Moisture: {:.1f}% (Voltage: {:.3f}V, ADC address: 0x{:02X})".format(
        percent, voltage, adc_address
    ))
    
    return percent

#####

def showStatus():
    print(sensorValues)
    
    if(all(x< minSensorValue for x in sensorValues)):
        drawNeedsWater()
        
    elif(all((x >= minSensorValue and x <= maxSensorValue) for x in sensorValues)):
        drawAllOke()
        
    elif(all(x > maxSensorValue for x in sensorValues)):
        drawToMuchWater()
        
    else:
        drawDiffrentStates()

def drawNeedsWater():
    image((
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x007f00,0x007f00,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x007f00,0x000000,0x000000,0x007f00),
(0x000000,0x007f00,0x007f00,0x007f00,0x007f00,0x007f00,0x007f00,0x007f00),
(0x000066,0x000000,0x000000,0x007f00,0x000000,0x000000,0x000000,0x007f00),
(0x000066,0x000000,0x000000,0x007f00,0x000000,0x000000,0x000000,0x007f00),
(0x000000,0x000000,0x000000,0x007f00,0x007f00,0x007f00,0x007f00,0x007f00)))
    time.sleep(1)
    
def drawAllOke():
    image((
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x007f00,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x007f00,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x007f00,0x000000,0x000000,0x000000),
(0x000000,0x007f00,0x000000,0x007f00,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x007f00,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000)))

    time.sleep(1)
    
def drawToMuchWater():
    image((
(0x7f0000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x7f0000),
(0x000000,0x7f0000,0x000000,0x000000,0x000000,0x000000,0x7f0000,0x000000),
(0x000000,0x000000,0x7f0000,0x000000,0x000000,0x7f0000,0x007f00,0x000000),
(0x000000,0x000000,0x000000,0x7f0000,0x7f0000,0x000000,0x000000,0x007f00),
(0x000000,0x007f00,0x007f00,0x7f0000,0x7f0000,0x007f00,0x007f00,0x007f00),
(0x000066,0x000000,0x7f0000,0x007f00,0x000000,0x7f0000,0x000000,0x007f00),
(0x000066,0x7f0000,0x000000,0x007f00,0x000000,0x000000,0x7f0000,0x007f00),
(0x7f0000,0x000000,0x000000,0x007f00,0x007f00,0x007f00,0x007f00,0x7f0000)))

    time.sleep(1)

def getColor(value):
    if value < minSensorValue:
        return BLUE
    if value > maxSensorValue:
        return RED
    return GREEN  
    
def drawDiffrentStates():
    fillRectangle(0, 0, 4, 8, getColor(sensorValues[0]))
    fillRectangle(4, 0, 8, 8, getColor(sensorValues[1]))

    time.sleep(1)
    

#returns false as long the backup batteryis not fully charged, it can take a moment until the battery is loaded
def isBackupBatteryFull():
    if(simulatorMode):
        #in simulatorMode always return true
        return True
    adc = ADC(Pin(34))
    adc.atten(ADC.ATTN_11DB)
    
    raw = adc.read()
    voltage = raw / 4095 * 3.3
    
    estimated_battery = voltage * 4
    print("Battery------------------------")
    print("Raw ADC:", raw)
    print("Voltage (divided):", voltage)
    print("Estimated battery voltage:", estimated_battery)
    print("-------------------------------")
    #This detects if it is using the small batery or gets the engergie form somwhere else
    return estimated_battery>=3.65


def checkBattery():
    #todo call func runn backupbattery
  if(not deactivateBatteryWarning and not isBackupBatteryFull()):
    repeat(2):
        image((
    (0x000000,0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x000000,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x000000,0x000000,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x007f00,0x007f00,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x007f00,0x007f00,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x007f00,0x007f00,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000))
    )
        
        time.sleep(0.5)
        image((
    (0x000000,0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x000000,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x000000,0x000000,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x000000,0x000000,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f0000,0x7f0000,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f0000,0x7f0000,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000)))
        if(not simulatorMode):
            beep(3, 1000)
        time.sleep(0.5)


def showSensorValues():
    for i in range(numberOfSensors):
        smallTextScroll(str(i+1)+": "+str(round(sensorValues[i])))
        time.sleep(0.5)
    

        
def drawCurrentSettingOption(option):
    if(option==1):
        image((
(0x000000,0x7f7f7f,0x000000,0x000000,0x000000,0x000000,0x000000,0x7f7f7f),
(0x7f7f7f,0x7f7f7f,0x000000,0x000000,0x000000,0x000000,0x7f7f7f,0x000000),
(0x000000,0x7f7f7f,0x000000,0x000000,0x000000,0x7f7f7f,0x000000,0x000000),
(0x000000,0x7f7f7f,0x000000,0x000000,0x7f7f7f,0x000000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x7f7f7f,0x000000,0x7f7f7f,0x7f7f7f,0x000000),
(0x000000,0x000000,0x7f7f7f,0x000000,0x000000,0x000000,0x7f7f7f,0x000000),
(0x000000,0x7f7f7f,0x000000,0x000000,0x000000,0x7f7f7f,0x000000,0x000000),
(0x7f7f7f,0x000000,0x000000,0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x000000)))
    elif(option==2):
        image((
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x7f7f7f,0x00007f,0x00007f,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x7f7f7f,0x00007f,0x00007f,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x7f7f7f,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x7f7f7f,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000),
(0x000000,0x7f7f7f,0x7f0000,0x7f0000,0x7f0000,0x7f0000,0x000000,0x000000),
(0x000000,0x7f7f7f,0x7f0000,0x7f0000,0x7f0000,0x7f0000,0x000000,0x000000),
(0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000)))
    elif(option==3):
        image((
    (0x000000,0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x000000,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x000000,0x000000,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x007f00,0x007f00,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x007f00,0x007f00,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x007f00,0x007f00,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x7f7f7f,0x000000,0x000000),
    (0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000,0x000000))
    )
        
def settings():
    numberOfSettings=3    
    currentSettingOption=1
    #draw first sting icon => whit +/- durchwählen
    #when a setting selectet go to the setting
    bigTextScroll("SETTINGS")
    drawCurrentSettingOption(currentSettingOption)
    while not button_L2.wasPressed():
        if(button_R3.wasPressed()):
            currentSettingOption+=1
            if(currentSettingOption>numberOfSettings):
                currentSettingOption=1
            drawCurrentSettingOption(currentSettingOption)
        if(button_R2.wasPressed()):
            currentSettingOption-=1
            if(currentSettingOption<1):
                currentSettingOption=numberOfSettings
            drawCurrentSettingOption(currentSettingOption)
        if(button_R1.wasPressed()):
            settingSelected(currentSettingOption)
            drawCurrentSettingOption(currentSettingOption)
          
def settingSelected(option):
    if(option==1):
        sensorSetting()
    elif(option==2):
        valueSetting()
    elif(option==3):
        batterySeeting()
    


def sensorSetting():
    global numberOfSensors
    
    while not button_R1.wasPressed():
        smallTextScroll(str(numberOfSensors))
        if(button_R3.wasPressed()):
            numberOfSensors-=1
            if(numberOfSensors<1):
                numberOfSensors=len(calibrations)
        if(button_R2.wasPressed()):
            numberOfSensors+=1
            if(numberOfSensors>len(calibrations)):
                numberOfSensors=1

def batterySeeting():
    global deactivateBatteryWarning
    
    while not button_R1.wasPressed():
        if(deactivateBatteryWarning):
            fillRectangle(0, 0, 8, 8,RED )
        else:
            fillRectangle(0, 0, 8, 8, GREEN )
        if(button_R3.wasPressed() or button_R2.wasPressed()):
            deactivateBatteryWarning=not deactivateBatteryWarning

            
def valueSetting():
     global minSensorValue
     global maxSensorValue
    
    #when false max setting is edited
     updateMinSetting=True
     clear()
     while not button_L2.wasPressed():
        if(button_R3.wasPressed() or button_R2.wasPressed()):
            updateMinSetting=not updateMinSetting
        if(updateMinSetting):
            fillRectangle(2, 2, 4, 4, BLUE)
        else:
            fillRectangle(2, 2, 4, 4, RED)
        if(button_R1.wasPressed()):
            if(updateMinSetting):
                minSensorValue=updateValue(minSensorValue)
            else:
                maxSensorValue=updateValue(maxSensorValue)
            clear()  


def updateValue(value):
    while not button_R1.wasPressed():
        smallTextScroll(str(value))
        if(button_R3.wasPressed()):
            value-=1
            if(value<0):
                value=100
        if(button_R2.wasPressed()):
            value+=1
            if(value>100):
                value=0
    return value

while True: 
    updateSensorReadings()
    showStatus()
    checkBattery()
    if(button_L3.wasPressed()):
        showSensorValues()
    if(button_L2.wasPressed()):
        settings()
  
    
    
    

