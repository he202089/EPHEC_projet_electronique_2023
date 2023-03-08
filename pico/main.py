from machine import Pin
import utime

TOGGLE = True
soundspeed = 0.0343
DOT = False
ALARM_LIMIT = 20
ALARM_OPERATOR = "<" # can be "<" or ">"
DISTANCE = 0
BLINK_DELAY = 0.5

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

led_green = Pin(6, Pin.OUT)
led_red = Pin(11, Pin.OUT)

pin_one = Pin(32, Pin.OUT) # MSB
pin_two = Pin(31, Pin.OUT)
pin_three = Pin(26, Pin.OUT)
pin_four = Pin(24, Pin.OUT) # LSB
pin_list = [pin_one, pin_two, pin_three, pin_four]
pin_dot = Pin(21, Pin.OUT)

listLedBinaire = [Bin1,Bin2,Bin3,Bin4]


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
    int(decimal)
    list_output=[]
    affichage = [0,0]
    while decimal > 0:
        list_output.append(decimal%10)
        decimal /= 10
        decimal = int(decimal)
        
    
    affichage[0] = list_output[0]
    affichage[1] = list_output[1]
    
    return affichage
    
        
 
    

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
        
         x.value(0)
    

# Boucle des LEDS
while 1:
    if ALARM_OPERATOR == "<":
        if distance < ALARM_LIMIT:
            if led_red.value == 0:
                led_red.value(1)
            else:
                led_red.value(0)

            led_green.value(0)
            time.sleep(BLINK_DELAY)
        else:
            led_red.value(0)
            led_green.value(1)
    elif ALARM_OPERATOR == ">":
        if distance > ALARM_LIMIT:
            if led_red.value == 0:
                led_red.value(1)
            else:
                led_red.value(0)

            led_green.value(0)
            time.sleep(BLINK_DELAY)
        else:
            led_red.value(0)
            led_green.value(1)
    else:
        led_red.value(1)
        led_green.value(0)
    
# Boucle principale
while 1:
   DISTANCE = ultra()

   if DISTANCE >= 100:
    DOT = True
   list_mesure = DecimalToResult(DISTANCE)
   test_bin_diz = decimalToOutPut(list_mesure[0])

   #unité 
   test_bin_unit = decimalToOutPut(list_mesure[1])
   
   
   #Allumé dizaine
   for i, x in enumerate(pin_list):
        if int(test_bin_diz[i]) == 1:
            x.value(1)
            
   if DOT:
    pin_dot.value(1)  
   
   utime.sleep(0.05)
   refresh(pin_list)
   pin_dot.value(0)

   #Allume unité
   for i, x in enumerate(pin_list):
        if int(test_bin_unit[i]) == 1:
            x.value(1)
    refresh(pin_list)