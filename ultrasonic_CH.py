# 導入需要模塊模塊
import RPi.GPIO as GPIO
import time
import asyncio
 
# 引脚用GPIO位置設置
GPIO.setmode(GPIO.BCM)
 
# 引脚GPIO設置
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)   # Trig 引脚輸出
GPIO.setup(GPIO_ECHO, GPIO.IN)       # Echo 引脚輸出
 
async def distance():
    # 準備「啟動引脚」以40kHz的頻率發射8個週期的超聲脈衝並將其設置為低電平1秒
    GPIO.output(GPIO_TRIGGER, False) 
    await asyncio.sleep(1)
    GPIO.output(GPIO_TRIGGER, True)
    # 設置「啟動引脚」於高電平0.01微秒
    await asyncio.sleep(0.00001)
    # 設置「啟動引脚」於低電平
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # 記錄超聲波開始時間
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # 記錄超聲波超反射時間
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # 算計開始和到達時間差
    TimeElapsed = StopTime - StartTime
    # 乘以音速（34300 cm / s）倍增，然後除以2，因為要計來回距離
    distance = (TimeElapsed * 34300) / 2
    return distance
 
def measure_dist():
    # 準備「啟動引脚」以40kHz的頻率發射8個週期的超聲脈衝並將其設置為低電平1秒
    GPIO.output(GPIO_TRIGGER, False) 
    time.sleep(1)
    GPIO.output(GPIO_TRIGGER, True)
    # 設置「啟動引脚」於高電平0.01微秒
    time.sleep(0.00001)
    # 設置「啟動引脚」於低電平
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # 記錄超聲波開始時間
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # 記錄超聲波超反射時間
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # 算計開始和到達時間差
    TimeElapsed = StopTime - StartTime
    # 乘以音速（34300 cm / s）倍增，然後除以2，因為要計來回距離
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    print('啟動程式...')
    try:
        while True:
            dist = asyncio.run(distance())
            print ("測量距離 = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        print("停止了測量...")
        print('完成程式...')
        GPIO.cleanup()



        
