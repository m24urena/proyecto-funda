from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms, sleep
import random
import network
import socket
import time

SSID = "okay"
PASSWORD = "12345678"
wlan = None
s = None
conn = None
addr = None

#Botones
boton1 = Pin(0, Pin.IN, Pin.PULL_UP)
boton2 = Pin(6, Pin.IN, Pin.PULL_UP)
boton3 = Pin(8, Pin.IN, Pin.PULL_UP)
boton4 = Pin(10, Pin.IN, Pin.PULL_UP)
botones = [boton1, boton2, boton3, boton4]

#Leds
led1 = Pin(1,Pin.OUT)
led1.value(0)
led2 = Pin(7,Pin.OUT)
led2.value(0)
led3 = Pin(22,Pin.OUT)
led3.value(0)
led4 = Pin(11,Pin.OUT)
led4.value(0)
leds = [led1, led2, led3, led4]

#7 segmentos
segmentos = [
    Pin(2, Pin.OUT),  # a
    Pin(21, Pin.OUT),  # b
    Pin(19, Pin.OUT),  # c
    Pin(18, Pin.OUT),  # d
    Pin(4, Pin.OUT),  # e
    Pin(3, Pin.OUT),  # f
    Pin(20, Pin.OUT)   # g
]

animacion_segmentos = [
    [0,1,1,1,1,1,1],
    [1,0,1,1,1,1,1],
    [1,1,0,1,1,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,0,1,1],
    [1,1,1,1,1,0,1]
]

buzzer = Pin(5, Pin.OUT)

sensor100 = Pin(12, Pin.IN, Pin.PULL_UP)
sensor50 = Pin(13, Pin.IN, Pin.PULL_UP)
sensor25 = Pin(15, Pin.IN, Pin.PULL_UP)

print("Presiona el botón para medir el tiempo...\n")
sleep_ms(1000)

juegos_ganados = 13
numeritos = [1, 1, 1, 1, 1, 1, 1]
cantidad_total = 0
cantidad_monedas = 0



def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConectado:", wlan.ifconfig())
    return wlan.ifconfig()[0]

def start_server(ip):
    global s, conn, addr
    s = socket.socket()
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    print("Conectado desde:", addr)


ip = connect_wifi()
start_server(ip)



def los_demas(num):
    numeros = []
    for i in range(4):
        if i != num:
            numeros.append(i)
    return numeros
            

def siete_segmentos(numeritos):
    for i in range(7):
        if numeritos[i]:
            segmentos[i].value(1)
        else:
            segmentos[i].value(0)

def animacion_ganar(cant):
    buzzer.on()
    sleep_ms(10)
    buzzer.off()
    sleep_ms(10)
    buzzer.on()
    sleep_ms(10)
    buzzer.off()
    for led in leds:
        led.on()
        sleep_ms(50)
        led.off()
    for chunche in animacion_segmentos:
        for i in range(7):
            segmentos[i].value(chunche[i])
            sleep_ms(10)
    siete_segmentos(cant)

def binario(num):
    b4 = num % 2
    num = num // 2
    b3 = num % 2
    num = num // 2
    b2 = num % 2
    num = num // 2
    b1 = num % 2
    A = (not b1 and not b2 and not b3 and b4) or (not b1 and b2 and not b3 and not b4) or (b1 and not b2 and b3 and b4) or (b1 and b2 and not b3 and b4)
    B = (not b1 and b2 and not b3 and b4) or (not b1 and b2 and b3 and not b4) or (b1 and not b2 and b3 and b4) or (b1 and b2 and not b3 and not b4) or (b1 and b2 and b3 and not b4) or (b1 and b2 and b3 and b4)
    C = (not b1 and not b2 and b3 and not b4) or (b1 and b2 and not b3 and not b4) or (b1 and b2 and b3 and not b4) or (b1 and b2 and b3 and b4)
    D = (not b1 and not b2 and not b3 and b4) or (not b1 and b2 and not b3 and not b4) or (not b1 and b2 and b3 and b4) or (b1 and not b2 and not b3 and b4) or (b1 and not b2 and b3 and not b4) or (b1 and b2 and b3 and b4)
    E = (not b1 and not b2 and not b3 and b4) or (not b1 and not b2 and b3 and b4) or (not b1 and b2 and not b3 and not b4) or (not b1 and b2 and not b3 and b4) or (not b1 and b2 and b3 and b4) or (b1 and not b2 and not b3 and b4)
    F = (not b1 and not b2 and not b3 and b4) or (not b1 and not b2 and b3 and not b4) or (not b1 and not b2 and b3 and b4) or (not b1 and b2 and b3 and b4) or (b1 and b2 and not b3 and b4)
    G = (not b1 and not b2 and not b3 and not b4) or (not b1 and not b2 and not b3 and b4) or (not b1 and b2 and b3 and b4) or (b1 and b2 and not b3 and not b4)
    return [int(A), int(B), int(C), int(D), int(E), int(F), int(G)]


perder = True
ganar = False
modo_adicional = False
patron = []


while modo_adicional:
    inicio = ticks_ms()
    fin = ticks_ms()
    while True and len(patron) > 0 and ticks_diff(fin, inicio) < 100/6:
        a, b, c = los_demas(patron[0])
        if not botones[patron[0]] and botones[a] and botones[b] and botones[c]:
            leds[patron[0]].on()
            sleep_ms(10)
            leds[patron[0]].off()
            del patron[0]
        elif botones[a] or botones[b] or not botones[a] or not botones[b] or not botones[c]:
            buzzer.on()
            sleep_ms(50)
            buzzer.off()
            break
        fin = ticks_ms()
    print('liiisto')
    conn.send('liiisto'.encode())
    if len(patron) == 0:
        animacion_ganar(binario(0))
        perder = False
        modo_adicional = False
    else:
        perder = True
        modo_adicional = False
    
            
        

while not perder and not modo_adicional:
    print('hola')
    
    buzzer.on()
    sleep_ms(10)
    buzzer.off()
    
    while juegos_ganados < 5:
        leds[n].on()
        fin1 = ticks_ms()

        if not botones[n].value() and ticks_diff(fin1, inicio) < 1000:
            leds[n].off()
            fin = ticks_ms()
            tiempo_ms = ticks_diff(fin, inicio)
            tiempo_hex = hex(tiempo_ms)[2:].upper()
            print(f"Tiempo transcurrido: {tiempo_ms} ms")
            print(f"En hexadecimal: {tiempo_hex} h\n")
            
            while not botones[n].value():
                sleep_ms(10)
            sleep_ms(1000)
            
            print("Volviendo a iniciar la cuenta...\n")

            juegos_ganados += 1
            siete_segmentos(binario(juegos_ganados))
            n = random.randint(0, 3)
            print(n)

            inicio = ticks_ms()

        elif ticks_diff(fin1, inicio) >= 1000:
            leds[n].off()
            siete_segmentos(binario(0))
            perder = True

    if juegos_ganados == 5:
        animacion_ganar(binario(juegos_ganados))
        for led in leds:
            led.off()
        inicio = ticks_ms()

    while juegos_ganados < 12:
        leds[n].on()
        fin1 = ticks_ms()

        if not botones[n].value() and ticks_diff(fin1, inicio) < 500:
            leds[n].off()
            fin = ticks_ms()
            tiempo_ms = ticks_diff(fin, inicio)
            tiempo_hex = hex(tiempo_ms)[2:].upper()
            print(f"Tiempo transcurrido: {tiempo_ms} ms")
            print(f"En hexadecimal: {tiempo_hex} h\n")
            
            while not botones[n].value():
                sleep_ms(10)
            sleep_ms(1000)
            
            print("Volviendo a iniciar la cuenta...\n")

            juegos_ganados += 1
            siete_segmentos(binario(juegos_ganados))
            n = random.randint(0, 3)
            print(n)

            inicio = ticks_ms()

        elif ticks_diff(fin1, inicio) >= 500:
            leds[n].off()
            siete_segmentos(binario(0))
            perder = True

    if juegos_ganados == 12:
        animacion_ganar(binario(juegos_ganados))
        for led in leds:
            led.off()
        inicio = ticks_ms()

    k = random.randint(1,4)
    m = random.randint(0,3)

    while juegos_ganados < 16:
        if k < 4:

            leds[n].on()
            fin1 = ticks_ms()

            if not botones[n].value() and ticks_diff(fin1, inicio) < 200:
                leds[n].off()
                fin = ticks_ms()
                tiempo_ms = ticks_diff(fin, inicio)
                tiempo_hex = hex(tiempo_ms)[2:].upper()
                print(f"Tiempo transcurrido: {tiempo_ms} ms")
                print(f"En hexadecimal: {tiempo_hex} h\n")
                
                while not botones[n].value():
                    sleep_ms(10)
                sleep_ms(1000)
                
                print("Volviendo a iniciar la cuenta...\n")

                juegos_ganados += 1
                
                if juegos_ganados == 16:
                    siete_segmentos(binario(0))
                else:
                    siete_segmentos(binario(juegos_ganados))
                    n = random.randint(0, 3)

                inicio = ticks_ms()

            elif ticks_diff(fin1, inicio) >= 200:
                leds[n].off()
                siete_segmentos(binario(0))
                perder = True
        
        else:

            leds[n].on()
            leds[m].on()

            fin1 = ticks_ms()

            if not botones[n].value() and not botones[m].value() and ticks_diff(fin1, inicio) < 200:
                leds[n].off()
                leds[m].off()
                fin = ticks_ms()
                tiempo_ms = ticks_diff(fin, inicio)
                tiempo_hex = hex(tiempo_ms)[2:].upper()
                print(f"Tiempo transcurrido entre los dos botones: {tiempo_ms} ms")
                print(f"En hexadecimal: {tiempo_hex} h\n")
                
                while not botones[n].value() and not botones[m].value():
                    sleep_ms(10)
                sleep_ms(1000)
                
                print("Volviendo a iniciar la cuenta...\n")

                juegos_ganados += 1
                
                if juegos_ganados == 16:
                    siete_segmentos(binario(0))
                else:
                    siete_segmentos(binario(juegos_ganados))
                    n = random.randint(0, 3)
                    m = random.randint(0, 3)

                inicio = ticks_ms()

            elif ticks_diff(fin1, inicio) >= 200:
                leds[n].off()
                leds[m].off()
                siete_segmentos(binario(0))
                perder = True
    
    
    if juegos_ganados >= 16:
        animacion_ganar(binario(0))
        animacion_ganar(binario(0))
        animacion_ganar(binario(0))
        perder = True   