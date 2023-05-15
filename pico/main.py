from machine import Pin, UART
import utime



soundspeed = 0.0343
DOT = False

ALARM_OPERATOR = "<" # can be "<" or ">"
BLINK_DELAY = 0.01

ALARM_LIMIT = 20
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


def process_serial_commands():
    #Doesn't work
    new_limit = ALARM_LIMIT
    if uart.any():
        command = uart.read()
        if command.startswith("L"):
            new_limit = int(command[1:])
    return new_limit
            
trigger = Pin(0, Pin.OUT)
echo = Pin(1, Pin.IN)

led_green = Pin(5, Pin.OUT)
led_red = Pin(9, Pin.OUT)

pin_one = Pin(19, Pin.OUT) # MSB
pin_two = Pin(26, Pin.OUT)
pin_three = Pin(27, Pin.OUT)
pin_four = Pin(18, Pin.OUT) # LSB

dizainePin = Pin(14, Pin.OUT)
unitePin = Pin(16, Pin.OUT)
pin_dot = Pin(15, Pin.OUT)

pin_list = [pin_one, pin_two, pin_three, pin_four]


def reset_pin():
    pin_one.value(0)
    pin_two.value(0)
    pin_three.value(0)
    pin_four.value(0)
    pin_dot.value(1)
    led_green.value(0)
    led_red.value(0)

def launchSound():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()

            
def ultra():
   launchSound()
   signaloff = 0
   signalon = 0

   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()

   timepassed = signalon - signaloff
   distance = (timepassed * soundspeed) / 2
   print("L'objet est perçu à ",distance,"cm", "la limite de l'alarm est à", ALARM_LIMIT)
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

def decimalToBin(DECIMAL):
    BINARY = to_four_bits(bin(DECIMAL).split('b')[1])
    BINARY_LIST = str(BINARY)

    return BINARY_LIST

def check_leds(distance):
    if ALARM_OPERATOR == "<":
        if distance < ALARM_LIMIT:
            led_red.value(0)
            led_green.value(1)
        elif distance >= ALARM_LIMIT:
            led_red.value(1)
            led_green.value(0)
    elif ALARM_OPERATOR == ">":
        if distance > ALARM_LIMIT:
            led_red.value(0)
            led_green.value(1)
        elif distance <= ALARM_LIMIT:
            led_red.value(1)
            led_green.value(0)


# Boucle principale
while 1:
    distance = ultra()
    check_leds(distance)

    
    if distance >= 100:
        DOT = True
    elif distance < 100:
        DOT = False

    list_mesure = DecimalToResult(distance)
    # Dizaine
    bin_diz = decimalToBin(list_mesure[0])
    # Unité 
    bin_unit = decimalToBin(list_mesure[1])

    # Allume Dizaine
    reset_pin()
    dizainePin.value(1)
    unitePin.value(1)
    if DOT:
        pin_dot.value(0)

    for i, x in enumerate(pin_list):
        if int(bin_diz[i]) == 1:
            x.value(1)
    
    utime.sleep(BLINK_DELAY)
    

    # Allume unité
    reset_pin()
    dizainePin.value(0)
    unitePin.value(1)
    for i, x in enumerate(pin_list):
        if int(bin_unit[i]) == 1:
            x.value(1)

    utime.sleep(BLINK_DELAY)
    ALARM_LIMIT = process_serial_commands()

    

