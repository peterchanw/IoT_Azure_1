# 導入 GPIO 模塊庫
import RPi.GPIO as GPIO
from time import sleep

# 設置GPIO 17來驅動LED
GPIO_PIN=25
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)

for i in range(0,10):
    GPIO.output(GPIO_PIN,1)   # 打開引針17 – 3.3v
    sleep(1)                  # 睡1秒
    GPIO.output(GPIO_PIN,0)   # 關閉引針17 – 0v 
    sleep(1)                  # 睡1秒

# 清理所有 GPIO 端口
GPIO.cleanup()

