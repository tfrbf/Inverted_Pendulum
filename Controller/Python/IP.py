import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from math import pi, sin, cos


g = 9.8   
L = 1.0   
m = 0.5   


dt = 0.05
Tmax = 30
t = np.arange(0.0, Tmax, dt)


Y = .0          # سرعت زاویه‌ای اولیه پاندول
th = pi - 0.1   # زاویه اولیه پاندول
x = .0          # موقعیت اولیه کالسکه
x0 = 0          # موقعیت هدف کالسکه
Z = -0.05       # سرعت اولیه کالسکه
k = 0.08        # ضریب کنترل انرژی

# ضرایب کنترل‌کننده
Kp_th = 50
Kd_th = 15
Kp_x = 3.1
Kd_x = 4.8

# وضعیت اولیه
state = np.array([th, Y, x, Z])
stabilizing = False

# متغیر برای ذخیره نیروی کنترلی
u_values = []

def energy(th, dth):
    return m * dth * L * dth * L / 2 + m * g * L * (cos(th) - 1)

def isControllable(th, dth):
    return th < pi/9 and abs(energy(th, dth)) < 0.5

def derivatives(state, t):
    global stabilizing
    ds = np.zeros_like(state)
    _th = state[0]
    _Y = state[1]  # سرعت زاویه‌ای
    _x = state[2]
    _Z = state[3]  # سرعت کالسکه

    # کنترل با توجه به وضعیت پایدارسازی
    if stabilizing or isControllable(_th, _Y):
        stabilizing = True
        u = Kp_th * _th + Kd_th * _Y + Kp_x * (_x - x0) + Kd_x * _Z
    else:
        E = energy(_th, _Y)
        u = k * E * _Y * cos(_th)

    u_values.append(u)  # ذخیره نیروی کنترلی

    ds[0] = state[1]
    ds[1] = (g * sin(_th) - u * cos(_th)) / L
    ds[2] = state[3]
    ds[3] = u

    return ds

# شبیه‌سازی
# شبیه‌سازی
print("Integrating...")
solution = integrate.odeint(derivatives, state, t)
print("Done")

# بررسی و تطبیق اندازه u_values و solution
if len(u_values) > len(t):
    u_values = u_values[:len(t)]
elif len(u_values) < len(t):
    t = t[:len(u_values)]

# استخراج مقادیر حالت‌ها از solution
ths = solution[:, 0]
Ys = solution[:, 1]
xs = solution[:, 2]
Zs = solution[:, 3]

# رسم نمودارهای پارامترهای کنترلی
plt.figure(figsize=(12, 10))

# نمودار زاویه پاندول
plt.subplot(3, 2, 1)
plt.plot(t, ths, label="Angle (θ)")
plt.xlabel("Time (s)")
plt.ylabel("θ (rad)")
plt.title("Pendulum Angle (θ) over Time")
plt.legend()

# نمودار سرعت زاویه‌ای
plt.subplot(3, 2, 2)
plt.plot(t, Ys, label="Angular Velocity (θ')", color='orange')
plt.xlabel("Time (s)")
plt.ylabel("θ' (rad/s)")
plt.title("Angular Velocity (θ') over Time")
plt.legend()

# نمودار موقعیت کالسکه
plt.subplot(3, 2, 3)
plt.plot(t, xs, label="Cart Position (x)", color='green')
plt.xlabel("Time (s)")
plt.ylabel("x (m)")
plt.title("Cart Position (x) over Time")
plt.legend()

# نمودار سرعت کالسکه
plt.subplot(3, 2, 4)
plt.plot(t, Zs, label="Cart Velocity (x')", color='red')
plt.xlabel("Time (s)")
plt.ylabel("x' (m/s)")
plt.title("Cart Velocity (x') over Time")
plt.legend()

# نمودار نیروی کنترلی
plt.subplot(3, 2, 5)
plt.plot(t, u_values, label="Control Force (u)", color='purple')
plt.xlabel("Time (s)")
plt.ylabel("u (N)")
plt.title("Control Force (u) over Time")
plt.legend()

plt.tight_layout()
plt.show()


# پارامترهای شبیه‌سازی گرافیکی پاندول
pxs = L * np.sin(ths) + xs
pys = L * np.cos(ths)

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
    thisx = [xs[i], pxs[i]]
    thisy = [0, pys[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i * dt))
    E = energy(ths[i], Ys[i])
    energy_text.set_text(energy_template % (E))
    patch.set_x(xs[i] - cart_width / 2)
    return line, time_text, energy_text, patch

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(solution)), interval=25, blit=True, init_func=init)

plt.show()
