% Define state-space matrices
A = [0 1 0 0;
     0.1423 0 0 0;
     0 0 0 1;
    -0.0774 0 0 0]; % Example A matrix
B = [0; 0.3267; 0; -0.0124]; % Example B matrix
C = [1 0 0 0;
    0 0 1 0];     % Example C matrix
D = [0;0];             % Example D matrix
% Convert state-space to transfer function
% Convert state-space to transfer function
[num, den] = ss2tf(A, B, C, D);

% Number of outputs
num_outputs = size(C, 1);

% Initialize the transfer function matrix
TF_matrix = tf(zeros(num_outputs, 1)); % Preallocate as a column vector for SIMO

% Compute the transfer functions for each output
for i = 1:num_outputs
    TF_matrix(i) = tf(num(i, :), den);
end

% Display the transfer function matrix
disp('Transfer Function Matrix:');
disp(TF_matrix);

% Optional: Plot transfer functions for visualization
figure;
for i = 1:num_outputs
    subplot(num_outputs, 1, i);
    bode(TF_matrix(i));
    title(['Bode Plot for Output ', num2str(i)]);
end