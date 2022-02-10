from microbit import *
from collections import OrderedDict
import radio
import random

radio.on()

imageBright = Image("00000:00000:00000:00000:00000")
#bildet som viser hvor nært man er til deltakere

brightness = 0
#hvor lyst bildet skal være
brightnessSteps = 6
#(blir forklart senere)

gameStart = False
#om spillet er i gang
hidersFound = OrderedDict([])
#en liste av deltakere som er funnet
hidersStrength = OrderedDict([])
#en liste av IDene til deltakerne og sine rssi-verdier (blir forklart nede)
rssiHistory = list()
#en liste av hvilke rssi har blitt brukt
historyLength = 5
#bestemmer hvor lang rssiHistory kan være

while True:
    received = radio.receive_full()
    #får meldingen (msg), signalstyrken (rssi) og tidsstempel
    if received:
        msg = str(received[0], 'UTF-8')
        msg = msg[3:len(msg)]
        #konverterer msg fra bytes til en string
        msgParts = msg.split(",")
        #lager en liste av deler i meldingen
        statusMsg = msgParts[0]
        #bokstaven foran Iden til deltakeren (status)
        idMsg = msgParts[1]
        #IDen til deltakeren
        rssi = received[1]
        #rssi / signalstyrke
    if not gameStart: #hvis spillet ikke løper
        display.show(str(len(hidersFound))) #vis hvor mange er registrert
        sleep(500) #vent i 0,5 sekunder
        if received and statusMsg == "S": #hvis statusen er "S" (registrering)
            hidersFound[idMsg] = False #blir IDen del av listen, den blir False fordi den ikke er funnet
        if button_a.was_pressed() and len(hidersFound) >= 1: #hvis a er trykket og det finnes minst en deltaker
            gameStart = True #begynner spillet
            radio.send("START")
    else:
        display.show(imageBright) #viser bildet
        if received:
            if statusMsg == "H": #hvis statusen er "H" (Hot)
                hidersStrength[idMsg] = rssi #velger rssien av idMsg i listen hidersStrength
                rssiMax = max(hidersStrength.values()) #rssiMax tar den høyeste verdien (rssien) av hidersStrength
                brightness = 9-(((-1)*rssiMax)-44)%brightnessSteps
                if (rssiMax > -44): #hvis rssiMax er større enn -44
                    brightness = 9 #blir brightness automatisk 9
                if (rssiMax < (-44 - brightnessSteps*9)): 
                    #hvis rssiMax er mindre enn -44 - brightnessSteps*9 (den maksimale verdien) 
                    brightness = 0 #blir brightness automatisk 0
                rssiHistory.append(brightness) #legger til verdien av brightness til listen av rssi-verdier
                if (len(rssiHistory) > historyLength): #hvis det finnes flere rssi-verdier i rssi-listen enn det maksimale:
                    rssiHistory.pop(0) #blir den første verdien fjernet fra listen
                rssiAverage = sum(rssiHistory) / len(rssiHistory) #den tar gjennomsnittet av rssiHistory
                imageBright.fill(int(rssiAverage)) #og endrer lysstyrken av bildet
            if idMsg in hidersFound and not statusMsg == "H": 
                #hvis den får en melding og IDen er del av hidersFound og statusen ikke er "H" (Hot)
                hidersFound[idMsg] = True #har den funnet spilleren
        hidersNotFound = dict(filter(lambda elem:elem[1] == False, hidersFound.items())) 
        #hvis ingen ikke er funnet (hvis alle er funnet)
        if len(hidersFound) >= 1 and len(hidersNotFound) == 0:
            #hvis det finnes mer enn en spiller og alle er funnet
            display.scroll("WIN!") #har søkeren vunnet
            sleep(2000)
            gameStart = False #spillet slutter
            radio.send("END")
            hidersFound.clear()
            hidersStrength.clear() 
            hidersNotFound.clear()
            rssiHistory.clear() #listene blir tømt
    sleep(300)
