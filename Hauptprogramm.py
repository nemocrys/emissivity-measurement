#!/usr/bin/env python3
import adafruit # ptSensor
import heizer  # Heizplatte & Temperaturmessung
import pyrometer_lumasense # Steuert das Ratio-Pyrometer

import os
import time
import datetime
import yaml

import matplotlib.pyplot as plt
import numpy as np

# converges to the true emisity with each call
def Emissions_Anpassung(Temp_Pyro, Temp_Oberf, e_Alt, e_Drauf, o_Grenze, u_Grenze):                                  # Funktion für das Emissionsgrad bestimmen
    if Temp_Pyro != Temp_Oberf:                               # Wenn die Werte gleich sind, soll der Emissionsgrad bleiben wir er ist
        e_Drauf = e_Drauf/2                                     # Bei Ungleichheit wird e_Drauf halbiert
    if Temp_Oberf > Temp_Pyro:                                # Wenn die Oberflächentempratur größer als die des Pyrometrs ist, so ...
        e_Alt = round(e_Alt - e_Drauf,1)                        # ... wird der Emissionsgrad kleiner
        if e_Alt < u_Grenze:                                    # Bei Grenzunterschreitung wird der Emissionsgrad auf der Untergrenze gehalten
            e_Alt = u_Grenze
            e_Drauf = e_Drauf * 2
    if Temp_Oberf < Temp_Pyro:                                # Wenn Pyrometer Temperatur größer ist als die der Oberfläche, dann ...
        e_Alt = round(e_Alt + e_Drauf,1)                        # ... wird der Emissionsgrad größer
        if e_Alt > o_Grenze:                                    # Bei Grenzüberschreitung wird der Emissionsgrad auf der Obergrenze gehalten
            e_Alt = o_Grenze
            e_Drauf = e_Drauf * 2
    e_Neu = e_Alt                                             # wenn die Temperaturen gleich sind, so wird der Alte_Wert zurückgegeben, sonst der neu berechnete!
    return e_Neu, e_Drauf

# calculates a rolling average of the list "List" with "N" net points.
# To get len(List) == len(listAvg), at the end of the list "listAvg" the last value will be appended, until the condition is true. 
def rollingAvg(List,N):
    if len(List) > N:
        listAvg = []
        for i in range(len(List) - N + 1):
            window = List[i : i + N]
            window_average = round(sum(window) / N, 2)
            listAvg.append(window_average)
                
        for i in range(len(listAvg), len(List)):
            listAvg.append(listAvg[-1])
    else:
        listAvg = List
    return listAvg


# Creates the folder where the results are stored and the csv files and first lines of them
# returns the path to the folder
def createFiles():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    parent_dir = "./data/"
    
    # Automatische Erzeugung von eindeutigen Filenamen, ohne das eine alte Datei überschrieben wird:
    directoryIndex = '#'+str(1).zfill(2)
    directory = f"{date}_{directoryIndex}" # Andere Dateiendungen (z.B. dat) auch möglich
    j = 1
    while os.path.exists(parent_dir + '/' + directory): # Schaut ob es den Namen schon in dem Verzeichnis gibt ...
        j = j + 1 # ... wenn ja wird der FleOutIndex (j) solange erhöht bis es eine neue Datei erstellen kann
        directoryIndex = '#'+str(j).zfill(2)
        directory = f"{date}_{directoryIndex}"
    
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    
    # Pepare Files
    with open(os.path.join(path, "data.csv"), "w", encoding="utf-8") as f: 
        f.write("tTarget,tHeizplate,tSample,tRatio,tRatio_avg,tMono,E\n")
        
    with open(os.path.join(path, "measurement_data.csv"), "w", encoding="utf-8") as f: 
        f.write(f"k,tTarget,tSample_avg,tSample_std,tRatio_avg,tRatio_std,tMono_avg,tMono_std,E_last,EmisSensor\n")
        
    return path


# reads the file "settings.txt"
# Erg: lists from the recepy
def readRezept(debugPrint=True):
    with open("settings.txt", "r", encoding="utf-8") as f:
        rezept = f.read().split("\n")
    
    tTarget             = [] # in °C
    tToleranz           = [] # in °C
    tTime               = []   # in min
    tStationaer         = [] # in min
    tStationaerTolerace = [] # in °C
    sensorList          = []
    targetSensor        = ""
    
    for temp in rezept:
        line = temp.replace(" ", "")
        
        if line.startswith("s:"):
            sensorList = line.split(",")
            sensorList[0] = sensorList[0][2:] # remove the "s:"
        
        elif line.startswith("m:"):
            targetSensor = line[2:] # remove the "m:"
            
        elif line.startswith("r:"):
            tTarget.append(line.split(",")[0])
            tToleranz.append(line.split(",")[1])
            tTime.append(line.split(",")[2])
            tStationaer.append(line.split(",")[3])
            tStationaerTolerace.append(line.split(",")[4])


    # remove the "r:"
    for i in range(len(tTarget)):
        tTarget[i] = tTarget[i].replace("r:", "")
        
    if debugPrint == True:
        print("\n-----------------------")
        print(f"tTarget:        {tTarget}")             # Liste der Zieltemeraturen
        print(f"tToleranz:      {tToleranz}")           # Liste des Tolranzbereich für die Zieltemeraturen
        print(f"tTime:          {tTime}")               # Liste der Zeiten die für die Messung verwedet werden soll
        print(f"tStatio:        {tStationaer}")         # Liste der Zeiten, die die Temperatur stationär sein soll
        print(f"tStatioToleranz:{tStationaerTolerace}") # Liste der Toleranz der Stationärtemperatur
        print(f"SensorList:     {sensorList}")          # Liste die Angibt, ob mit ratiopyrometer oder dem pt Sensor gemessen werden soll (oder beiden) gültige Werte: pyro, pt
        print(f"targetSensor:   {targetSensor}")        # Gibt den Sensor an der verwendet wird für die Berechnung der ZielTemp&Stationärität
        print("-----------------------\n")
        
    return tTarget, tToleranz, tTime, tStationaer, tStationaerTolerace, sensorList, targetSensor


# Erg: plots lines with new data
def plotData(ax ,x , List, Line):
    Line.set_xdata(x/30)
    ax.set_xlim([0, len(List)/30+1/30])
    
    if List != None:
        Line.set_ydata(List) # plot new line


# checks if temperature is stationary
# Vor: tList:               Liste der Temperaturen die geprüft werden sollen
#      tStationär:          Wie lang die Stationärität daueren soll in Minuten
#      tStationaerTolerace: Welche Temperaturabweichung "geduldet" wird in °C
def stationaerPruefung(tList, tStationaer, tStationaerTolerace):
    isStationaer = False
    if len(tList) > tStationaer: # Nur prüfen wenn über StationarTime Einträge vohanden sind
        tempList = tList[int(-tStationaer * 30):] # Liste der letzten Temperaturen erstellen...
        tempList.sort() # ...und sortieren
        #print(f"Größte   Temp:{round(tempList[-1],2)}\nKleinste Temp:{round(tempList[0],2)}")
        if tempList[-1] - tempList[0] <= tStationaerTolerace: # Wenn die größte die Temperaur und die Kleinste Temp. kleiner sind als der vorggebene Bereich
            isStationaer = True
            #print("Stationaer")
        else:
            isStationaer = False
            #print("Nicht Stationaer")
    return isStationaer
            
# closes program correctly
def on_close(event):
    sensor.stop_heizung() # Stopt die Heizung
    print("Program wurde ordungsgemäß geschlossen!")
    exit()
    
    
###########################################################################################
                                    ### ### ### BEGIN PREP ### ### ###
# Load config data
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Prepare Heizer
heizer.logging_on(False)
heizer_config = config['Heizer']['Schnittstelle']
sensor = heizer.HeizerPlatte(**heizer_config)
sensor.start_heizung()


### Prepare Pt Sensor
PTsensor = adafruit.Adafruit(name="Pt100", GPIO="D24",res=100,refres=430,wire=4,Vergleichssensor=True)
tSample = float(PTsensor.get_temperatur())
print(f"T_sensor = {round(tSample,2)}°C")


### Prepare Pyro1
RatioPyro = pyrometer_lumasense.PyrometerLumasense(config["IGAR-6-adv"], name="Pyro. (SW, Ratio)")
k = RatioPyro.k
RatioPyro.set_operationMode("2")

### Variabless
e_start = RatioPyro.emissivity
e_old  = e_start
e_next = e_start


tTargetList, tToleranceList, tTimeList, tStationaerList, tStationaerToleraceList, EmisSensorList, targetSensor = readRezept() # tTargetList ist die Liste der Zieltempraturen,# tTimeList ist die Liste der "Verweilzeiten"

path = createFiles()

# Plot Prep.
x = -1

plt.ion()
fig = plt.figure(figsize=(10,10)) # Fenster Größe des Diagrammes festlegen
fig.suptitle("Programm wird beendet, wenn Plot geschlossen wird!",fontsize=14, c="red") # Erzeugt eine Gesamt Überschrifft des Graphen

# Graph: Temperature
tSampleList     = [0]
tRatioList      = [0]
tRatioAvgList   = [0]
tMonoList       = [0]
tHeizplateList  = [0]
tTargetListPlot = [0]
EList           = [0]

ax1 = plt.subplot(211)

tSampleLine,    = ax1.plot(x, tSampleList, label='pt100 Probe',c="black")
tRatioLine,     = ax1.plot(x, tRatioList,c="red",alpha=0.4)
tRatioAvgLine,  = ax1.plot(x, tRatioAvgList, label=f"{RatioPyro.name} (Ratio_Avg)",c="red")
tMonoLine,      = ax1.plot(x, tMonoList, label=f"{RatioPyro.name} (Mono)",c="blue")
tHeizplateLine, = ax1.plot(x, tHeizplateList, label="Heizplatte",c="green")
tTargetLine,    = ax1.plot(x, tTargetListPlot, label=f"ZielTemperatur",c="orange")

plt.title("Temperatur über Zeit", fontsize=12)
plt.xlabel("Zeit [min]",fontsize=10)
plt.ylabel("Temperatur [°C]",fontsize=10)
plt.grid()
plt.legend()

# Graph: Emisivity
ax2 = plt.subplot(212)
ax2.set_ylim([0, 100])
ELine, = ax2.plot(x, tSampleList,c="black")
plt.title("Emissivität über Zeit", fontsize=12)
plt.xlabel("Zeit [min]",fontsize=10)
plt.ylabel("Emissivität [%]",fontsize=10)
plt.grid()

plt.tight_layout()
plt.show()
fig.canvas.mpl_connect('close_event', on_close) # program will be halted when ploted gets closed!

programStart = datetime.datetime.now().timestamp() # Saves starting time of script for automatic shutdown after 8 hours




###########################################################################################
                         ### ### ### BEGIN LOOP ### ### ###



for i in range(len(tTargetList)):
    
    # creates the current variables for temperature from settings.txt
    tTarget             = float(tTargetList[i])
    tTolerance          = float(tToleranceList[i])
    tTime               = float(tTimeList[i])
    tStationaer         = float(tStationaerList[i])
    tStationaerTolerace = float(tStationaerToleraceList[i])

    # change target-temperature to tTarget
    sensor.change_SollTemp(str(tTarget))
    ax1.set_ylim([20, tTarget+50])
    print(f"next temperature!\n  tTarget={tTarget}°C")
    
    for EmisSensor in EmisSensorList: # for every EmisSensor (in every temperature):
        
        # resets temporary lists
        tSampleListTemp = []
        tRatioListTemp  = []
        tMonoListTemp   = []
        EListTemp       = []
        
        data_points = 0 # saves how many datapoints are stored (in current measurement)
        
        # resets emisivity values
        e_old  = e_start
        e_next = e_start
        RatioPyro.set_emissivity(e_start/100)
        
        isInMessbereich = False

        # Main Loop (gets executed every second)
        while True:
            calcStart = datetime.datetime.now().timestamp()
            
            ### Generate Data
            tSample =    round(PTsensor.get_temperatur(),2)
            tMono, tRatio = RatioPyro.sampleMonoAndRatio()
            tHeizplate = round(sensor.get_istwert()     ,2)
            E = RatioPyro.emissivity
            
            ### Save data internaly (for plots, stationäermessung)
            tSampleList.append(tSample)
            tRatioList.append(tRatio)
            tRatioAvgList = rollingAvg(tRatioList,8)
            tMonoList.append(tMono)
            tHeizplateList.append(tHeizplate)
            tTargetListPlot.append(tTarget)
            EList.append(E)

            # Save data externaly
            with open(os.path.join(path,"data.csv"), "a") as f:
                f.write(f"{tTarget},{tHeizplate},{tSample},{tRatio},{tRatioAvgList[-1]},{tMono},{E}\n")
            
            # Check if targetSensor is in Target Area and stationary
            if isInMessbereich == True:
                pass # Skip if Messurement has already begun
            elif targetSensor == "ratio":
                isStationaer = stationaerPruefung(tRatioAvgList, tStationaer, tStationaerTolerace)
                if tRatio <= (tTarget + tTolerance) and tRatio >= (tTarget - tTolerance) and isStationaer == True:
                    isInMessbereich = True
                    print(f"Emissionsmessung beginnt!\n  EmisSensor={EmisSensor}")
                    
            elif targetSensor == "heizer":
                isStationaer = stationaerPruefung(tHeizplateList, tStationaer, tStationaerTolerace)
                if tHeizplate <= (tTarget + tTolerance) and tHeizplate >= (tTarget - tTolerance) and isStationaer == True:
                    isInMessbereich = True
                    print(f"Emissionsmessung beginnt!\n  EmisSensor={EmisSensor}")
                    
            elif targetSensor == "sample":
                isStationaer = stationaerPruefung(tSampleList, tStationaer, tStationaerTolerace)
                if tSample <= (tTarget + tTolerance) and tSample >= (tTarget - tTolerance) and isStationaer == True:
                    isInMessbereich = True
                    print(f"Emissionsmessung beginnt!\n  EmisSensor={EmisSensor}")
                    
            else:
                
                raise ValueError('targetSensor has to be "ratio", "heizer" or "sample".\n  look "settings.txt" up, for further information/fixing')
                    
            
            if isInMessbereich == True: # start measurement if true
                tSampleListTemp.append(tSample) # Speichert alle Temperaturen der aktuellen Messung
                tRatioListTemp.append(tRatio)   # Speichert alle Temperaturen der aktuellen Messung
                tMonoListTemp.append(tMono)     # Speichert alle Temperaturen der aktuellen Messung
                EListTemp.append(E)             # Speichert alle Emmisivitätwerte der aktuellen Messung
                
                # Passt die Emmisivität numerisch an.
                if EmisSensor =="pyro":
                    e_old, e_next = Emissions_Anpassung(tMono, tRatioAvgList[-1], e_old, e_next, 100, 5)
                elif EmisSensor =="pt":
                    e_old, e_next = Emissions_Anpassung(tMono, tSample, e_old, e_next, 100, 5)
                RatioPyro.set_emissivity(e_old/100)
                
                data_points = data_points + 1
                
                # Skip to next Step in Sequence
                if data_points >= tTime * 30:
                    # Speichert gerundete Werte der aktuellen Messung in measurement_data.csv datei
                    # Achtung: passiert erst am Schluss der akteullen Messung!
                    with open(os.path.join(path,"measurement_data.csv"), "a", encoding="utf-8") as f:
                        line = f"{k/100},{tTarget},{round(np.mean(tSampleListTemp),2)},{round(np.std(tSampleListTemp),2)},{round(np.mean(tRatioListTemp),2)},{round(np.std(tRatioListTemp),2)},{round(np.mean(tMonoListTemp),2)},{round(np.std(tMonoListTemp),2)},{E},{EmisSensor}\n"
                        f.write(line)
                    break # Beendet die aktuelle Messung und springt zur nächsten
        
        
            # Zeichnet die Linien
            x = np.linspace(-1,len(tSampleList),len(tSampleList))
            
            plotData(ax1, x, tSampleList,     tSampleLine   )
            plotData(ax1, x, tRatioList,      tRatioLine    )
            plotData(ax1, x, tRatioAvgList,   tRatioAvgLine )
            plotData(ax1, x, tMonoList,       tMonoLine     )
            plotData(ax1, x, tHeizplateList,  tHeizplateLine)
            plotData(ax1, x, tTargetListPlot, tTargetLine   )
            plotData(ax2, x, EList,           ELine         )
            
            # aktualiesiert den Graphen
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            calcEnd = datetime.datetime.now().timestamp() # speichert Zeit am Ende der Berechnung
            
            # adjust for calculation time so every step is exactly 1s appart
            calcTime = calcEnd - calcStart
            if calcTime < 2:
                time.sleep(2 - calcTime)
            else:
                print(f"Achtung: Berechnungszeit ist größer als der Messabstand!\n  calcTime={round(calcTime,2)}s")
                pass
            
            # Programm wid nach 12 Stunden vorzeitig beeendet und die Heizplatte deaktiviert.
            if programStart + 3600*12 < calcEnd:
                print("\nProgramm dauert zu lang und wird aus Sicherheitsgründen beendet!\n")
                plt.savefig(os.path.join(path,"plot.png"))
                plt.close() # Beendet das Skript in den der Plot geschlossen wird und die on_close() Funktion a
        
        plt.savefig(os.path.join(path,"plot.png")) # save plot after every Temperature

plt.savefig(os.path.join(path,"plot.png"))
plt.close() # Beendet das Skript in den der Plot geschlossen wird und die on_close() Funktion ausgelößt wird
