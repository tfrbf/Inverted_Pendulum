A = [0 1 0; 0 0 1; -2 -3 -4];
B = [0; 0; 1];
C = [1 0 0];
D = 0;

% محاسبه ماتریس فیدبک
poles = [-2, -3, -4];
K = place(A, B, poles);

% تعریف مدل در Simulink
simulinkModel = 'state_feedback_system';
new_system(simulinkModel);
open_system(simulinkModel);

% بلوک‌ها را اضافه کنید
add_block('simulink/Continuous/State-Space', [simulinkModel '/State-Space'], ...
          'A', mat2str(A), 'B', mat2str(B), 'C', mat2str(C), 'D', mat2str(D), ...
          'Position', [100, 100, 200, 200]);

add_block('simulink/Math Operations/Gain', [simulinkModel '/Gain'], ...
          'Gain', mat2str(-K), ...
          'Position', [300, 100, 350, 150]);

add_block('simulink/Math Operations/Sum', [simulinkModel '/Sum'], ...
          'Inputs', '|+', ...
          'Position', [250, 100, 300, 150]);

add_block('simulink/Sinks/Scope', [simulinkModel '/Scope'], ...
          'Position', [400, 100, 450, 150]);

% اتصال بلوک‌ها
add_line(simulinkModel, 'State-Space/1', 'Sum/1');
add_line(simulinkModel, 'Sum/1', 'State-Space/2');
add_line(simulinkModel, 'State-Space/1', 'Gain/1');
add_line(simulinkModel, 'Gain/1', 'Sum/2');
add_line(simulinkModel, 'State-Space/1', 'Scope/1');

% ذخیره و باز کردن مدل
save_system(simulinkModel);
open_system(simulinkModel);
