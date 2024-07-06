import serial
import time
import random

def write_to_com5():
    with serial.Serial('COM5', 9600) as ser:
        while True:
            # sensor random values
            temperature = random.randint(1, 100)
            print(temperature)
            pressure = random.randint(1, 10)
            humidity = random.randint(1, 4)

            data = f"{temperature},{pressure},{humidity}\n"
            ser.write(data.encode())
            time.sleep(1)

write_to_com5()