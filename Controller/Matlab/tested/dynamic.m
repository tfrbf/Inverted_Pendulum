clc;
clear;
close all;


t = 1:0.01:10;
x0 = [0.1 ,0.1];
[t ,x] = ode45('sys1',t,x0);

figure
plot(t,x(:,1),t,x(:,2),'LineWidth',1.5)
grid on;
ylabel('theta');
xlabel('time(s)');
title('state variabels');
legend('theta', 'dtheta') ;
ylim([-1,4]);


