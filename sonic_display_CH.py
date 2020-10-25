# 導入需要模塊模塊
import RPi.GPIO as GPIO
from ultrasonic_CH import distance
import RPi_I2C_driver as lcd1602
from time import sleep
import asyncio

mylcd = lcd1602.lcd()   

if __name__ == '__main__':
    print('啟動程式...')
    try:
        while True:
            dist = asyncio.run(distance())
            print ("測量距離 = %.1f cm" % dist)
            msg = 'Dist: ' + str(round(dist,2)) + ' cm'
            mylcd.lcd_clear()
            mylcd.lcd_display_string(msg, 1)
            sleep(0.5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        print("停止了測量...")
        print('完成程式...')
        mylcd.lcd_clear()
        GPIO.cleanup()

