import serial
from datetime import datetime
import xml.etree.ElementTree as ET

# Configurar el puerto serial
# Cambia 'COM3' por el puerto adecuado en tu sistema (puede ser diferente, como '/dev/ttyUSB0' en Linux)
ser = serial.Serial('COM5', 9600)

class Station:
    def __init__(self, id, name, sensors):
        self.id = id
        self.name = name
        self.sensors = sensors

class Sensor():
    def __init__(self, id, name, value, unity):
        self.id = id
        self.name = name
        self.value = value
        self.unity = unity
        self.time = datetime.now().isoformat()
    
class SensorTemperature(Sensor):
    def __init__(self, id, value):
        name = "temperatura"
        unity = "°C"
        super().__init__(
            id, 
            name,
            value,
            unity,
        )

class SensorHumidity(Sensor):
    def __init__(self, id, value):
        name = "humedad_relativa"
        unity = "%"
        super().__init__(
            id, 
            name,
            value,
            unity,
        )

class SensorPressure(Sensor):
    def __init__(self, id, value):
        name = "presion_atmosferica"
        unity = "kPa"
        super().__init__(
            id, 
            name,
            value,
            unity,
        )


def readDataSensors():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            t, p, h = map(float, line.split(','))

            print(f"t: {t}, p: {p}, h: {h}")

            # Creating sensors 
            sensor_t = SensorTemperature(1, t)
            sensor_h = SensorHumidity(2, h)
            sensor_p = SensorPressure(3, p)

            sensors = [
                sensor_t,
                sensor_h,
                sensor_p,
            ]

            station = Station(1, "Estacion Meteorológica A", sensors)

            writeXML(station)

        except KeyboardInterrupt:
            print("Terminando la lectura de datos.")
            break

def writeXML(station:Station):
    root = ET.Element("estacion")

    ide_element = ET.SubElement(root, "ide")
    ide_element.text = str(station.id)

    nameSt_element = ET.SubElement(root, "nombreEst")
    nameSt_element.text = station.name

    sensors_element = ET.SubElement(root, "sensores")

    for sensor in station.sensors:
        sensor_element = ET.Element("sensor")

        sensor_element_tmp = ET.SubElement(sensor_element, "id")
        sensor_element_tmp.text = str(sensor.id)

        sensor_element_tmp = ET.SubElement(sensor_element, "nombre")
        sensor_element_tmp.text = sensor.name

        sensor_element_tmp = ET.SubElement(sensor_element, "valor")
        sensor_element_tmp.text = str(sensor.value)

        sensor_element_tmp = ET.SubElement(sensor_element, "unidad")
        sensor_element_tmp.text = sensor.unity

        sensor_element_tmp = ET.SubElement(sensor_element, "tiempo")
        sensor_element_tmp.text = sensor.time

        sensors_element.append(sensor_element)

    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'

    with open("sensor_data.xml", "w", encoding='utf-8') as xml_file:
        xml_file.write(xml_declaration + "\n" + xml_str)

readDataSensors()

# Cerrar el puerto serial
ser.close()