import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
g = 9.81        # gravity (m/s^2)
L_a = 0.5       # arm length (m)
L_p = 1.0       # pendulum length (m)
m_a = 0.5       # arm mass (kg)
m_p = 0.2       # pendulum mass (kg)
I_a = 0.02      # arm moment of inertia (kg.m^2)
I_p = 0.006     # pendulum moment of inertia (kg.m^2)
b_a = 0.01      # damping coefficient of the arm
b_p = 0.01      # damping coefficient of the pendulum

# Control parameters
Kp = 50
Kd = 10
target_alpha = np.pi  # Target angle for pendulum (upright position)

# System dynamics
def derivatives(t, s):
    theta, dtheta, alpha, dalpha = s

    # Calculate control input u
    u = -Kp * (alpha - target_alpha) - Kd * dalpha
    print(f"Control Input u at t={t:.2f}: {u}")

    # Pendulum dynamics
    d2alpha = (-m_p * g * L_p / 2 * np.sin(alpha) - b_p * dalpha - u) / I_p

    # Arm dynamics
    d2theta = (u - b_a * dtheta) / I_a

    return [dtheta, d2theta, dalpha, d2alpha]

# Initial conditions
theta0 = 0.0    # initial arm angle (rad)
dtheta0 = 0.0   # initial arm angular velocity (rad/s)
alpha0 = 0.1    # initial pendulum angle (rad)
dalpha0 = 0.0   # initial pendulum angular velocity (rad/s)
s0 = [theta0, dtheta0, alpha0, dalpha0]

# Time span
t_span = (0, 30)
t_eval = np.linspace(t_span[0], t_span[1], 600)

# Solve the system
sol = solve_ivp(derivatives, t_span, s0, t_eval=t_eval, method='RK45')

# Plotting results
theta = sol.y[0]
dtheta = sol.y[1]
alpha = sol.y[2]
dalpha = sol.y[3]
u_vals = -Kp * (alpha - target_alpha) - Kd * dalpha  # Calculated control signal

plt.figure(figsize=(12, 8))

# Pendulum angle
plt.subplot(3, 2, 1)
plt.plot(sol.t, alpha, label=r'Pendulum Angle ($\alpha$)')
plt.xlabel('Time (s)')
plt.ylabel(r'$\alpha$ (rad)')
plt.legend()

# Pendulum angular velocity
plt.subplot(3, 2, 2)
plt.plot(sol.t, dalpha, label=r'Pendulum Velocity ($\dot{\alpha}$)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel(r'$\dot{\alpha}$ (rad/s)')
plt.legend()

# Arm angle
plt.subplot(3, 2, 3)
plt.plot(sol.t, theta, label=r'Arm Angle ($\theta$)', color='green')
plt.xlabel('Time (s)')
plt.ylabel(r'$\theta$ (rad)')
plt.legend()

# Arm angular velocity
plt.subplot(3, 2, 4)
plt.plot(sol.t, dtheta, label=r'Arm Velocity ($\dot{\theta}$)', color='red')
plt.xlabel('Time (s)')
plt.ylabel(r'$\dot{\theta}$ (rad/s)')
plt.legend()

# Control input
plt.subplot(3, 2, 5)
plt.plot(sol.t, u_vals, label='Control Force (u)', color='purple')
plt.xlabel('Time (s)')
plt.ylabel('u (N)')
plt.legend()

plt.tight_layout()
plt.show()
