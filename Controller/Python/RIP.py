# import libraries
import numpy as np
from scipy import optimize, constants
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from math import pi, sin, cos, pow


# system parameters
g   = constants.g      # gravity
L_p = 0.30             # pendulum length (m)
L_a = 0.38             # arm length (m)
m_p = 0.5              # pendulum mass (kg)
m_a = 0.6              # arm mass
I_a = m_p * pow(L_p,2) # Moment of inertia of the arm = 0.0025
I_p = m_a * pow(L_a,2) # Moment of inertia of the pendulum = 0.006
I_eq = I_a + I_p       # Total Inersia
mc  = 0.15             # Location of the center of mass of the pendulum

# simulation parameters
dt = 0.05
Tmax = 30
t = np.arange(0.0, Tmax, dt)

# initail condition
alpha = pi - 0.1      # pendulum initial angel
dtheta = .0           # pendulum initial speed
theta = .0            # arm initial angle
alpha_d = 0           # موقعیت هدف
dalpha= 0       # arm initial speed
k = 0.4               # energy control gain

# PID controller gains (Based on ACO, beta =1)
Kp_theta = 4.091
Kd_theta = 0.350
Kp_alpha = 0.125
Kd_alpha = 0.281

# creating initial state
state = np.array([theta, dtheta, alpha, dalpha])
stabilizing = False
u_values = []




def energy(dtheta, alpha,dalpha):
    return 0.5 * (I_eq * pow(dtheta,2) +
          (m_p * pow((L_a * dtheta - L_p * cos(alpha) * dalpha),2))+
           m_p * pow((L_p * sin(alpha) * dalpha),2) +
           I_eq * pow(alpha,2)) + m_p * g * L_p * cos(alpha)

def isControllable(alpha, dalpha):
    return alpha < pi/6 and abs(energy(alpha, dalpha)) < 0.5

def derivatives(state, t):
    global stabilizing
    ds = np.zeros_like(state)  # مشتقات حالت‌ها را در این آرایه ذخیره می‌کنیم
    _alpha  = state[0]  # زاویه پاندول
    _dalpha = state[1]  # سرعت زاویه‌ای پاندول
    _theta  = state[2]  # زاویه بازو
    _dtheta = state[3]  # سرعت زاویه‌ای بازو

    # سوئیچ کنترل بر اساس انرژی
    if stabilizing or isControllable(_theta, _dtheta):
        stabilizing = True
        # کنترلر تناسبی-مشتقی (PD) برای پایدارسازی
        u = Kp_theta * _theta + Kd_theta * _dtheta + Kp_alpha * (_alpha) + Kd_alpha * _dalpha
    else:
        # محاسبه انرژی و اعمال کنترلر بر اساس آن
        E = energy(_alpha, _dalpha, _dtheta)
        u = k * E * _dtheta * np.cos(_alpha)

    u_values.append(u)  # ذخیره مقادیر گشتاور کنترلی

    # معادلات حرکت
    ds[0] = _dalpha  # مشتق زاویه پاندول
    ds[1] = (g * np.sin(_alpha) - u * np.cos(_alpha)) / L_p  # شتاب زاویه‌ای پاندول
    ds[2] = _theta  # مشتق زاویه بازو
    ds[3] = u  # شتاب زاویه‌ای بازو بر اساس گشتاور کنترل

    return ds

# simulation
print("Integrating...")
solution = integrate.odeint(derivatives, state, t)
print("Done")

# array size check for solution and u
if len(u_values) > len(t):
    u_values = u_values[:len(t)]
elif len(u_values) < len(t):
    t = t[:len(u_values)]

# state variebles from ODE solution
alpha_s  = solution[:, 0]
dalpha_s = solution[:, 1]
theta_s  = solution[:, 2]
dtheta_s = solution[:, 3]


plt.figure(figsize=(12, 12))

# pendulum angle plot
plt.subplot(3, 2, 1)
plt.plot(t, alpha_s, label="Pendulum Angle (θ)")
#.xlabel("Time (s)")
plt.ylabel("θ (rad)")
#plt.title("Pendulum Angle (θ) over Time")
plt.grid()
plt.legend()

# pendulum velocity plot
plt.subplot(3, 2, 2)
plt.plot(t, dalpha_s, label="Pendulum Velocity (θ')", color='orange')
#plt.xlabel("Time (s)")
plt.ylabel("θ' (rad/s)")
#plt.title("Angular Velocity (θ') over Time")
plt.grid()
plt.legend()

# arm position plot
plt.subplot(3, 2, 3)
plt.plot(t, theta_s, label="Arm Angle (α)", color='green')
#plt.xlabel("Time (s)")
plt.ylabel("α (rad/s)")
#plt.title("Cart Position (x) over Time")
plt.grid()
plt.legend()

# arm velocity
plt.subplot(3, 2, 4)
plt.plot(t, dtheta_s, label="Arm Velocity (α')", color='red')
plt.xlabel("Time (s)")
plt.ylabel("α' (rad/s)")
#plt.title("Cart Velocity (x') over Time")
plt.legend()
plt.grid()

# control force plot
plt.subplot(3, 2, 5)
plt.plot(t, u_values, label="Control Force (u)", color='purple')
plt.xlabel("Time (s)")
plt.ylabel("u (N)")
#plt.title("Control Force (u) over Time")
plt.legend()
plt.grid()

# energy plot
plt.subplot(3, 2, 6)
plt.plot(t, energy, label="Energy (J)", color='black')
plt.xlabel("Time (s)")
plt.ylabel("u (N)")
#plt.title("Control Force (u) over Time")
plt.legend()
plt.grid()


plt.tight_layout()
plt.show()

'''
# پارامترهای شبیه‌سازی گرافیکی پاندول
pxs = L_p * np.sin(theta_s) + alpha_s
pys = L_p * np.cos(theta_s)

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1.5, 1.5), ylim=(-1.2, 1.2))
ax.set_aspect('equal')
ax.grid()

patch = ax.add_patch(Rectangle((0, 0), 0, 0, linewidth=1, edgecolor='k', facecolor='g'))
line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

energy_template = 'E = %.3f J'
energy_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)

cart_width = 0.3
cart_height = 0.2

def init():
    line.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    patch.set_xy((-cart_width / 2, -cart_height / 2))
    patch.set_width(cart_width)
    patch.set_height(cart_height)
    return line, time_text, energy_text, patch

def animate(i):
    thisx = [alpha_s[i], pxs[i]]
    thisy = [0, pys[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i * dt))
    E = energy(theta_s[i], dtheta_s[i])
    energy_text.set_text(energy_template % (E))
    patch.set_x(alpha_s[i] - cart_width / 2)
    return line, time_text, energy_text, patch

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(solution)), interval=25, blit=True, init_func=init)

plt.show()
'''