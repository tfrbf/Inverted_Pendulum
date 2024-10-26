import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# پارامترهای پاندول معکوس
m_p = 0.2  # جرم پاندول (kg)
l_p = 0.5  # طول پاندول (m)
g = 9.81   # شتاب گرانش (m/s^2)
I_p = m_p * l_p**2 / 3  # اینرسی پاندول
I_a = 0.02  # اینرسی محور

# تعریف توابع عضویت و سیستم فازی
alpha = ctrl.Antecedent(np.linspace(-np.pi/2, np.pi/2, 100), 'alpha')
alpha_dot = ctrl.Antecedent(np.linspace(-10, 10, 100), 'alpha_dot')
tau = ctrl.Consequent(np.linspace(-10, 10, 100), 'tau')

alpha['negative'] = fuzz.trimf(alpha.universe, [-np.pi/2, -np.pi/4, 0])
alpha['zero'] = fuzz.trimf(alpha.universe, [-np.pi/4, 0, np.pi/4])
alpha['positive'] = fuzz.trimf(alpha.universe, [0, np.pi/4, np.pi/2])

alpha_dot['negative'] = fuzz.trimf(alpha_dot.universe, [-10, -5, 0])
alpha_dot['zero'] = fuzz.trimf(alpha_dot.universe, [-5, 0, 5])
alpha_dot['positive'] = fuzz.trimf(alpha_dot.universe, [0, 5, 10])

tau['negative'] = fuzz.trimf(tau.universe, [-10, -5, 0])
tau['zero'] = fuzz.trimf(tau.universe, [-5, 0, 5])
tau['positive'] = fuzz.trimf(tau.universe, [0, 5, 10])

# تعریف قوانین فازی
rule1 = ctrl.Rule(alpha['negative'] & alpha_dot['negative'], tau['positive'])
rule2 = ctrl.Rule(alpha['negative'] & alpha_dot['zero'], tau['positive'])
rule3 = ctrl.Rule(alpha['negative'] & alpha_dot['positive'], tau['zero'])
rule4 = ctrl.Rule(alpha['zero'] & alpha_dot['negative'], tau['positive'])
rule5 = ctrl.Rule(alpha['zero'] & alpha_dot['zero'], tau['zero'])
rule6 = ctrl.Rule(alpha['zero'] & alpha_dot['positive'], tau['negative'])
rule7 = ctrl.Rule(alpha['positive'] & alpha_dot['negative'], tau['zero'])
rule8 = ctrl.Rule(alpha['positive'] & alpha_dot['zero'], tau['negative'])
rule9 = ctrl.Rule(alpha['positive'] & alpha_dot['positive'], tau['negative'])

# سیستم کنترل فازی
tau_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
fuzzy_sim = ctrl.ControlSystemSimulation(tau_ctrl)

# تابع کنترل فازی
def fuzzy_control(alpha_value, alpha_dot_value):
    fuzzy_sim.input['alpha'] = alpha_value
    fuzzy_sim.input['alpha_dot'] = alpha_dot_value
    fuzzy_sim.compute()
    return fuzzy_sim.output['tau']

# تابع دینامیک پاندول معکوس
def dynamics_with_fuzzy_control(t, state):
    theta, theta_dot, alpha, alpha_dot = state
    
    # اعمال کنترل فازی
    tau = fuzzy_control(alpha, alpha_dot)
    
    # محاسبات دینامیکی سیستم
    coriolis = m_p * l_p * alpha_dot**2 * np.sin(alpha)
    theta_ddot = (tau - coriolis) / I_a
    
    gravitation = m_p * g * l_p * np.sin(alpha)
    alpha_ddot = (-m_p * l_p * theta_dot**2 * np.cos(alpha) - gravitation) / I_p
    
    return [theta_dot, theta_ddot, alpha_dot, alpha_ddot]

# شرایط اولیه و تنظیمات شبیه‌سازی
t_span = (0, 10)
initial_state = [0, 0, np.pi / 4, 0]  # [theta, theta_dot, alpha, alpha_dot]
t_eval = np.linspace(0, 10, 1000)

# شبیه‌سازی دینامیک
sol = solve_ivp(dynamics_with_fuzzy_control, t_span, initial_state, t_eval=t_eval)

# نمایش نتایج
theta = sol.y[0]
alpha = sol.y[2]

plt.plot(sol.t, theta, label='زاویه چرخش (theta)')
plt.plot(sol.t, alpha, label='زاویه پاندول (alpha)')
plt.xlabel('زمان (ثانیه)')
plt.ylabel('زاویه (رادیان)')
plt.legend()
plt.title('شبیه‌سازی پاندول معکوس با کنترل‌کننده فازی')
plt.show()
