# main code for raspberry pi
import serial

# The interface config for serial port needs to be: login: No, serial port: Yes

# Baund rate needs to be the same on both ends, Arduino serial runs on 9600 so RasPi listens on 9600
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        print(f"Recieved: {line}")
