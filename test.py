from machine import Pin
import utime



pin_one = Pin(18, Pin.OUT) # MSB
pin_two = Pin(27, Pin.OUT)
pin_three = Pin(26, Pin.OUT)
pin_four = Pin(19, Pin.OUT) # LSB

led_green = Pin(5, Pin.OUT)
led_red = Pin(9, Pin.OUT)

dizainePin = Pin(14, Pin.OUT)
unitePin = Pin(16, Pin.OUT)
pin_dot = Pin(15, Pin.OUT)

# dizainePin.value(0)ETEINT LES DIZAINES
# unitePin.value(1) ETEINT LES UNITE

dizainePin.value(1) 
unitePin.value(0)
while 1:

    led_green.value(1)
    led_red.value(1)
    
    pin_dot.value(1) # dot off
    
    pin_one.value(1)
    pin_two.value(0)
    pin_three.value(1)
    pin_four.value(0)
    
