import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. تعریف متغیرهای فازی ورودی
theta = ctrl.Antecedent(np.arange(-np.pi, np.pi, 0.01), 'theta')  # زاویه
theta_dot = ctrl.Antecedent(np.arange(-10, 10, 0.1), 'theta_dot')  # سرعت زاویه‌ای

# 2. تعریف متغیر فازی خروجی
force = ctrl.Consequent(np.arange(-50, 50, 0.1), 'force')

# 3. توابع عضویت برای ورودی و خروجی
# زاویه (theta)
theta['very_negative'] = fuzz.trimf(theta.universe, [-np.pi, -np.pi, -np.pi/2])
theta['negative'] = fuzz.trimf(theta.universe, [-np.pi, -np.pi/2, 0])
theta['zero'] = fuzz.trimf(theta.universe, [-np.pi/4, 0, np.pi/4])
theta['positive'] = fuzz.trimf(theta.universe, [0, np.pi/2, np.pi])
theta['very_positive'] = fuzz.trimf(theta.universe, [np.pi/2, np.pi, np.pi])

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

# و ... (ادامه قوانین مشابه برای پوشش تمام شرایط)
# هرچه قوانین بیشتری تعریف کنید، کنترل سیستم دقیق‌تر خواهد بود.

# 5. تعریف سیستم کنترل فازی
pendulum_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
pendulum_simulation = ctrl.ControlSystemSimulation(pendulum_ctrl)

# 6. مثال برای محاسبه خروجی کنترل فازی با مقدار ورودی مشخص
pendulum_simulation.input['theta'] = 0.1  # مقدار آزمایشی زاویه
pendulum_simulation.input['theta_dot'] = 1.5  # مقدار آزمایشی سرعت زاویه‌ای

pendulum_simulation.compute()  # محاسبه نیروی کنترلی بر اساس سیستم فازی
print("Control Force:", pendulum_simulation.output['force'])

# 7. رسم نمودارهای فازی
theta.view()
theta_dot.view()
force.view()
plt.show()
