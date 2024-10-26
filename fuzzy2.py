import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import sin, cos, pi

# 1. تعریف متغیرهای فازی ورودی
theta = ctrl.Antecedent(np.arange(-pi, pi, 0.01), 'theta')  # زاویه
theta_dot = ctrl.Antecedent(np.arange(-10, 10, 0.1), 'theta_dot')  # سرعت زاویه‌ای

# 2. تعریف متغیر فازی خروجی
force = ctrl.Consequent(np.arange(-50, 50, 0.1), 'force')

# 3. توابع عضویت برای ورودی و خروجی
# زاویه (theta)
theta['very_negative'] = fuzz.trimf(theta.universe, [-pi, -pi, -pi/2])
theta['negative'] = fuzz.trimf(theta.universe, [-pi, -pi/2, 0])
theta['zero'] = fuzz.trimf(theta.universe, [-pi/4, 0, pi/4])
theta['positive'] = fuzz.trimf(theta.universe, [0, pi/2, pi])
theta['very_positive'] = fuzz.trimf(theta.universe, [pi/2, pi, pi])

# سرعت زاویه‌ای (theta_dot)
theta_dot['very_negative'] = fuzz.trimf(theta_dot.universe, [-10, -10, -5])
theta_dot['negative'] = fuzz.trimf(theta_dot.universe, [-10, -5, 0])
theta_dot['zero'] = fuzz.trimf(theta_dot.universe, [-2.5, 0, 2.5])
theta_dot['positive'] = fuzz.trimf(theta_dot.universe, [0, 5, 10])
theta_dot['very_positive'] = fuzz.trimf(theta_dot.universe, [5, 10, 10])

# نیروی کنترلی (force)
force['very_negative'] = fuzz.trimf(force.universe, [-50, -50, -30])
force['negative_medium'] = fuzz.trimf(force.universe, [-50, -30, -10])
force['negative_weak'] = fuzz.trimf(force.universe, [-30, -10, 0])
force['zero'] = fuzz.trimf(force.universe, [-5, 0, 5])
force['positive_weak'] = fuzz.trimf(force.universe, [0, 10, 30])
force['positive_medium'] = fuzz.trimf(force.universe, [10, 30, 50])
force['very_positive'] = fuzz.trimf(force.universe, [30, 50, 50])

# 4. قوانین فازی برای کنترل
rule1 = ctrl.Rule(theta['very_negative'] & theta_dot['very_negative'], force['very_positive'])
rule2 = ctrl.Rule(theta['negative'] & theta_dot['very_negative'], force['positive_medium'])
rule3 = ctrl.Rule(theta['zero'] & theta_dot['very_negative'], force['positive_weak'])
rule4 = ctrl.Rule(theta['positive'] & theta_dot['very_negative'], force['zero'])
rule5 = ctrl.Rule(theta['very_positive'] & theta_dot['very_negative'], force['negative_weak'])
rule6 = ctrl.Rule(theta['very_negative'] & theta_dot['zero'], force['positive_weak'])
rule7 = ctrl.Rule(theta['negative'] & theta_dot['zero'], force['positive_weak'])
rule8 = ctrl.Rule(theta['zero'] & theta_dot['zero'], force['zero'])
rule9 = ctrl.Rule(theta['positive'] & theta_dot['zero'], force['negative_weak'])
rule10 = ctrl.Rule(theta['very_positive'] & theta_dot['zero'], force['very_negative'])

# 5. تعریف سیستم کنترل فازی
pendulum_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
pendulum_simulation = ctrl.ControlSystemSimulation(pendulum_ctrl)

# 6. پارامترهای فیزیکی
g = 9.8
L = 1.0
m = 0.5
dt = 0.05
Tmax = 10
t = np.arange(0.0, Tmax, dt)

# شرایط اولیه
theta_val = pi - 0.1
theta_dot_val = 0.0
state = [theta_val, theta_dot_val]

# 7. تابع شبیه‌سازی
def simulate_fuzzy_pendulum(state):
    theta_val, theta_dot_val = state
    pendulum_simulation.input['theta'] = theta_val
    pendulum_simulation.input['theta_dot'] = theta_dot_val
    pendulum_simulation.compute()
    u = pendulum_simulation.output['force']

    theta_ddot = (g * sin(theta_val) - u * cos(theta_val)) / L
    theta_dot_val += theta_ddot * dt
    theta_val += theta_dot_val * dt
    return theta_val, theta_dot_val

# 8. ذخیره نتایج برای انیمیشن
theta_vals = []
for _ in t:
    theta_val, theta_dot_val = simulate_fuzzy_pendulum(state)
    theta_vals.append(theta_val)
    state = [theta_val, theta_dot_val]

# 9. ایجاد انیمیشن
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
line, = ax.plot([], [], 'o-', lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = L * sin(theta_vals[i])
    y = -L * cos(theta_vals[i])
    line.set_data([0, x], [0, y])
    return line,

ani = animation.FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=dt*1000)
plt.show()
