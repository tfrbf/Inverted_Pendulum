clc;
clear;
close all;

% Define the parameters
a = 3.291;
b = 0.12519;
c = 0.23688;
d = 6.0521;

% Define the state-space matrices
A_p = [0, 1, 0, 0;
       ((-c * d) / (d * b - (a * a))), 0, 0, 0;
       0, 0, 0, 1;
       ((c * a) / (d * b - (a * a))), 0, 0, 0];

B_p = [0;
       (-a) / (d * b - a * a);
       0;
       b / (d * b - a * a)];

C_p = [1, 0, 0, 0;
       0, 0, 1, 0];

D_p = [0;
       0];

% Convert to transfer function for the first output
[num, den] = ss2tf(A_p, B_p, C_p, D_p, 1); % First output selected
G = tf(num(1, :), den); % Transfer function for the first output

% Auto-tune PID controller
desired_bandwidth = 1;  % You can adjust this parameter based on response time
[PID_controller, info] = pidtune(G, 'PID', desired_bandwidth);

% Display tuned parameters
Kp = PID_controller.Kp;
Ki = PID_controller.Ki;
Kd = PID_controller.Kd;
disp(['Tuned PID gains: Kp = ' num2str(Kp) ', Ki = ' num2str(Ki) ', Kd = ' num2str(Kd)]);

% Create closed-loop system with tuned controller
Closed_Loop_System = feedback(PID_controller * G, 1);

% Plot step response to evaluate performance
step(Closed_Loop_System);
title('Closed-Loop Step Response with Auto-Tuned PID Controller');
grid on;
