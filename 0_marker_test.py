import serial
import time

s = serial.Serial('COM4', 115200, timeout=1) 

marker_list = [50,51,70,71,3] # 50 for learning, 70 for fb,  51 for testing, 71 for testing
for i_marker in marker_list:
    s.write(bytes([i_marker]))
    time.sleep(0.05)
    s.write(bytes([0]))
    time.sleep(0.5)

s.write(bytes([0]))
s.write(bytes([0]))

s.close()
