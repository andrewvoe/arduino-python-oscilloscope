from collections import deque
import matplotlib.pyplot as plt
import serial
import time

N=500
SAMPLE_MS = 50     
ser = serial.Serial("COM9", 115200, timeout=1)  
time.sleep(2)
ser.reset_input_buffer()
buf= deque([0.0]*N, maxlen=N)

plt.ion()
fig, ax = plt.subplots()
                         
t = [i * SAMPLE_MS for i in range(N)]       

line, = ax.plot(t, list(buf))
ax.set_xlabel("Time (ms)")
ax.set_ylim(0,5)
ax.set_ylabel("Volts")
try:
    while True:
        raw = ser.readline().decode(errors="ignore").strip()

        try:
            value = int(raw)
        except ValueError:
            continue

        if not 0 <= value <= 1023:
            continue

        buf.append(value * 5.0 / 1023)
        line.set_ydata(list(buf))
        fig.canvas.draw_idle()
        fig.canvas.flush_events()

except KeyboardInterrupt:
    pass
finally:
    ser.close()