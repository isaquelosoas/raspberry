"""Controle de semáforo com 3 LEDs.

Pressione o botão para alternar entre as cores:
Vermelho -> Verde -> Amarelo -> Vermelho

Conexões sugeridas (BCM):
- LED Vermelho -> pino 18 (com resistor) -> GND
- LED Verde -> pino 23 (com resistor) -> GND
- LED Amarelo -> pino 24 (com resistor) -> GND
- Botão -> pino 17, outro terminal do botão ao GND; usa pull-up interno
"""

import time
import RPi.GPIO as GPIO

# Pinos (BCM)
LED_RED = 18
LED_GREEN = 23
LED_YELLOW = 25
BUTTON_PIN = 17

# Estados do semáforo: 0 = Vermelho, 1 = Verde, 2 = Amarelo
traffic_light_state = 0
last_press_time = 0.0

# Cores dos estados
COLORS = {
    0: "Vermelho",
    1: "Verde",
    2: "Amarelo"
}

def setup():
    """Configura os pinos GPIO."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Apaga todos os LEDs inicialmente
    GPIO.output(LED_RED, GPIO.LOW)
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_YELLOW, GPIO.LOW)
    
    # Detecta borda de descida (botão para GND)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=200)

def button_pressed(channel):
    """Callback chamado quando o botão é pressionado. Alterna a cor do semáforo."""
    global traffic_light_state, last_press_time
    now = time.time()
    # debounce simples adicional (segundos)
    if now - last_press_time < 0.25:
        return
    last_press_time = now
    traffic_light_state = (traffic_light_state + 1) % 3
    color_name = COLORS[traffic_light_state]
    print(f"Semáforo alterado para: {color_name}")

def turn_off_all_leds():
    """Apaga todos os LEDs."""
    GPIO.output(LED_RED, GPIO.LOW)
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_YELLOW, GPIO.LOW)

def set_traffic_light_color():
    """Define a cor do semáforo de acordo com o estado."""
    turn_off_all_leds()
    
    if traffic_light_state == 0:  # Vermelho
        GPIO.output(LED_RED, GPIO.HIGH)
    elif traffic_light_state == 1:  # Verde
        GPIO.output(LED_GREEN, GPIO.HIGH)
    elif traffic_light_state == 2:  # Amarelo
        GPIO.output(LED_YELLOW, GPIO.HIGH)

def main():
    """Loop principal."""
    setup()
    print("Semáforo iniciado. Pressione o botão para alternar cores. Ctrl+C para sair.")
    
    try:
        while True:
            set_traffic_light_color()
            # pequeno intervalo para permitir callback e reduzir uso de CPU
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Encerrando...")
    finally:
        turn_off_all_leds()
        GPIO.cleanup()

if __name__ == '__main__':
    main()