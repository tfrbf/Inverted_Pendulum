import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from math import pi, sin, cos

# Physical constants
g = 9.8      # Gravity (m/s^2)
L = 0.5      # Pendulum length (m)
m = 0.2      # Pendulum mass (kg)
I = 0.006    # Pendulum moment of inertia (kg*m^2)
M = 0.5      # Arm mass (kg)
b = 0.1      # Damping coefficient (N*m*s)

# Control parameters
Kp_phi = 50   # Proportional gain for arm
Kd_phi = 15   # Derivative gain for arm
Kp_th = 50    # Proportional gain for pendulum
Kd_th = 15    # Derivative gain for pendulum
swing_up_gain = 5

# Initial conditions
theta = pi - 0.1   # Initial pendulum angle (rad)
dtheta = 0.0       # Initial angular velocity of pendulum (rad/s)
phi = 0.0          # Initial arm angle (rad)
dphi = 0.0         # Initial angular velocity of arm (rad/s)

state = np.array([theta, dtheta, phi, dphi])
stabilizing = False

# Simulation parameters
dt = 0.01
Tmax = 30
t = np.arange(0.0, Tmax, dt)

# Control torque history
torque_values = []

def energy(theta, dtheta):
    """Energy of the pendulum."""
    return 0.5 * I * dtheta**2 + m * g * L * (1 - cos(theta))

def is_controllable(theta, dtheta):
    """Checks if the pendulum is close to the upright position."""
    return abs(theta) < pi / 9 and abs(energy(theta, dtheta)) < 0.5

def derivatives(state, t):
    """Derivatives for the rotary inverted pendulum system."""
    global stabilizing
    theta, dtheta, phi, dphi = state
    dstate = np.zeros_like(state)

    # Control logic
    if stabilizing or is_controllable(theta, dtheta):
        stabilizing = True
        # Stabilization using PID
        torque = -Kp_phi * phi - Kd_phi * dphi - Kp_th * theta - Kd_th * dtheta
    else:
        # Swing-up control
        E = energy(theta, dtheta)
        torque = swing_up_gain * E * dtheta * cos(theta)
    
    torque_values.append(torque)

    # Equations of motion
    dstate[0] = dtheta
    dstate[1] = (m * g * L * sin(theta) - torque * cos(theta)) / I
    dstate[2] = dphi
    dstate[3] = torque / M - b * dphi

    return dstate

# Simulate the system
solution = integrate.odeint(derivatives, state, t)

# Extract state variables
theta_vals = solution[:, 0]
dtheta_vals = solution[:, 1]
phi_vals = solution[:, 2]
dphi_vals = solution[:, 3]

# Adjust torque values to match the time array length
torque_values = torque_values[:len(t)]

# Plot results
plt.figure(figsize=(12, 10))

# Pendulum angle
plt.subplot(3, 2, 1)
plt.plot(t, theta_vals, label="Pendulum Angle (θ)")
plt.xlabel("Time (s)")
plt.ylabel("θ (rad)")
plt.title("Pendulum Angle over Time")
plt.legend()

# Pendulum angular velocity
plt.subplot(3, 2, 2)
plt.plot(t, dtheta_vals, label="Pendulum Angular Velocity (θ')", color='orange')
plt.xlabel("Time (s)")
plt.ylabel("θ' (rad/s)")
plt.title("Pendulum Angular Velocity over Time")
plt.legend()

# Arm angle
plt.subplot(3, 2, 3)
plt.plot(t, phi_vals, label="Arm Angle (φ)", color='green')
plt.xlabel("Time (s)")
plt.ylabel("φ (rad)")
plt.title("Arm Angle over Time")
plt.legend()

# Arm angular velocity
plt.subplot(3, 2, 4)
plt.plot(t, dphi_vals, label="Arm Angular Velocity (φ')", color='red')
plt.xlabel("Time (s)")
plt.ylabel("φ' (rad/s)")
plt.title("Arm Angular Velocity over Time")
plt.legend()

# Control torque
plt.subplot(3, 2, 5)
plt.plot(t, torque_values, label="Control Torque (τ)", color='purple')
plt.xlabel("Time (s)")
plt.ylabel("τ (N*m)")
plt.title("Control Torque over Time")
plt.legend()

plt.tight_layout()
plt.show()

# Animation
fig, ax = plt.subplots()
ax.set_xlim(-1.0, 1.0)
ax.set_ylim(-1.0, 1.0)
line, = ax.plot([], [], 'o-', lw=2)
time_template = 'Time = %.1f s'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

def animate(i):
    x_pendulum = L * sin(theta_vals[i])
    y_pendulum = -L * cos(theta_vals[i])
    x_arm = 0
    y_arm = 0
    line.set_data([x_arm, x_pendulum], [y_arm, y_pendulum])
    time_text.set_text(time_template % (i * dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=dt * 1000, init_func=init, blit=True)
plt.show()
