# 導入需要模塊模塊
import RPi.GPIO as GPIO
from ultrasonic_CH import measure_dist
import RPi_I2C_driver as lcd1602
from time import sleep
import asyncio
import json
from azure.iot.device.aio import IoTHubDeviceClient

mylcd = lcd1602.lcd()
# 設置GPIO 17來驅動LED
GPIO_PIN=25
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)

def handle_twin(twin):
    if ('desired' in twin):
        print("收到雲端影子設備", twin)
        desired = twin['desired']
        if ('led' in desired):
            GPIO.output(GPIO_PIN, desired['led'])

async def main():
    # 建立Microsoft Azure连接
    conn_str = "HostName=PChanRaspiIoT.azure-devices.net;DeviceId=RaspPiDistance;SharedAccessKey=ZiP67PLKn/hyNpa3TdcM9jGVoYiVIb+Qg27ALKq3eDg="
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()
    
    last_dist = 0
    while True:
        dist = measure_dist()
        print ("測量距離 = %.1f cm" % dist)
        msg = 'Dist: ' + str(round(dist,2)) + ' cm'
        mylcd.lcd_clear()
        mylcd.lcd_display_string(msg, 1)
        await asyncio.sleep(0.5)
        dist = round(dist, 2)
        # MS Azure IoT Hub 
        diff = dist - last_dist
        if abs(diff) > last_dist*0.25:
            last_dist = dist
            data = {} 
            data['distance'] = dist                 
            json_body = json.dumps(data)
            print("設備發送消息到物聯網: ", json_body)
            await device_client.send_message(json_body)

            # handle the control of led from twin settings in the cloud
            twin = await device_client.get_twin()
            handle_twin(twin)
        await asyncio.sleep(1)
        GPIO.output(GPIO_PIN, 0)
    await device_client.disconnect()

if __name__ == '__main__':
    print('啟動程式...')
    try:
        asyncio.run(main())  

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        print("停止了測量...")
        print('完成程式...')
        mylcd.lcd_clear()
        GPIO.cleanup()

