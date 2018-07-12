import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time
import numpy
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
u_nominal = 24#volt
k_motor = omega_from_sensor[7] / u_nominal
k_pwm = 4
print("kmotor",k_motor)
pwm_dt = []
Tm = 0.2 / 3

omega_real_ar = [];
omega_pressure = []

u=0.
omega_real = 0
d_omega_real = 0
omega_target = 5
omega_error = 0.
kp = 0.8#Tm / (Tz * k_motor)
ki = 8#2.9 #* numpy.sqrt(4)#1.0 / (Tz * k_motor)
kd = 0.0
kforward = 4
for i in range(120):
	if i > 60:
		pressure_i = 4
	else:
		pressure_i = 0
	omega -= pressure_i
	omega_real_ar.append(omega_real)
	omega_pressure.append(pressure_i)
	
	omega_error = omega_target - omega_real;
	
	integral += omega_error * dt
	diff = (omega_error - prev_omega_error) / dt
	prev_omega_error = omega_error
	u_dt.append(u)
	u = kp*omega_error + kd*diff + ki*integral + kforward * omega_target
	#u = 24.2/4
	d_omega = (dt / Tm) * (k_motor * u - omega)
	omega += d_omega
	betta = 14
	if omega < betta:
		omega_real = 0
	else:
		d_omega_real = (dt / 0.051) * (omega - omega_real - betta)
		omega_real += d_omega_real


plt.figure(0)
time = np.arange(0, 0.05 * 120, 0.05)
plt.plot(time, u_dt,label = "voltage")
plt.plot(time, omega_pressure,label = "pressure")
plt.plot(time, omega_real_ar,label = "omega real")

plt.legend()
pwm_dt = np.asarray(u_dt)
pwm_dt = pwm_dt*41
#plt.figure(1)
#time = np.arange(0, 0.05 * 120, 0.05)
#plt.plot(time, pwm_dt,label = "stm pwm")
#plt.plot(time, omega_from_sensor,'-o',label='omega_from_sensor (radian / sec)')


plt.legend()
plt.show()