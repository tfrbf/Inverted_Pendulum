% Denominator of the transfer functions (shared for all outputs)
den = [1, 5.551e-17, -0.1423, 0]; % Example denominator from image

% Compute the poles of the system
poles = roots(den);
disp('Poles of the system:');
disp(poles);

% Define the state-space representation (if not directly given)
% Use transfer function to state-space conversion if needed:
[num1, den] = tfdata(tf([0.3267, 0, 1.417e-19], den), 'v'); % Output 1
[num2, ~] = tfdata(tf([-0.0124, 0, -0.02352], den), 'v');  % Output 2

% Combine into state-space (if matrices are unknown)
[A, B, C, D] = tf2ss(num1, den); % Use one transfer function to build A, B, C, D

% Define desired pole locations for feedback
desired_poles = [-1, -2, -3, -4]; % Example (adjust based on requirements)

% Compute state feedback gain
K = place(A, B, desired_poles); % Pole placement
disp('State feedback gain K:');
disp(K);
