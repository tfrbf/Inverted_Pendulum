import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# System Parameters
M = 1.0       # Mass of the cart (kg)
m = 0.1       # Mass of the pendulum (kg)
L = 0.5       # Length of the pendulum (m)
g = 9.81      # Gravitational acceleration (m/s^2)

# Control force function (0 for now)
def control_force(t):
    return 0.0  # No control initially

# Dynamics function
def inverted_pendulum_dynamics(t, y):
    x, x_dot, theta, theta_dot = y
    u = control_force(t)
    
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    denom = M + m * sin_theta**2
    
    theta_ddot = (g * sin_theta - cos_theta * (u + m * L * theta_dot**2 * sin_theta) / denom) / (L * (4/3 - (m * cos_theta**2) / denom))
    x_ddot = (u + m * L * (theta_dot**2 * sin_theta - theta_ddot * cos_theta)) / denom
    
    return [x_dot, x_ddot, theta_dot, theta_ddot]

# Initial conditions and time setup
y0 = [0, 0, np.pi + 0.1, 0]  # Slightly perturbed upright position
t_span = (0, 10)              # Simulate for 10 seconds
t_eval = np.linspace(0, 10, 300)  # Evaluation points for smoother animation

# Solve the system dynamics
sol = solve_ivp(inverted_pendulum_dynamics, t_span, y0, t_eval=t_eval)
x, x_dot, theta, theta_dot = sol.y  # Solution arrays

# Set up figure for animation
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(-2, 2)
ax.set_ylim(-1, 1.5)
ax.set_aspect('equal')
ax.grid()

# Create cart and pendulum lines
cart_width, cart_height = 0.4, 0.2
cart, = ax.plot([], [], 'blue', lw=4)
pendulum_line, = ax.plot([], [], 'orange', lw=2)

# Animation initialization function
def init():
    cart.set_data([], [])
    pendulum_line.set_data([], [])
    return cart, pendulum_line

# Update function for animation
def update(frame):
    # Cart position
    cart_x = x[frame] - cart_width / 2
    cart_y = 0  # Cart is on the ground level
    cart.set_data([cart_x, cart_x + cart_width], [cart_y, cart_y])
    
    # Pendulum position
    pendulum_x = x[frame] + L * np.sin(theta[frame])
    pendulum_y = -L * np.cos(theta[frame])
    pendulum_line.set_data([x[frame], pendulum_x], [0, pendulum_y])
    
    return cart, pendulum_line

# Create the animation
ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=30)

plt.show()
