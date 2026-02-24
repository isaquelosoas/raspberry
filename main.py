# Gere algo para leds usando o Raspberry Pi e a biblioteca GPIO. O código deve acender um LED conectado ao pino 18 por 1 segundo, depois apagá-lo por 1 segundo, e repetir esse ciclo 5 vezes.```python
import RPi.GPIO as GPIO
import time 
# Configuração do modo de numeração dos pinos
GPIO.setmode(GPIO.BCM)
# Configuração do pino 18 como saída
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)
try:
    for _ in range(5):
        print("Acendendo o LED...")
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED aceso.")
        time.sleep(1)  # Aguarda 1 segundo
        GPIO.output(LED_PIN, GPIO.LOW)   # Apaga o LED
        print("LED apagado.")
        time.sleep(1)  # Aguarda 1 segundo
finally:    
    GPIO.cleanup()  # Limpa a configuração dos pinos
