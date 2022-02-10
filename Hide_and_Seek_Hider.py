from microbit import *
import radio
import random
import machine

radio.on()
#skrur på radio
radio.config(power=7)
#signalet har styrken 7, som er den høyeste

idHider = str(hash(str(machine.unique_id()))) + str(random.randint(1000, 9999))
#lager en unik ID for å skille mellom deltakerne
gameStart = False
#bestemmer om spiller er i gang
ready = False
#sier om deltakeren er klar til å begynne spillet
found = False
#om deltakeren har blitt funnet

while True:
    received = radio.receive()
    if gameStart: #hvis spillet er i gang
        if not found: #hvis den ikke har blitt funnet
            display.show("H") #H for hot
            radio.send("H,"+idHider) #sender den H, og IDen sin (H er statusen og den står for hot)
            sleep(500) #venter i 0,5 sek
        if button_a.was_pressed(): #hvis man trykker a-knappen
        #dette gjør søkeren etter de har funnet deltakeren
            sleep(1000) #vent i 1 sek
            radio.send("S,"+idHider) #sender S (statusen), og IDen sin
            found = True #den er funnet
            display.scroll("FOUND")
        if received: #hvis den får et signal
            if received == "END": #hvis signalet er "END"
                gameStart = False #slutter spillet
                found = False
                ready = False
    else: #hvis spillet ikke er i gang
        if not ready: #hvis den ikke er klar
            display.show("J") #J for join
            if button_a.was_pressed(): #hvis a knappen blir trykket
                radio.send("S,"+idHider) #sender den S (statusen), og IDen sin
                ready = True #den er klar og registrert hos leteren
        else: #hvis den er klar
            display.show("R") #R for ready
            if received == "START": #hvis den får startsignal
                gameStart = True #begynner spillet
    sleep(300)
        
                