import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time
#20Hz
period_from_sensor = np.array([65535,217,100,75,66,62,61,62,63,64,63,63,63,63,64,63,63,63,62,63,63,63,62,62,63,63,64,62,63,62,63,63,64,62,62,62,63,63,64,63,63,63,63,63,64,63,64,66,71,76,81,87,94,101,112,116,65535])
period_from_sensor = period_from_sensor.astype(float) / 10000
freq_of_rotation = 1.0 / period_from_sensor

omega_from_sensor = freq_of_rotation / 7.17  #radian per sec

integral = 0.0
diff = 0.0
omega_error = 0.0
prev_omega_error = 0.0
dt = 1.0/20#0.05

omega = 0.0;
d_omega = 0.0;
omega_dt = [];

u_dt = []
omega_freq_max = omega_from_sensor[7]
u_nominal = 15#volt
k_motor = omega_from_sensor[7] / u_nominal
print("kmotor",k_motor)

Tm = 0.4 / 3

omega_real = [];
omega_pressure = []

u=0.

omega_target = 21.
omega_error = 0.
kp = 0.01#Tm / (Tz * k_motor)
ki = 2.9#1.0 / (Tz * k_motor)
kd = 0.#15
for i in range(120):
	if i > 60:
		pressure_i = 1
	else:
		pressure_i = 0
	omega -= pressure_i
	omega_real.append(omega)
	omega_pressure.append(pressure_i)
	
	omega_error = omega_target - omega;
	integral += omega_error * dt
	diff = (omega_error - prev_omega_error) / dt
	prev_omega_error = omega_error
	u_dt.append(u)
	u = kp*omega_error + kd*diff + ki*integral
	d_omega = (dt / Tm) * (k_motor * u - omega)
	omega += d_omega


plt.figure(0)
time = np.arange(0, 0.05 * 120, 0.05)
plt.plot(time, u_dt,label = "voltage")
plt.plot(time, omega_pressure*1,label = "pressure")
plt.plot(time, omega_real,label = "omega real")

plt.legend()

plt.figure(1)
time = np.arange(0, 0.05 * len(omega_from_sensor), 0.05)
plt.plot(time, omega_from_sensor,'-o',label='omega_from_sensor (radian / sec)')


plt.legend()
plt.show()