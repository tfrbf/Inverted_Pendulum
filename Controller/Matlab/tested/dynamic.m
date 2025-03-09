clc;
clear;
close all;


t = 1:0.001:20;
x0 = [0.3 ,0.1, -0.1, 0];
[t ,x] = ode45('sys1',t,x0);

figure
plot(t,x(:,1),t,x(:,2),t,x(:,3),t,x(:,4),'LineWidth',1.5)
grid on;
ylabel('theta');
xlabel('time(s)');
title('state variabels');
legend('alpha', 'alpha dot', 'U', 'theta') ;
%ylim([-1,4]);


