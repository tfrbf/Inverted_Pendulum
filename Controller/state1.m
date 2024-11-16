A = [0 1 0 0;
     0.1423 0 0 0;
     0 0 0 1;
    -0.0774 0 0 0];% Example A matrix
B = [0; 0.3267; 0; -0.0124]; % Example B matrix  % Example B matrix (single input)
C = [1 0 0 0;       % Output matrix (for SIMO system)
     0 1 0 0];
D = [0; 0];         % Direct transmission matrix

% Check dimensions of A and B
disp('Dimensions of A:');
disp(size(A));
disp('Dimensions of B:');
disp(size(B));

% Define desired poles for the state feedback controller
desired_poles = [-2, -3, -4, -5]; % Adjust as per stability and performance needs

% Ensure the number of desired poles equals the number of rows in A
if length(desired_poles) ~= size(A, 1)
    error('The number of desired poles must equal the number of states (rows in A).');
end

% Compute state feedback gain using pole placement
K = place(A, B, desired_poles);

% Display the state feedback gain
disp('State feedback gain K:');
disp(K);
