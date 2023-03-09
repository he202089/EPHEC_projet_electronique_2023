from machine import Pin
import utime
import _thread

TOGGLE = True
soundspeed = 0.0343
DOT = False
ALARM_LIMIT = 20
ALARM_OPERATOR = "<" # can be "<" or ">"
DISTANCE = 0
BLINK_DELAY = 0.5

trigger = Pin(0, Pin.OUT)
echo = Pin(1, Pin.IN)

led_green = Pin(5, Pin.OUT)
led_red = Pin(9, Pin.OUT)

pin_one = Pin(18, Pin.OUT) # MSB
pin_two = Pin(10, Pin.OUT)
pin_three = Pin(11, Pin.OUT)
pin_four = Pin(17, Pin.OUT) # LSB

dizainePin = Pin(14, Pin.OUT)
unitePin = Pin(16, Pin.OUT)


pin_list = [pin_one, pin_two, pin_three, pin_four]
pin_dot = Pin(15, Pin.OUT)


def launchSound():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()

            

def ultra():
   launchSound()

   while echo.value() == 0:
       """ Track the time when we launch the trigger"""
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       """ Track the time when the trigger is back"""
       signalon = utime.ticks_us()

   timepassed = signalon - signaloff
   distance = (timepassed * soundspeed) / 2
   print("L'objet est perçu à ",distance,"cm")
   return distance

def DecimalToResult(decimal):
    decimal = int(decimal)
    list_output=[]
    while decimal > 0:
        list_output.append(decimal%10)
        decimal /= 10
        decimal = int(decimal)

    list_output.reverse()
    while len(list_output) < 2:
        list_output.insert(0,0)
    while(len(list_output) > 2):
        list_output.pop(-1)
    
    return list_output
        
    
def to_four_bits(binary):
    if len(binary) == 0:
        return '0000'
    elif len(binary) == 1:
        return '000' + binary
    elif len(binary) == 2:
        return '00' + binary
    elif len(binary) == 3:
        return '0' + binary
    else:
        return binary

def decimalToOutPut(DECIMAL):
    BINARY = to_four_bits(bin(DECIMAL).split('b')[1])
    BINARY_LIST = str(BINARY)

    return (BINARY_LIST)

#dizaine
test_bin_diz = decimalToOutPut(8)

#unité 
test_bin_unit = decimalToOutPut(9)

def refresh(pint_list):
    for x in (pin_list):
        
        x.value(1)
    

# LEDS
def check_leds():
    while True:
        if ALARM_OPERATOR == "<":
            if DISTANCE < ALARM_LIMIT:
                if led_red.value == 0:
                    led_red.value(1)
                else:
                    led_red.value(0)

                led_green.value(0)
                utime.sleep(BLINK_DELAY)
            else:
                led_red.value(0)
                led_green.value(1)
        elif ALARM_OPERATOR == ">":
            if DISTANCE > ALARM_LIMIT:
                if led_red.value == 0:
                    led_red.value(1)
                else:
                    led_red.value(0)

                led_green.value(0)
                utime.sleep(BLINK_DELAY)
            else:
                led_red.value(0)
                led_green.value(1)
        else:
            led_red.value(1)
            led_green.value(0)

def main():
    #_thread.start_new_thread(check_leds, ())
    pass

#main()


def affichage():
    # Allumé dizaine
    unitePin.value(1)
    dizainePin.value(0)
    for i, x in enumerate(pin_list):
        if int(test_bin_diz[i]) == 1:
            x.value(0)
            
    if DOT:
        pin_dot.value(0)  
   
    refresh(pin_list)
    utime.sleep(1)
    pin_dot.value(0)

    # Allume unité
    unitePin.value(0)
    dizainePin.value(1)
    for i, x in enumerate(pin_list):
        if int(test_bin_unit[i]) == 1:
            x.value(0)
    
    refresh(pin_list)

# Boucle principale
while 1:
    refresh(pin_list)
    distance = ultra()

    if distance >= 100:
        DOT = True

    list_mesure = DecimalToResult(distance)
    # Dizaine
    test_bin_diz = decimalToOutPut(list_mesure[0])
    # Unité 
    test_bin_unit = decimalToOutPut(list_mesure[1])
   
    newMesure = False
    timeSpend = 0
    #startAffichage = utime.ticks_us()
    
    unitePin.value(1)
    dizainePin.value(0)
    for i, x in enumerate(pin_list):
        if int(test_bin_diz[i]) == 1:
            x.value(0)
            
    if DOT:
        pin_dot.value(0)  
   
    
    utime.sleep(0.5)
    pin_dot.value(0)

    # Allume unité
    unitePin.value(0)
    dizainePin.value(1)
    for i, x in enumerate(pin_list):
        if int(test_bin_unit[i]) == 1:
            x.value(0)
    
    utime.sleep(0.5)
    #while not newMesure:
#
     #   affichage()

        #timeIn = utime.ticks_us()
        #timeSpend = timeIn - startAffichage

        #if timeSpend > 1000000:
            #newMesure = True
