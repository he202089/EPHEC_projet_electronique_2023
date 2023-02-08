from machine import Pin, Timer, ADC

def init_leds():
    for i in range(4): # pin 0 à 3
         led = Pin(i)
         led.init(Pin.OUT) 

def set_leds(x):
    for i in range(4): # pin 0 à 3
         led = Pin(i)
         led.value(  (x>>i)%2 )       # la pin i prend la valeur du bit i de x
                                      # le reste de la division par 2 après décallage de i position vers la droite
                                      # (reste de la division par 2 == 1) <=> chiffre impair

def button_init():
    button = Pin(4)
    button.init(mode=Pin.IN,pull=Pin.PULL_UP)

def get_button():
    button = Pin(4)
    return button.value()
