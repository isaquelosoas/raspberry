"""Controle de LED com 4 modos de piscar.

Pressione o botão para alternar entre os modos:
0 - Pisca lento (1s on / 1s off)
1 - Pisca rápido (0.2s on / 0.2s off)
2 - Duplo: duas piscadas rápidas e pausa
3 - Fade (PWM) subindo e descendo o brilho

Conexões sugeridas (BCM):
- LED -> pino 18 (com resistor) -> GND
- Botão -> pino 17, outro terminal do botão ao GND; usa pull-up interno
"""

import time
import RPi.GPIO as GPIO

# Pinos (BCM)
LED_PIN = 18
BUTTON_PIN = 17

# Estado global do modo
current_mode = 0
last_press_time = 0.0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Detecta borda de descida (botão para GND)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=200)

def button_pressed(channel):
    """Callback chamado quando o botão é pressionado. Alterna o modo com debounce."""
    global current_mode, last_press_time
    now = time.time()
    # debounce simples adicional (segundos)
    if now - last_press_time < 0.25:
        return
    last_press_time = now
    current_mode = (current_mode + 1) % 4
    print(f"Modo alterado: {current_mode}")

def slow_blink():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1.0)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(1.0)

def fast_blink():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.2)

def double_blink():
    for _ in range(2):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.12)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.12)
    time.sleep(0.6)

def fade_blink():
    # Usa PWM para simular fade (0-100% duty cycle)
    pwm = GPIO.PWM(LED_PIN, 100)  # 100 Hz
    pwm.start(0)
    try:
        # Sobe
        for dc in range(0, 101, 4):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.02)
        # Desce
        for dc in range(100, -1, -4):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.02)
    finally:
        pwm.stop()

def main():
    setup()
    print("Iniciado. Pressione o botão para alternar modos (0-3). Ctrl+C para sair.")
    global current_mode
    try:
        while True:
            mode = current_mode
            if mode == 0:
                slow_blink()
            elif mode == 1:
                fast_blink()
            elif mode == 2:
                double_blink()
            elif mode == 3:
                fade_blink()
            # pequeno intervalo para permitir callback e reduzir uso de CPU
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Encerrando...")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()